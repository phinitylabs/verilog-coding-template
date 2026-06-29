#!/usr/bin/env python3
"""Print the prompt for a given problem id."""

from __future__ import annotations

import argparse
import os

import hud_controller.problems
from hud_controller.prompts import get_spec, spec_to_statement
from hud_controller.utils import import_submodules

import_submodules(hud_controller.problems)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("problem_id")
    parser.add_argument("--hints", action="store_true", default=False)
    args = parser.parse_args()

    os.environ["HINTS"] = "all" if args.hints else "none"

    spec = get_spec(args.problem_id)
    print(spec_to_statement(spec))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
