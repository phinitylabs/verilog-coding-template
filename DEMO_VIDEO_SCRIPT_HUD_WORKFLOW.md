# 🎬 Demo Video Script: Converting a Verilog Problem to HUD Format

**Video Title:** "Complete Walkthrough: Converting a Verilog Problem to HUD Format for AI Agent Evaluation"  
**Duration:** ~20-25 minutes  
**Goal:** Show the complete workflow from a local problem directory to validated HUD task with pass@10 evaluation

---

## 🎯 What This Video Covers

"Hi! Today I'm going to show you how to convert a Verilog problem to HUD format for AI agent evaluation. I'll be starting from scratch in my IDE, creating:
- A detailed specification in `docs/`
- Hidden tests and golden solution in `harness/`
- Empty RTL starting files in `rtl/`

Then I'll show you how to:
1. Initialize Git and create the three required branches
2. Push to GitHub
3. Integrate with the HUD evaluation framework
4. Validate the task
5. Run a pass@10 evaluation to see how AI agents perform"

---

## 📁 Branch Structure Overview

**[Show this diagram early to explain the concept]**

Here's how the directory structure changes across branches:

| Content | Master (Initial) | Baseline | Test | Golden |
|---------|-----------------|----------|------|--------|
| `docs/` | ✅ | ✅ | ✅ | ✅ |
| `prompt.txt` | ✅ | ✅ | ✅ | ✅ |
| `hints.txt` | ✅ | ✅ | ✅ | ✅ |
| `sources/` (empty) | ✅ | ✅ | ✅ | ❌ |
| `sources/` (solution) | ❌ | ❌ | ❌ | ✅ |
| `harness/` | ✅ | ❌ | ❌ | ❌ |
| `tests/` | ❌ | ❌ | ✅ | ❌ |

**Key idea:** We start with `master` containing everything in `harness/`, then create three branches by reorganizing the files:
- **Baseline**: Empty starting point (no tests, no solution)
- **Test**: Baseline + tests extracted from `harness/test/`
- **Golden**: Baseline + solution extracted from `harness/patch/`

---

## 🔄 Workflow Overview

**[Show this flowchart]**

```
1. Create Directory Structure in IDE
   ├── docs/Specification.md
   ├── harness/patch/sources/ (golden solution)
   ├── harness/test/ (hidden test file)
   ├── sources/ (empty starter)
   └── prompt.txt, hints.txt
   
2. Initialize Git → Commit "master"
   
3. Create 3 Branches:
   ├── baseline (remove harness/)
   ├── test (extract tests from harness/)
   └── golden (extract solution from harness/)
   
4. Push to GitHub
   
5. Update HUD Framework:
   ├── Modify Dockerfile (point to your repo)
   ├── Register problem in basic.py
   └── Build Docker image
   
6. Validate Task (6 checks)
   
7. Generate HUD JSON
   
8. Run pass@10 Evaluation 🎯
```

---

## Part 1: Creating the Problem Directory Structure (0:00-3:00)

**[Narration]**
"I'm going to create a new Verilog problem from scratch. I already have my specification written, my golden solution tested, and my hidden test files ready. Now I need to set up the directory structure for HUD."

### 1.1 Create Directory in Finder

**[Screen: Finder]**
1. Navigate to `~/Documents/GitHub/`
2. Right-click → "New Folder"
3. Name it: `problem5_rc5_ca_keygen`

**[Narration]**
"This will be our problem repository. Now let's open it in VS Code (or your IDE of choice)."

### 1.2 Open in IDE

**[Screen: Terminal or IDE]**

```bash
cd ~/Documents/GitHub/problem5_rc5_ca_keygen
code .
```

**[Screen: VS Code opens with empty folder]**

### 1.3 Create Directory Structure

**[Narration]**
"Now I'll create the directory structure. For HUD, we need this specific layout before we create Git branches."

**[Screen: VS Code, create folders]**

1. Create folder: `docs/`
2. Create folder: `harness/`
3. Create folder: `harness/patch/`
4. Create folder: `harness/patch/sources/`
5. Create folder: `harness/test/`
6. Create folder: `sources/`

**[Show final structure in VS Code sidebar]**

```
problem5_rc5_ca_keygen/
├── docs/
├── harness/
│   ├── patch/
│   │   └── sources/
│   └── test/
└── sources/
```

**[Narration]**
"Perfect! Now let's add the actual files."

---

## Part 2: Add Files to the Problem Directory (3:00-8:00)

**[Narration]**
"Now I'll create each file and paste in the content. I already have these written, so I'll just paste them in."

### 2.1 Create `pyproject.toml`

**[Screen: VS Code]**
1. Right-click on root folder → New File
2. Name: `pyproject.toml`
3. Paste:

```toml
[project]
name = "verilog-problems"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "cocotb>=1.8.0",
    "pytest>=7.0.0",
    "pytest-xdist>=3.0.0",
]
```

**[Narration]**
"This file declares the Python dependencies needed for testing. HUD requires this!"

### 2.2 Create `prompt.txt`

**[Screen: VS Code]**
1. New File → `prompt.txt`
2. Paste in the task description

**[Show content briefly]**

```
Spec-to-rtl task:

Title: RC5 encryption core with custom key generation

Implement a synthesizable SystemVerilog module rc5_enc_16bit that performs 
RC5 encryption per docs/Specification.md...
```

### 2.3 Create `hints.txt`

**[Screen: VS Code]**
1. New File → `hints.txt`
2. Paste content:

```
1. key generation: The number of keys required for two rounds have 
   to be generated in the first state of FSM
2. Use LFSR for pseudo-random key generation
```

### 2.4 Create Specification

**[Screen: VS Code]**
1. New File → `docs/Specification.md`
2. Paste the full RC5 specification

**[Narration]**
"This is a detailed specification with the RC5 algorithm, interface requirements, FSM details, etc. I'll paste it all in..."

**[Show scrolling through the spec briefly]**

### 2.5 Create Empty Starter File

**[Screen: VS Code]**
1. New File → `sources/rc5_enc_16bit.sv`
2. Add just the module signature:

```systemverilog
`timescale 1ns/1ps

module rc5_enc_16bit(
    input clock,
    input reset,
    input enc_start,
    input [15:0] p,
    input [7:0] lfsr_key_enc,
    output reg [15:0] c,
    output reg enc_done
);

// TODO: Implement RC5 encryption

endmodule
```

**[Narration]**
"This is the empty starting point. The AI agent will need to fill in the implementation."

### 2.6 Create Golden Solution

**[Screen: VS Code]**
1. New File → `harness/patch/sources/rc5_enc_16bit.sv`
2. Paste the complete working implementation

**[Narration]**
"This is my golden solution - fully tested and working. I'm putting it in the harness/patch/sources directory."

**[Show scrolling through the solution briefly]**

### 2.7 Create Hidden Test File

**[Narration]**
"Now the critical part - creating ONE test file that contains both the cocotb tests AND a pytest wrapper function."

**[Screen: VS Code]**
1. New File → `harness/test/test_rc5_ca_keygen.py`
2. Paste the complete test file:

```python
import cocotb
from cocotb.triggers import Timer, RisingEdge

@cocotb.test()
async def test_rc5_basic(dut):
    """Test basic RC5 encryption"""
    # Initialize
    dut.reset.value = 0
    await Timer(10, unit="ns")
    dut.reset.value = 1
    
    # Test encryption with plaintext 0x1234
    dut.p.value = 0x1234
    dut.lfsr_key_enc.value = 0xAB
    dut.enc_start.value = 1
    
    # Wait for done signal
    while dut.enc_done.value == 0:
        await RisingEdge(dut.clock)
    
    # Check ciphertext
    assert dut.c.value == 0x9530, f"Expected 0x9530, got {dut.c.value}"

# ✅ CRITICAL: Pytest wrapper function (required by HUD!)
def test_rc5_ca_keygen_runner():
    """Pytest wrapper for cocotb tests"""
    import os
    from pathlib import Path
    from cocotb_tools.runner import get_runner
    
    sim = os.getenv("SIM", "icarus")
    proj_path = Path(__file__).resolve().parent.parent
    
    sources = [proj_path / "sources/rc5_enc_16bit.sv"]
    
    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="rc5_enc_16bit",
        always=True,
    )
    
    runner.test(
        hdl_toplevel="rc5_enc_16bit",
        test_module="test_rc5_ca_keygen"
    )
```

**[Narration]**
"This ONE file has everything: the cocotb tests at the top, and the pytest wrapper function at the bottom. Without the wrapper, pytest won't find any tests!"

### 2.8 Verify Directory Structure

**[Screen: VS Code sidebar]**

```
problem5_rc5_ca_keygen/
├── docs/
│   └── Specification.md         ✅ Detailed spec
├── harness/
│   ├── patch/
│   │   └── sources/
│   │       └── rc5_enc_16bit.sv ✅ Golden solution
│   └── test/
│       └── test_rc5_ca_keygen.py ✅ Tests + Pytest wrapper (ONE file!)
├── hints.txt                    ✅ Optional hints
├── prompt.txt                   ✅ Task description
├── pyproject.toml               ✅ Python dependencies (required!)
└── sources/
    └── rc5_enc_16bit.sv         ✅ Empty starting point
```

**[Narration]**
"Perfect! All files are in place. Key points to notice:
- ONE test file with both cocotb tests and pytest wrapper
- Using `sources/` directory, NOT `rtl/`
- `pyproject.toml` with dependencies
Now we're ready to initialize Git!"

---

## Part 3: Initialize Git Repository (8:00-10:00)

**[Narration]**
"Now we need to turn this into a Git repository. HUD uses Git branches to separate the baseline (empty), test (with hidden tests), and golden (with solution) states."

### 3.1 Create `.gitignore`

**[Screen: VS Code]**
1. New File → `.gitignore` (in root)
2. Paste:

```gitignore
# Python
__pycache__/
*.py[cod]
.pytest_cache/
*.egg-info/

# Simulation outputs
sim_build/
*.vvp
*.vcd
*.fst

# Logs
*.log

# IDE
.vscode/
.DS_Store
```

**[Narration]**
"This prevents build artifacts and IDE files from being committed."

### 3.2 Initialize Git

**[Screen: VS Code integrated terminal]**

```bash
# Make sure we're in the problem directory
cd ~/Documents/GitHub/problem5_rc5_ca_keygen

# Initialize Git repository
git init

# Check what we have
git status
```

**[Show output]**
"We can see all our files are untracked. Let's commit this initial state."

### 3.3 Initial Commit

```bash
# Stage all files
git add .

# Commit
git commit -m "Initial commit with harness structure"

# Verify
git log --oneline
```

**[Show]**
"Great! Now we have our initial commit with everything - the harness directory with tests and solution, the empty RTL starters, docs, and prompts."

---

## Part 4: Create Baseline Branch (12:00-14:00)

**[Narration]**
"The baseline branch is the starting point for AI agents. It has empty/stub RTL files, the spec, and the prompt, but NO tests or solutions. We need to remove the harness directory."

### 4.1 Create Baseline Branch

**[Screen: Terminal]**

```bash
# Create and checkout baseline branch
git checkout -b rc5_ca_keygen_baseline
```

**[Narration]**
"Now we're on the baseline branch. Let's remove the harness directory since agents shouldn't see tests or solutions."

### 4.2 Remove Harness Directory

**[Screen: VS Code]**
- Right-click on `harness/` folder → Delete
- Or in terminal:

```bash
rm -rf harness/
```

**[Screen: Show VS Code sidebar - no harness folder]**

### 4.3 Commit Baseline

```bash
# Check what changed
git status

# Stage the deletion
git add -A

# Commit
git commit -m "Baseline: remove harness (tests and solution)"

# Verify directory structure
ls -la
```

**[Show output]**

```
✓ docs/
✓ sources/ (empty starter file)
✓ prompt.txt
✓ hints.txt
✓ .gitignore
✗ No harness/ directory
```

**[Narration]**
"Perfect! The baseline branch only has the empty starting point in `sources/`, specification, and prompts. This is what the AI agent will see."

---

## Part 5: Create Test Branch (14:00-17:00)

**[Narration]**
"The test branch adds the hidden tests to the baseline. When we apply the test patch to baseline, tests should FAIL because there's no implementation yet."

### 5.1 Go Back to Master and Create Test Branch

**[Screen: Terminal]**

```bash
# Go back to master (which has the harness directory)
git checkout master

# Create test branch from master
git checkout -b rc5_ca_keygen_test
```

**[Narration]**
"We start from master because it has the harness directory with our test files."

### 5.2 Reorganize Files for Test Branch

**[Screen: VS Code]**

1. Create `tests/` folder in root
2. Drag `harness/test/test_rc5_ca_keygen.py` → `tests/test_rc5_ca_keygen.py` (same name)
3. Delete the entire `harness/` folder

**[Or via terminal if preferred]**

```bash
# Create tests directory
mkdir -p tests

# Copy test file (already has pytest wrapper inside!)
cp harness/test/test_rc5_ca_keygen.py tests/

# Remove harness directory
rm -rf harness/
```

**[Narration]**
"We're copying ONE file that already contains both the cocotb tests and the pytest wrapper function. No need for separate files!"

### 5.3 Commit Test Branch

```bash
# Check what changed
git status

# Stage changes
git add tests/
git add -A  # Include the deletion of harness/

# Commit
git commit -m "Test branch: add hidden tests"

# Verify structure
ls -la
```

**[Show output]**

```
✓ docs/
✓ sources/ (empty starter file)
✓ tests/test_rc5_ca_keygen.py (cocotb tests + pytest wrapper)
✓ prompt.txt
✓ hints.txt
✗ No harness/ directory
```

### 5.4 Verify Tests Fail on Empty Implementation

**[Narration]**
"Let's verify that tests fail without the implementation - this is crucial for HUD validation!"

**[Screen: Terminal]**

```bash
# Make sure we have pytest and cocotb
pip install pytest cocotb cocotb-test

# Run tests - they should FAIL ❌
pytest tests/ -v

# Expected output: FAILED (module has no implementation)
```

**[Show the failure output]**
"Perfect! Tests fail as expected because the RTL file only has the module signature with no implementation."

---

## Part 6: Create Golden Branch (17:00-20:00)

**[Narration]**
"The golden branch has the complete solution. When we apply both test patch AND golden patch to baseline, tests should PASS."

### 6.1 Go Back to Master and Create Golden Branch

**[Screen: Terminal]**

```bash
# Go back to master (which has the harness directory)
git checkout master

# Create golden branch from master
git checkout -b rc5_ca_keygen_golden
```

### 6.2 Copy Golden Solution

**[Screen: VS Code]**

1. Open `harness/patch/sources/rc5_enc_16bit.sv` (the golden solution)
2. Copy all the content (Cmd+A, Cmd+C)
3. Open `sources/rc5_enc_16bit.sv` (the empty starter)
4. Select all and paste (Cmd+A, Cmd+V)
5. Save (Cmd+S)

**[Or via terminal]**

```bash
# Copy golden solution to sources/ directory
cp harness/patch/sources/rc5_enc_16bit.sv sources/
```

**[Show briefly the complete golden solution in VS Code]**

### 6.3 Remove Harness Directory

**[Screen: VS Code]**
- Delete `harness/` folder

**[Or terminal]**

```bash
rm -rf harness/
```

### 6.4 Commit Golden Branch

```bash
# Check changes
git status

# Stage changes
git add sources/
git add -A  # Include harness deletion

# Commit
git commit -m "Golden branch: complete working solution"

# Verify structure
ls -la
```

**[Show output]**

```
✓ docs/
✓ sources/ (complete golden solution)
✓ prompt.txt
✓ hints.txt
✗ No harness/ directory
✗ No tests/ directory
```

### 6.5 Verify Golden Solution Works

**[Narration]**
"Let's verify that the golden solution passes all tests."

**[Screen: Terminal]**

```bash
# Temporarily add tests to verify
git checkout rc5_ca_keygen_test -- tests/

# Run tests - they should PASS ✅
pytest tests/ -v
```

**[Show the success output]**
"Excellent! All tests pass with the golden solution. This confirms our implementation is correct."

```bash
# Clean up (remove tests from golden branch)
rm -rf tests/
git checkout .  # Discard changes (tests)
```

**[Narration]**
"The golden branch should NOT have tests in the final version - just the solution."

---

## Part 7: Push to GitHub (20:00-22:00)

**[Narration]**
"Now let's push all three branches to GitHub so HUD can access them."

### 7.1 Create GitHub Repository

**[Screen capture: GitHub.com]**
1. Go to https://github.com
2. Click "New repository"
3. Name: `verilog-problems`
4. Make it Public (or Private with token)
5. Do NOT initialize with README
6. Click "Create repository"

### 7.2 Push All Branches

**[Screen: Terminal]**

```bash
# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/verilog-problems.git

# Push all three branches
git push -u origin rc5_ca_keygen_baseline
git push -u origin rc5_ca_keygen_test
git push -u origin rc5_ca_keygen_golden
```

**[Show the push progress]**

### 7.3 Verify on GitHub

**[Screen: Browser - GitHub]**
1. Go to your repository
2. Click on branch dropdown
3. Show all three branches exist

```bash
# Or verify via command line
git ls-remote --heads origin
```

**[Narration]**
"Perfect! All three branches are on GitHub. HUD will clone this repo and use these branches to create patches."

---

## Part 8: Integrate with HUD Framework (22:00-25:00)

**[Narration]**
"Now let's integrate this problem into the HUD evaluation framework."

### 8.1 Clone or Navigate to HUD Framework

```bash
cd ~/Documents/GitHub

# If you don't have it yet
git clone https://github.com/YOUR_ORG/verilog-template.git
cd verilog-template

# Or if you already have it
cd verilog-template
git pull origin main
```

### 8.2 Update Dockerfile to Point to Your Repo

**[Screen: VS Code - open Dockerfile]**

```bash
# Open Dockerfile in editor
code Dockerfile
```

**[Narration]**
"Find the section around line 108-112 where it clones the repository."

**[Screen: Show Dockerfile, scroll to the RUN git clone section]**

Update this section:

```dockerfile
# Example for public repo:
ENV random=random19  # ← Increment this number!
# Clone from public GitHub repository
RUN cd /home/ubuntu && \
    git clone https://github.com/YOUR_USERNAME/verilog-problems.git example-verilog-codebase && \
    chown -R ubuntu:ubuntu example-verilog-codebase

WORKDIR /home/ubuntu/example-verilog-codebase
```

**[Highlight the random variable]**
"Make sure to increment the `random` number whenever you change the repo URL. This forces Docker to rebuild without using cache."

**[Save the file]**

### 8.3 Register Problem in Framework

**[Screen: VS Code]**

```bash
# Open the problem registry
code src/hud_controller/problems/basic.py
```

**[Scroll to PROBLEM_REGISTRY list]**

**[Add to PROBLEM_REGISTRY]**

```python
PROBLEM_REGISTRY.append(
    ProblemSpec(
        id="rc5_ca_keygen",  # Must match your branch prefix
        description="""RC5 Encryption with Custom Key Generation

Implement an RC5 encryption module with LFSR-based key generation.

[Full prompt from your prompt.txt goes here]
""",
        base="rc5_ca_keygen_baseline",    # Branch names
        test="rc5_ca_keygen_test",
        golden="rc5_ca_keygen_golden",
        test_files=["tests/test_rc5_ca_keygen.py"],  # Test file path
        difficulty="hard",
        task_type="coding",
    )
)
```

---

## Part 9: Build Docker Image (25:00-27:00)

**[Narration]**
"Now let's build the Docker image. This packages your problem for HUD evaluation."

### 9.1 Install Dependencies

```bash
# Install uv if you haven't
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.cargo/env

# Or on Mac with Homebrew
brew install uv
```

### 9.2 Build Docker Image

**[Screen: Terminal]**

```bash
# Build the Docker image for your problem
uv run utils/imagectl3.py verilog_ -b --ids rc5_ca_keygen
```

**[Show build progress]**
"This will take a few minutes. Docker is:
1. Cloning your GitHub repo
2. Checking out all three branches
3. Generating patches (baseline→test, baseline→golden)
4. Installing dependencies
5. Creating the evaluation environment"

**[Show the final success message]**

### 9.3 Verify Docker Image

**[Screen: Terminal]**

```bash
# Check image was created
docker images | grep verilog_rc5_ca_keygen

# Check patches were generated inside the image
docker run --rm verilog_rc5_ca_keygen ls -la /home/root/*.patch
```

**[Show output]**
```
-rw-r--r-- 1 root root 4740 Nov 20 00:09 /home/root/golden.patch
-rw-r--r-- 1 root root 3851 Nov 20 00:09 /home/root/test.patch
```

**[Narration]**
"Perfect! Both patches were generated. These patches contain the diffs between branches."

---

## Part 10: Validate the Task (27:00-29:00)

**[Narration]**
"Validation ensures your task is properly set up. It checks that:
- Baseline compiles
- Test patch applies and causes failures
- Golden patch applies and passes tests"

### 10.1 Run Validation

**[Screen: Terminal]**

```bash
# Run validation
uv run utils/imagectl3.py verilog_ -v --ids rc5_ca_keygen
```

**[Show expected output scrolling]**

```
[validate verilog_rc5_ca_keygen]
  ✓ testBaselineCompiles
  ✓ testTestPatchApplies
  ✓ testTestPatchFailsTests      ← Tests fail without solution
  ✓ testGoldenPatchApplies
  ✓ testGoldenPatchCompiles
  ✓ testGoldenPatchPassesTests   ← Tests pass with solution
  
✅ Validation successful!
```

**[Narration - explain each check]**
"All 6 checks passed! This means:
- The baseline state is valid ✓
- Tests can be added ✓
- Tests correctly detect missing implementation ✓
- Solution can be added ✓
- Solution compiles ✓
- Solution passes all tests ✓

This confirms our task is properly set up for HUD!"

---

## Part 11: Generate HUD Configuration (29:00-30:00)

**[Narration]**
"Now let's generate the HUD configuration JSON. This file tells HUD how to run your task."

### 11.1 Generate JSON

**[Screen: Terminal]**

```bash
# Generate local-hud.json
uv run utils/imagectl3.py verilog_ -j --ids rc5_ca_keygen
```

**[Show success message]**

### 11.2 Verify JSON

**[Screen: VS Code - open local-hud.json]**

```bash
# View the generated config
cat local-hud.json
```

**[Show key parts of the JSON]**

```json
{
  "id": "rc5_ca_keygen",
  "prompt": "Implement RC5 encryption...",
  "setup_tool": {
    "name": "setup_problem",
    "arguments": {"problem_id": "rc5_ca_keygen"}
  },
  "evaluate_tool": {
    "name": "grade_problem",
    "arguments": {"problem_id": "rc5_ca_keygen"}
  },
  "mcp_config": {
    "local": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "verilog_rc5_ca_keygen"]
    }
  }
}
```

**[Narration]**
"This JSON file tells HUD which Docker image to use and how to setup and grade the problem."

---

## Part 12: Run Pass@10 Evaluation (30:00-35:00)

**[Narration]**
"Finally, let's run a pass@10 evaluation. This runs 10 AI agents independently to see how many can solve the problem."

### 12.1 Set Up HUD Account

**[Screen: Browser - hud.ai]**

"You need a HUD account and API key. If you don't have one yet:
1. Go to hud.ai
2. Sign up
3. Go to settings and copy your API key"

**[Screen: Terminal]**

```bash
# Set your HUD API key
export HUD_API_KEY="your-api-key-here"

# Or persist it
uv run hud set HUD_API_KEY your-api-key-here
```

### 12.2 Run Evaluation

**[Screen: Terminal]**

```bash
# Run pass@10 evaluation with Claude Sonnet
uv run hud eval local-hud.json claude \
  --model claude-sonnet-4-20250514 \
  --max-steps 30 \
  --group-size 10 \
  -v
```

**[Narration - explain parameters]**
"Let me explain these parameters:
- `local-hud.json`: Our task configuration
- `claude`: Use Anthropic's Claude AI
- `--model claude-sonnet-4-20250514`: Specific model version
- `--max-steps 30`: Allow up to 30 tool calls per attempt
- `--group-size 10`: Run 10 independent attempts (pass@10)
- `-v`: Verbose output to see what's happening"

### 12.3 Monitor Progress

**[Show real-time output scrolling]**

```
🔧 Initializing evaluation...
📊 Loading task file…
Found 1 task, running with group-size 10…

Attempt 1/10: Setting up environment...
  → setup_problem(...)
  ✓ Environment ready
  → Agent reading spec...
  → Agent writing code...
  → grade_problem(...)
  ✅ Reward: 1.0 (100%)

Attempt 2/10: Setting up environment...
  → setup_problem(...)
  ✓ Environment ready
  → Agent reading spec...
  → Agent writing code...
  → grade_problem(...)
  ❌ Reward: 0.0 (0% - compilation error)

...

Final Results:
  Pass@10: 7/10 = 70%
  Average reward: 0.70
```

**[Narration]**
"Great! 7 out of 10 attempts succeeded. Let's look at the detailed traces."

### 12.4 View Detailed Traces

**[Screen: Browser - HUD dashboard at hud.ai]**

"You can see detailed traces of each attempt on the HUD dashboard. Let me click into one..."

**[Click on a successful trace]**
- Shows all tool calls (read_file, write, run_terminal_cmd)
- Shows agent reasoning at each step
- Shows the final code
- Shows test results

**[Click on a failed trace]**
- Shows where it went wrong
- Shows compilation errors or test failures
- Shows what the agent tried

---

## Part 13: Interpreting Results (35:00-37:00)

**[Narration]**
"Let's interpret what pass@10 = 70% means for this task."

### 13.1 What Pass@10 Tells Us

**[Screen: Show summary statistics]**

"A 70% pass rate means:
- ✅ The task is solvable by AI (not too hard)
- ✅ The task has some challenge (not too easy)
- ✅ Good candidate for RL training

**Ideal ranges:**
- 20-40%: Hard task, good for advanced RL
- 40-70%: Medium task, good for general RL
- 70-90%: Easier task, good for initial training
- 90%+: Too easy, agent might memorize solution"

### 13.2 Analyzing Failures

**[Screen: HUD dashboard - click into failed traces]**

"Let's see why 3 attempts failed..."

**[Show examples of failures]**

Common failure patterns:
1. **Timing issues**: Agent didn't wait long enough for encryption to complete
2. **Algorithm bugs**: Incorrect RC5 round implementation
3. **Interface mismatch**: Wrong port names or bit widths
4. **FSM bugs**: State machine logic errors
5. **Key generation**: LFSR implementation mistakes

### 13.3 Improving the Task (Optional)

**[Narration]**
"If your pass rate is too high or too low, you can adjust:

**To make it harder:**
- Make spec less detailed
- Remove or reduce hints
- Increase complexity (more rounds, larger width)
- Add more edge cases to tests

**To make it easier:**
- Add more implementation guidance
- Provide more hints
- Simplify the algorithm
- Add partial credit tests"

---

## Part 14: Wrap-Up and Next Steps (37:00-40:00)

**[Screen: Slide with checklist or summary view]**

**[Narration]**
"Excellent! Let's recap what we accomplished today."

### 14.1 What We Did

**[Show checklist with checkmarks]**

"We successfully:
✅ Created a Verilog problem directory from scratch in VS Code
✅ Added specification, prompts, tests, and golden solution
✅ Initialized Git repository
✅ Created three branches (baseline, test, golden)
✅ Pushed all branches to GitHub
✅ Integrated with HUD framework
✅ Built Docker image
✅ Validated the task setup (all 6 checks passed!)
✅ Generated HUD configuration JSON
✅ Ran pass@10 evaluation
✅ Got 70% pass rate - perfect difficulty level!"

### 14.2 Next Steps

**[Show action items]**

"Here's what you can do next:

1. **Run more evaluations**: Try pass@100 for better statistics
2. **Test different models**: Compare Claude vs GPT-4 vs other models
3. **Iterate on difficulty**: Adjust based on pass rates
4. **Add more problems**: Repeat this workflow for other problems
5. **Share with HUD team**: Submit for production use
6. **RL training**: Use for reinforcement learning experiments"

### 14.3 Key Takeaways

**[Highlight important points]**

"Remember these key points:
- **3 branches are critical**: baseline (empty), test (with tests), golden (with solution)
- **Validation must pass**: All 6 checks must succeed
- **Test on baseline must fail**: This ensures tests actually check something
- **Increment ENV random**: Force Docker rebuild when you change repos
- **Target 40-70% pass rate**: Good challenge level for RL training"

### 14.4 Resources

**[Show links on screen]**

- **HUD Documentation**: docs.hud.ai
- **Framework Repo**: github.com/YOUR_ORG/verilog-template
- **Your Problem Repo**: github.com/YOUR_USERNAME/verilog-problems
- **HUD Dashboard**: hud.ai
- **Get Help**: HUD Slack channel or support@hud.ai

**[Narration]**
"Thank you for watching! You now know how to create and validate Verilog problems for HUD. If you have questions, reach out to the HUD team on Slack or via email. Happy testing!"

**[End screen with contact info]**

---

## Appendix: Common Issues and Troubleshooting

### Issue 1: Validation Fails - "Test patch doesn't fail tests"

**Cause**: Tests are passing even without implementation (probably checking wrong things)

**Fix**:
```bash
# Manually test baseline
git checkout rc5_ca_keygen_baseline
git checkout rc5_ca_keygen_test -- tests/
pytest tests/ -v  # Should FAIL
```

### Issue 2: Validation Fails - "Golden patch doesn't pass tests"

**Cause**: Solution has bugs

**Fix**:
```bash
# Test golden + tests together
git checkout rc5_ca_keygen_golden
git checkout rc5_ca_keygen_test -- tests/
pytest tests/ -v  # Should PASS
```

### Issue 3: Docker Build Fails - "Cannot clone repository"

**Cause**: Repository URL is wrong or private without token

**Fix**:
- Verify repo URL: `git ls-remote https://github.com/YOUR_USERNAME/verilog-problems.git`
- Make repo public, or add GitHub token to Dockerfile

### Issue 4: Tests Don't Run - "ModuleNotFoundError"

**Cause**: Missing dependencies in pyproject.toml

**Fix**: Add to your GitHub repo's pyproject.toml:
```toml
[project]
name = "verilog-problems"
dependencies = [
    "cocotb>=1.8.0",
    "pytest>=7.0.0",
    "cocotb-test>=0.2.4",
]
```

---

## Appendix: Quick Command Reference

### Git Workflow

```bash
# Initialize repository
git init
git add .
git commit -m "Initial commit with harness structure"

# Create baseline branch (remove harness/)
git checkout -b rc5_ca_keygen_baseline
rm -rf harness/
git add -A
git commit -m "Baseline: remove harness"

# Create test branch (from master, extract tests)
git checkout master
git checkout -b rc5_ca_keygen_test
mkdir -p tests
cp harness/test/test_rc5_ca_keygen.py tests/  # ONE file with cocotb + pytest wrapper
rm -rf harness/
git add -A
git commit -m "Test branch: add hidden tests"

# Create golden branch (from master, extract solution)
git checkout master
git checkout -b rc5_ca_keygen_golden
cp harness/patch/sources/* sources/
rm -rf harness/
git add -A
git commit -m "Golden branch: complete working solution"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/verilog-problems.git
git push -u origin rc5_ca_keygen_baseline
git push -u origin rc5_ca_keygen_test
git push -u origin rc5_ca_keygen_golden
```

### HUD Framework Commands

```bash
# Build Docker image
uv run utils/imagectl3.py verilog_ -b --ids rc5_ca_keygen

# Validate task
uv run utils/imagectl3.py verilog_ -v --ids rc5_ca_keygen

# Generate HUD JSON
uv run utils/imagectl3.py verilog_ -j --ids rc5_ca_keygen

# Run evaluation (pass@10)
uv run hud eval local-hud.json claude \
  --model claude-sonnet-4-20250514 \
  --group-size 10 \
  --max-steps 30 \
  -v
```

### Verification Commands

```bash
# Test that baseline fails
git checkout rc5_ca_keygen_baseline
git checkout rc5_ca_keygen_test -- tests/
pytest tests/ -v  # Should FAIL

# Test that golden passes
git checkout rc5_ca_keygen_golden
git checkout rc5_ca_keygen_test -- tests/
pytest tests/ -v  # Should PASS

# Check Docker patches
docker run --rm verilog_rc5_ca_keygen ls -la /home/root/*.patch

# View branches
git branch -a
git ls-remote --heads origin
```

