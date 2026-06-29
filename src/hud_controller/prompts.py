"""Problem prompt helpers shared by env.py and imagectl3."""

import os

from hud_controller.spec import PROBLEM_REGISTRY, ProblemSpec

# [CUSTOMIZE] Update this template for your project
template = """
You will be working on a task for example-verilog-codebase.
The repository has already been cloned in the environment in /home/ubuntu/example-verilog-codebase.
Iverilog and Verilator have been installed.
Do not change any of the input or output ports of the modules.

You should write verilog testbenches to test your code and ensure it matches the functional specification (in addition to syntactic correctness).

Use the tools provided to complete the following task:

<STATEMENT>
"""


def spec_to_statement(spec: ProblemSpec) -> str:
    """Convert a problem spec to a statement."""
    hints_enabled = os.environ.get("HINTS", "none").lower() in ["all"]
    statement = spec.description

    if hints_enabled and len(spec.hints) > 0:
        hint_text = ""
        for hint_spec in spec.hints:
            hint_text += f"\n - {hint_spec.text}\n"
        statement += "\n\n" + f"<HINTS>{hint_text}</HINTS>"
    return template.replace("<STATEMENT>", statement)


def get_spec(problem_id: str) -> ProblemSpec:
    """Look up a problem spec by id."""
    for spec in PROBLEM_REGISTRY:
        if spec.id == problem_id:
            return spec
    raise ValueError(f"No problem found for id: {problem_id}")
