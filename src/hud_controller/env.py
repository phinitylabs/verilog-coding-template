"""HUD v6 environment: ssh workspace + two-yield task template."""

# NOTE: deliberately no `from __future__ import annotations` — breaks @env.template
# param types at deploy time in hud-python 0.6.x.

import logging
import os
import shlex
import subprocess
import sys

from hud import Environment
from hud.environment import Workspace
from hud.graders import EvaluationResult, SubScore

import hud_controller.problems  # noqa: F401 — register problems
from hud_controller.grading_runner import GradingRunner
from hud_controller.prompts import get_spec, spec_to_statement
from hud_controller.setup import start_dinit
from hud_controller.utils import import_submodules

import_submodules(hud_controller.problems)

logger = logging.getLogger(__name__)

REPO_PATH = "/home/ubuntu/example-verilog-codebase"
AGENT_UID = 1000
AGENT_GID = 1000
ENV_NAME = "verilog-coding-template"
# Agent bash/SFTP tools block until the remote command exits; cap hung sims (vvp, etc.).
SHELL_TIMEOUT_SECONDS = int(os.environ.get("SHELL_TIMEOUT_SECONDS", "600"))

# The env name MUST be a string literal for `hud deploy` static parsing.
env = Environment(name=ENV_NAME)


class _AgentWorkspace(Workspace):
    """Workspace whose interactive shell runs as the unprivileged ubuntu uid."""

    def shell_argv(self, command=None, *, cwd=None, env=None):
        if command is not None:
            command = (
                f"timeout --kill-after=30 {SHELL_TIMEOUT_SECONDS} "
                f"bash -lc {shlex.quote(command)}"
            )
        argv = super().shell_argv(command, cwd=cwd, env=env)
        if sys.platform != "win32" and hasattr(os, "geteuid") and os.geteuid() == 0:
            argv = [
                "setpriv",
                "--reuid",
                str(AGENT_UID),
                "--regid",
                str(AGENT_GID),
                "--clear-groups",
                "--",
                *argv,
            ]
        return argv


_ws = _AgentWorkspace(
    REPO_PATH,
    user="ubuntu",
    env={"HOME": "/home/ubuntu", "USER": "ubuntu", "LOGNAME": "ubuntu"},
)


@env.initialize
async def _up() -> None:
    await _ws.start()
    env.add_capability(_ws.capability("shell"))
    await start_dinit()


@env.shutdown
async def _down() -> None:
    await _ws.stop()


def setup_problem_workspace() -> None:
    """Reset the in-place git repo to the committed baseline before each episode."""
    subprocess.run(
        ["sudo", "-u", "ubuntu", "git", "reset", "--hard"],
        cwd=REPO_PATH,
        check=True,
    )
    subprocess.run(
        ["sudo", "-u", "ubuntu", "git", "clean", "-fd", "-e", ".hud"],
        cwd=REPO_PATH,
        check=True,
    )


def grade_with_runner(spec) -> EvaluationResult:
    """Run patch-based grading; fail closed on errors."""
    try:
        runner = GradingRunner(
            base=spec.base,
            test=spec.test,
            golden=spec.golden,
            test_files=spec.test_files,
        )
        success, result = runner.run_grading()
        reward = 1.0 if success else 0.0
        subscores = [
            SubScore(
                name="Tests",
                weight=1.0,
                value=reward,
                metadata=result,
            )
        ]
        return EvaluationResult(
            reward=reward,
            done=True,
            content="Grading passed" if success else "Grading failed",
            info={"problem_id": spec.id, **(result or {})},
            subscores=subscores,
        )
    except Exception as exc:
        logger.exception("Grading error for %s", spec.id)
        return EvaluationResult(
            reward=0.0,
            done=True,
            content=f"Grading error: {type(exc).__name__}: {exc}",
            info={"problem_id": spec.id, "error": str(exc)},
            subscores=[],
        )


@env.template(id="solve_problem")
async def solve_problem():
    """Reset workspace, prompt the agent, then grade via hidden test patch + pytest."""
    problem_id = os.environ.get("PROBLEM_ID", "")
    try:
        spec = get_spec(problem_id)
    except ValueError:
        yield "Error: PROBLEM_ID not configured for this image."
        yield EvaluationResult(
            reward=0.0,
            done=True,
            content=f"Unknown PROBLEM_ID: {problem_id!r}",
            info={"problem_id": problem_id},
            subscores=[],
        )
        return

    setup_problem_workspace()
    answer = yield spec_to_statement(spec)
    evaluation = grade_with_runner(spec)
    info = dict(evaluation.info or {})
    info["final_answer"] = None if answer is None else str(answer)
    evaluation.info = info
    yield evaluation
