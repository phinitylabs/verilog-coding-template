# Local Repository Workflow (No Push Access Needed)

**For contractors who don't have push access to the example-verilog-codebase repository.**

---

## 🎯 Strategy: Use Local Branches Only

Instead of pushing to remote, we'll:
1. Create a **local copy** of the repository
2. Create all branches **locally**
3. Point Dockerfile to the **local path** instead of GitHub URL
4. Everything works the same way!

---

## Part 1: Create Local Repository

```bash
# Create a local repository from scratch
cd ~/Documents/GitHub
mkdir my-verilog-problems
cd my-verilog-problems

# Initialize git
git init
git config user.email "you@example.com"
git config user.name "Your Name"

# Create initial structure
mkdir -p rtl harness docs tb tests

# Create a basic README
cat > README.md << 'EOF'
# My Verilog Problems

Local repository for verilog evaluation problems.
EOF

# Create pyproject.toml
cat > pyproject.toml << 'EOF'
[project]
name = "my-verilog-problems"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "cocotb>=1.8.0",
    "pytest>=7.0.0",
    "cocotb-test>=0.2.4",
]
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
sim_build/
*.vcd
*.vvp
.pytest_cache/
EOF

# Initial commit
git add .
git commit -m "Initial commit"
git branch -M main
```

---

## Part 2: Add RC5 Problem to Local Repo

### Create Complete Solution Branch

```bash
cd ~/Documents/GitHub/my-verilog-problems

# Create branch with complete solution
git checkout -b rc5_bug_fix

# Copy RC5 files
cp ~/Documents/GitHub/rc5_pass-k/problem2_rc5_bug_fix/rtl/rc5_enc_16bit.sv rtl/
cp ~/Documents/GitHub/rc5_pass-k/problem2_rc5_bug_fix/harness/test_rc5_enc_16bit.py harness/
cp ~/Documents/GitHub/rc5_pass-k/problem2_rc5_bug_fix/harness/rc5_enc_16bit_golden.sv harness/
cp ~/Documents/GitHub/rc5_pass-k/problem2_rc5_bug_fix/docs/Specification.md docs/
cp ~/Documents/GitHub/rc5_pass-k/problem2_rc5_bug_fix/prompt.txt .
cp ~/Documents/GitHub/rc5_pass-k/problem2_rc5_bug_fix/tb/tb_rc5_enc.sv tb/

# Add pytest runner to test file (if not already there)
# See RC5_VALIDATION_CHECKLIST.md for the function to add

# Commit
git add .
git commit -m "Add rc5_bug_fix problem with complete solution"
```

### Create Baseline Branch

```bash
# Create baseline
git checkout -b rc5_bug_fix_baseline

# Remove hidden files
rm harness/test_rc5_enc_16bit.py
rm harness/rc5_enc_16bit_golden.sv
rmdir harness 2>/dev/null || true

# Commit
git add .
git commit -m "RC5 baseline: Buggy implementation only"
```

### Create Test Branch

```bash
# Create test branch
git checkout -b rc5_bug_fix_test

# Restore test files from complete branch
mkdir -p harness
git checkout rc5_bug_fix -- harness/test_rc5_enc_16bit.py
git checkout rc5_bug_fix -- harness/rc5_enc_16bit_golden.sv

# Commit
git add harness/
git commit -m "RC5 test: Add hidden tests"
```

### Create Golden Branch

```bash
# Go back to baseline
git checkout rc5_bug_fix_baseline

# Create golden
git checkout -b rc5_bug_fix_golden

# Get golden solution and replace buggy rtl
mkdir -p harness
git checkout rc5_bug_fix -- harness/rc5_enc_16bit_golden.sv
cp harness/rc5_enc_16bit_golden.sv rtl/rc5_enc_16bit.sv
rm -rf harness

# Commit
git add .
git commit -m "RC5 golden: Fixed implementation"
```

### Verify Branches

```bash
# List all branches (all local, no remotes)
git branch

# Should show:
#   main
#   rc5_bug_fix
#   rc5_bug_fix_baseline
#   rc5_bug_fix_test
#   rc5_bug_fix_golden
```

---

## Part 3: Update Dockerfile to Use Local Repository

**This is the key change!**

```bash
cd ~/Documents/GitHub/verilog-template
```

**Edit `Dockerfile` around line 109:**

```dockerfile
# BEFORE (GitHub URL):
# ENV random=random5
# RUN git clone https://github.com/hud-evals/example-verilog-codebase /home/ubuntu/example-verilog-codebase

# AFTER (Local path):
ENV random=random6
# Copy local repository instead of cloning
COPY --chown=ubuntu:ubuntu /path/to/your/my-verilog-problems /home/ubuntu/example-verilog-codebase

WORKDIR /home/ubuntu/example-verilog-codebase
```

**⚠️ Wait! COPY doesn't work with absolute paths outside Docker context.**

### Better Approach: Create a Symlink or Use Different Method

**Option A: Copy local repo into Docker build context**

```bash
# In verilog-template directory
mkdir -p local-repos
cp -r ~/Documents/GitHub/my-verilog-problems local-repos/

# Then in Dockerfile:
COPY --chown=ubuntu:ubuntu local-repos/my-verilog-problems /home/ubuntu/example-verilog-codebase
```

**Option B: Use git bundle (Recommended)**

```bash
# Create a git bundle from your local repo
cd ~/Documents/GitHub/my-verilog-problems
git bundle create ~/Documents/GitHub/verilog-template/repo.bundle --all

# Then in Dockerfile:
COPY repo.bundle /tmp/repo.bundle
RUN cd /home/ubuntu && \
    git clone /tmp/repo.bundle example-verilog-codebase && \
    rm /tmp/repo.bundle
```

**Option C: Best for Demo - Mount Volume**

For local testing/demo, use Docker volume mount:

```bash
# Build with local repo path as build arg
docker build \
  --build-arg REPO_PATH=/path/to/my-verilog-problems \
  -t test_verilog_rc5_bug_fix \
  .
```

---

## Part 4: Simplest Solution for Demo Video

**Recommended approach for your video:**

### 1. Create Local Repo with All Branches

```bash
cd ~/Documents/GitHub
mkdir verilog-problems-local
cd verilog-problems-local
git init

# Add all RC5 files to main
# ... (as shown above)

# Create all 3 branches locally
# ... (as shown above)
```

### 2. Modify Dockerfile to Copy Local Repo

```bash
cd ~/Documents/GitHub/verilog-template

# Create local-repos directory in build context
mkdir -p local-repos

# Copy your local repo into build context
cp -r ~/Documents/GitHub/verilog-problems-local local-repos/problems
```

**Update Dockerfile (around line 99-111):**

```dockerfile
# ========================= PROJECT SETUP =========================
# Using local repository

ENV random=random6

# Copy local repository into container
COPY --chown=ubuntu:ubuntu local-repos/problems /home/ubuntu/example-verilog-codebase

WORKDIR /home/ubuntu/example-verilog-codebase

# Checkout branches for testing (baseline, test, golden)
ARG TEST_BRANCH
ARG GOLDEN_BRANCH
ARG BASELINE_BRANCH
RUN git checkout $BASELINE_BRANCH && \
    git checkout $TEST_BRANCH && \
    git checkout $GOLDEN_BRANCH && \
    git checkout $BASELINE_BRANCH

# Generate patches for grading
USER root
RUN mkdir -p /home/root && \
    sudo -u ubuntu git diff $BASELINE_BRANCH $TEST_BRANCH > /home/root/test.patch && \
    sudo -u ubuntu git diff $BASELINE_BRANCH $GOLDEN_BRANCH > /home/root/golden.patch
USER ubuntu
```

### 3. Update grading_runner.py Path

**Edit `src/hud_controller/grading_runner.py` line 46:**

```python
# Keep the same - works with any repo name
self.original_repo_path = "/home/ubuntu/example-verilog-codebase"
```

---

## Part 5: Demo Video Script (Updated)

**Replace the "push to remote" sections with:**

```bash
# After creating each branch
git add .
git commit -m "Branch created"

# NO PUSH NEEDED - all local!
echo "✓ Branch created locally"
```

**Explain on camera:**

"We're working entirely with a local repository. All branches are local - no need to push to GitHub. The Docker build will copy this local repo, so everything works the same way."

---

## Part 6: Build and Validate (Same as Before)

```bash
cd ~/Documents/GitHub/verilog-template

# Build
uv run utils/imagectl3.py test_verilog_ -b --ids rc5_bug_fix

# Validate
uv run utils/imagectl3.py test_verilog_ -v --ids rc5_bug_fix

# Generate JSON
uv run utils/imagectl3.py test_verilog_ -j
```

Everything else works exactly the same!

---

## Alternative: Use Existing example-verilog-codebase Locally

If you already have a clone of `example-verilog-codebase`:

```bash
# Clone the existing repo
cd ~/Documents/GitHub
git clone https://github.com/hud-evals/example-verilog-codebase
cd example-verilog-codebase

# Create your branches LOCALLY (don't push)
git checkout -b rc5_bug_fix
# ... add files ...
git commit -m "Add RC5"

# Create other branches locally
# ... (same as before)

# Then in verilog-template:
cd ~/Documents/GitHub/verilog-template
mkdir -p local-repos
cp -r ~/Documents/GitHub/example-verilog-codebase local-repos/

# Update Dockerfile to use COPY instead of git clone
```

---

## Summary: What Changed

### Old Way (Needs Push Access):
```dockerfile
git clone https://github.com/hud-evals/example-verilog-codebase
```

### New Way (Local Only):
```dockerfile
COPY local-repos/your-repo-name /home/ubuntu/example-verilog-codebase
```

### In Your Workflow:
1. ✅ Create local repo with all files
2. ✅ Create all branches locally
3. ✅ Copy local repo into Docker build context
4. ✅ Update Dockerfile to COPY instead of clone
5. ✅ Build and validate normally

**No remote push needed!** 🎉

---

## For Your Demo Video

**Updated narration:**

"In this demo, I'm working with a local repository since I don't have push access to the main repo. This is actually more common for contractors! The process is the same - we create all the branches locally, then copy the local repo into the Docker build context instead of cloning from GitHub."

**Show on camera:**
- Local git branches (no origin/remote)
- Copying repo into build context
- Same validation results

**Benefits:**
- More realistic for contractors
- No GitHub access needed
- Faster iteration (no network)
- Same end result!

