# Quick Start Guide

## Prerequisites

- Docker Desktop (running)
- Python 3.10+
- Git
- uv (`pip install uv`)
- GitHub Personal Access Token with repo access

## Setup

### 1. Clone the template

```bash
cd ~/Documents/GitHub
git clone https://github.com/phinitylabs/verilog-coding-template.git
cd verilog-coding-template
uv sync
```

### 2. Set GitHub token

```bash
export GITHUB_TOKEN=ghp_your_token_here
```

Add to your shell profile (~/.zshrc or ~/.bashrc) to persist.

### 3. Build and validate

```bash
# Build one problem
uv run utils/imagectl3.py verilog_ -b --ids lifo_stack

# Validate one problem
uv run utils/imagectl3.py verilog_ -v --ids lifo_stack

# Build and validate all registered problems
uv run utils/imagectl3.py verilog_ -bv --jobs 4
```

## Adding a New Problem

### 1. Clone the problems repo

```bash
git clone https://github.com/phinitylabs/microcode_sequencer.git
cd microcode_sequencer
```

### 2. Create branches

Each problem needs 3 branches:
- `<problem_id>_baseline` - Starting code (stubs or buggy)
- `<problem_id>_test` - Baseline + hidden tests
- `<problem_id>_golden` - Complete solution (no tests)

```bash
# Create baseline
git checkout main
git checkout -b my_problem_baseline
# Add sources/my_problem.v with TODO stubs
# Add tests/test_my_problem.py with pytest runner only
git add . && git commit -m "Baseline"

# Create test branch from baseline
git checkout -b my_problem_test
# Add tests/test_my_problem_hidden.py with actual tests
git add . && git commit -m "Add hidden tests"

# Create golden branch from baseline
git checkout my_problem_baseline
git checkout -b my_problem_golden
# Implement the solution in sources/my_problem.v
git add . && git commit -m "Golden solution"

# Push all branches
git push origin my_problem_baseline my_problem_test my_problem_golden
```

### 3. Register the problem

Edit `src/hud_controller/problems/basic.py` in verilog-coding-template:

```python
PROBLEM_REGISTRY.append(
    ProblemSpec(
        id="my_problem",
        description="""Task description here.""",
        difficulty="easy",  # easy, medium, or hard
        base="my_problem_baseline",
        test="my_problem_test",
        golden="my_problem_golden",
        test_files=["tests/test_my_problem_hidden.py"],
    )
)
```

### 4. Build and validate

```bash
uv run utils/imagectl3.py verilog_ -bv --ids my_problem
```

Expected: All 6 validation checks pass.

## Running Agent Evaluations

```bash
# Generate JSON config
uv run utils/imagectl3.py verilog_ -j

# Run evaluation (requires ANTHROPIC_API_KEY)
uv run hud eval local-hud.json claude --model claude-sonnet-4-5-20250929 --max-steps 150
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Clone fails in Docker | Check GITHUB_TOKEN is set and has repo access |
| Branch not found | Ensure all 3 branches are pushed to microcode_sequencer |
| Tests don't fail on baseline | Baseline must have incomplete/buggy code |
| Tests don't pass on golden | Golden solution is incorrect |
| Docker cache stale | Increment `ENV random=randomN` in Dockerfile |
