#!/usr/bin/env python3
"""Local Docker eval driver for per-problem verilog images.

Routes each task slug to its Docker image via a callable DockerRuntime provider.
"""

from __future__ import annotations

import argparse
import asyncio
import contextlib
import sys
import uuid

from hud import DockerRuntime, Taskset
from hud.agents import create_agent
from hud.agents.base import Agent
from hud.eval.job import Job
from hud.eval.run import rollout
from hud.telemetry import flush

from hud_controller.eval_agent import VerilogClaudeAgent

ENV_NAME = "verilog-coding-template"
IMAGE_PREFIX = "verilog_"
DEFAULT_TASKS_FILE = "tasks.py"
DEFAULT_ROLLOUT_TIMEOUT = 7200.0
HEARTBEAT_INTERVAL_S = 60.0


def _log(msg: str) -> None:
    print(msg, flush=True)


def _job_url(job_id: str) -> str:
    return f"https://hud.ai/jobs/{job_id}"


def _job_name(taskset_name: str, task_list, group: int) -> str:
    suffix = f" ({group} times)" if group > 1 else ""
    if len(task_list) == 1:
        return f"{task_list[0].id}{suffix}"
    return f"{taskset_name} ({len(task_list)} tasks){suffix}"


def make_agent(agent_name: str, model: str | None, max_steps: int):
    """Build a v6 gateway agent for the requested provider."""
    if agent_name == "claude":
        model_id = model or "claude-sonnet-4-5"
        base = create_agent(model_id, max_steps=max_steps)
        return VerilogClaudeAgent(base.config)
    if agent_name == "openai":
        model_id = model or "gpt-4o"
        return create_agent(model_id, max_steps=max_steps)
    if agent_name == "gemini":
        model_id = model or "gemini-2.5-pro"
        return create_agent(model_id, max_steps=max_steps)
    raise SystemExit(f"unknown agent: {agent_name!r} (use claude, openai, or gemini)")


def docker_runtime_for_task(task):
    """Fresh container per rollout; image tag matches imagectl3 naming."""
    image = f"{IMAGE_PREFIX}{task.slug}"
    # DockerRuntime publishes 127.0.0.1:<host>->8765; --network none blocks that.
    return DockerRuntime(image)(task)


async def _heartbeat(
    done: asyncio.Event,
    *,
    completed: list[int],
    total: int,
    job_id: str,
) -> None:
    while not done.is_set():
        try:
            await asyncio.wait_for(done.wait(), timeout=HEARTBEAT_INTERVAL_S)
        except asyncio.TimeoutError:
            _log(
                f"  ... still running ({completed[0]}/{total} rollouts done) — {_job_url(job_id)}"
            )


async def run_taskset_with_progress(
    taskset: Taskset,
    agent: Agent,
    *,
    runtime,
    group: int,
    max_concurrent: int | None,
    rollout_timeout: float | None,
    agent_name: str,
    model: str | None,
    max_steps: int,
) -> Job:
    """Like ``Taskset.run`` but prints the job URL up front and rollout progress."""
    task_list = list(taskset)
    expanded: list[tuple] = []
    for task in task_list:
        group_id = uuid.uuid4().hex
        expanded.extend((task, group_id) for _ in range(group))

    job = await Job.start(
        _job_name(taskset.name, task_list, group),
        group=group,
        taskset_id=taskset.api_id,
    )
    total = len(expanded)
    completed = [0]
    done = asyncio.Event()
    lock = asyncio.Lock()
    model_label = model or f"{agent_name} default"

    _log(f"Starting eval: {len(task_list)} task(s) x {group} rollout(s) = {total} total")
    _log(f"  agent={agent_name}  model={model_label}  max_steps={max_steps}")
    _log(f"  job: {_job_url(job.id)}")
    _log(
        "Rollouts in progress (traces stream to the job URL; "
        "the first completion may take several minutes)..."
    )

    sem = asyncio.Semaphore(max_concurrent) if max_concurrent else None
    heartbeat = asyncio.create_task(
        _heartbeat(done, completed=completed, total=total, job_id=job.id),
    )

    async def _run_one(task, group_id: str):
        async def _rollout():
            return await rollout(
                task,
                agent,
                runtime=runtime,
                job_id=job.id,
                group_id=group_id,
                rollout_timeout=rollout_timeout,
            )

        if sem is not None:
            async with sem:
                run = await _rollout()
        else:
            run = await _rollout()

        async with lock:
            completed[0] += 1
            n = completed[0]
        _log(f"  [{n}/{total}] {task.slug} finished (reward={run.reward:.2f})")
        return run

    try:
        job.runs.extend(await asyncio.gather(*(_run_one(t, gid) for t, gid in expanded)))
    finally:
        done.set()
        heartbeat.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await heartbeat

    if not await asyncio.to_thread(flush, timeout=120.0):
        _log("  (warning: telemetry flush did not fully drain within 120s)")

    return job


async def run_eval(args: argparse.Namespace) -> int:
    taskset = Taskset.from_file(args.tasks)
    if args.ids:
        taskset = taskset.filter(args.ids)

    if len(taskset) == 0:
        print("No tasks matched the given filters.", file=sys.stderr)
        return 1

    max_steps = 100 if args.full else args.max_steps
    agent = make_agent(args.agent, args.model, max_steps=max_steps)

    job = await run_taskset_with_progress(
        taskset,
        agent,
        runtime=docker_runtime_for_task,
        group=args.group_size,
        max_concurrent=args.max_concurrent,
        rollout_timeout=args.rollout_timeout,
        agent_name=args.agent,
        model=args.model,
        max_steps=max_steps,
    )

    _log(f"Done. Mean reward: {job.reward:.2f}")
    _log(f"job: {_job_url(job.id)}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Run verilog HUD v6 evals in per-problem Docker images.")
    parser.add_argument("--ids", nargs="+", help="Task slug(s) to run (default: all in tasks.py)")
    parser.add_argument("--agent", default="claude", help="Agent harness: claude, openai, or gemini")
    parser.add_argument("--model", "-m", help="Model id passed to create_agent")
    parser.add_argument("--max-steps", type=int, default=10, help="Max agent steps per rollout")
    parser.add_argument("--full", action="store_true", help="Run all tasks with max-steps 100")
    parser.add_argument("--group-size", "--group", type=int, default=1, dest="group_size")
    parser.add_argument("--max-concurrent", type=int, default=None, help="Cap parallel rollouts (default: unlimited)")
    parser.add_argument(
        "--rollout-timeout",
        type=float,
        default=DEFAULT_ROLLOUT_TIMEOUT,
        help="Per-rollout wall-clock cap in seconds (default: 7200).",
    )
    parser.add_argument("--tasks", default=DEFAULT_TASKS_FILE, help="Path to tasks.py rows file")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation (no-op, for CLI compat)")
    args = parser.parse_args()

    raise SystemExit(asyncio.run(run_eval(args)))


if __name__ == "__main__":
    main()
