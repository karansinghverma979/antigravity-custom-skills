---
name: hook-master
description: >-
  Antigravity lifecycle hook architect, security gate generator, and automation governor.
  Use whenever configuring hooks.json, setting up PreToolUse/PostToolUse safety checks,
  intercepting tool arguments, forcing test passes before task completion, or automating linters on tool actions.
---

# 🪝 Hook Master: Antigravity Lifecycle Hook Suite

Use this skill when designing, authoring, testing, or debugging event-driven lifecycle hooks (`hooks.json`) in Antigravity.

---

## 🏛️ Lifecycle Hooks Architecture

Antigravity executes hook handlers at specific checkpoints in the agent execution loop:
1. **`PreToolUse`**: Intercept tool calls, validate commands, block unsafe actions (`deny`), or rewrite arguments (`overwrite`).
2. **`PostToolUse`**: Trigger post-action linters, test suites, or auto-formatters.
3. **`PreInvocation` / `PostInvocation`**: Inject dynamic prompt context or force continuation.
4. **`Stop`**: Prevent the agent from stopping prematurely if background jobs or builds are failing.

For full input/output payload contracts:
- [Hook Lifecycle Contracts Reference](./references/hook_contracts.md)

---

## 🔄 Hook Creation Workflow

### Step 1: Define Event & Interception Goal
Determine where in the lifecycle the check must happen:
- Safety gate on commands $\rightarrow$ `PreToolUse` with `matcher: "run_command"`.
- Quality gate before final answer $\rightarrow$ `Stop` with `decision: "continue"`.

### Step 2: Automated Scaffolding
Generate a handler script and `hooks.json` configuration:

```bash
python ~/.gemini/antigravity-cli/skills/hook-master/scripts/generate_hook.py <target_dir> <hook_name> <event_type>
```

### Step 3: Implement & Test Handler
- Ensure the handler reads JSON from `sys.stdin` and outputs valid JSON to `sys.stdout`.
- Verify the timeout and Windows executable paths.
