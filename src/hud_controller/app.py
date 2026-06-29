"""Validation CLI for imagectl3 -v (patch sanity checks)."""

import asyncio
import logging

import click

import hud_controller.problems
from hud_controller.grading_runner import GradingRunner
from hud_controller.prompts import get_spec
from hud_controller.utils import import_submodules

import_submodules(hud_controller.problems)

logger = logging.getLogger(__name__)


async def validate_problem(problem_id: str) -> tuple[bool, dict[str, object]]:
    """Validate the test and golden patches for a problem."""
    spec = get_spec(problem_id)

    if not spec.base:
        raise ValueError(f"Problem {problem_id} missing base branch/commit")
    if not spec.test:
        raise ValueError(f"Problem {problem_id} missing test branch/commit")
    if not spec.golden:
        raise ValueError(f"Problem {problem_id} missing golden branch/commit")

    logger.info("=== VALIDATE_PROBLEM DEBUG ===")
    logger.info("Problem ID: %s", problem_id)
    logger.info("Base: %s", spec.base)
    logger.info("Test: %s", spec.test)
    logger.info("Golden: %s", spec.golden)
    logger.info("Test files: %s", spec.test_files)

    runner = GradingRunner(
        base=spec.base,
        test=spec.test,
        golden=spec.golden,
        test_files=spec.test_files,
    )

    success, result = runner.validate_patches()

    if success:
        logger.info("Validation successful!")
    else:
        logger.error("Validation failed!")

    if "junit" in result:
        print("\nJUnit XML Result:")
        print(result["junit"])

    return success, result


@click.command()
@click.argument("problem_id", envvar="PROBLEM_ID")
@click.option("--output_path", default="/tmp/validate_junit.xml", help="Path to output the JUNIT XML file")
def validate_problem_script(problem_id: str, output_path: str | None = None):
    """Validate a problem solution and return the validation results."""
    success, result = asyncio.run(validate_problem(problem_id))

    if output_path and "junit" in result:
        with open(output_path, "w") as f:
            f.write(str(result["junit"]))

    if success:
        raise SystemExit(0)
    raise SystemExit(1)
