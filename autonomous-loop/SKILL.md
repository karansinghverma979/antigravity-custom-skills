---
name: autonomous-loop
description: >-
  Goal-directed autonomous execution, continuous test-driven iteration, and self-healing loop.
  Use whenever running automated bug fixing, resolving compiler or test failures in a closed loop,
  iterating until all tests pass green, or performing unattended script repairs without asking for permission on trivial syntax fixes.
---

# ⚡ Autonomous Loop: Closed-Loop Test-Driven Healing Engine

Inspired by the Ralph Loop and Codex CLI autonomous architectures, this skill enables self-directed code repair and goal achievement through continuous execution feedback.

---

## 🏛️ Autonomous Loop Architecture

The loop operates on a strict **Execute $\rightarrow$ Inspect $\rightarrow$ Patch $\rightarrow$ Re-verify** state machine with a hard iteration budget (max 5–8 iterations) to prevent runaway token spend.

For safety boundaries and rollback protocols:
- [Loop Guardrails & Rollback Protocols](./references/loop_guardrails.md)

---

## 🔄 Autonomous Healing Workflow

### Step 1: Execute Target Test / Build Command
Run the runner script to capture clean structured outputs and extract failing file/line coordinates:

```bash
python ~/.gemini/antigravity-cli/skills/autonomous-loop/scripts/run_loop.py "pytest" <repo_path>
```

### Step 2: Parse Failure & Apply Minimal Targeted Patch
- Locate the exact file and line number identified by the runner.
- Inspect the logic and apply a minimal, non-breaking fix using `replace_file_content`.

### Step 3: Re-execute & Verify
- Re-run the command immediately.
- If exit code == 0 $\rightarrow$ Complete turn and report success.
- If new errors are introduced $\rightarrow$ Rollback the patch and try alternative logic.
- Stop when all tests pass or iteration limit is reached.
