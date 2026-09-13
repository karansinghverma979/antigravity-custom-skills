# Antigravity Lifecycle Hooks Specification (`hooks.json`)

Hooks execute shell commands at deterministic checkpoints in the agent execution loop, exchanging protojson-encoded JSON over `stdin` and `stdout`.

---

## 1. Supported Lifecycle Events

| Event | When It Triggers | Matcher Target | Common Use Cases |
| :--- | :--- | :--- | :--- |
| **`PreToolUse`** | Right before a tool executes | Tool Name (e.g. `run_command`, `write_to_file`) | Safety gating (`ask`/`deny`), argument rewriting (`overwrite`). |
| **`PostToolUse`** | Right after tool execution completes | Tool Name | Auto-formatting, linting, metric tracking. |
| **`PreInvocation`** | Before model is called | N/A | Dynamic context injection (`injectSteps`). |
| **`PostInvocation`**| After tool calls finish | N/A | Forcing continuation (`force_continue`). |
| **`Stop`** | When agent finishes all steps | N/A | Preventing premature exit if tests/builds failed. |

---

## 2. Stdin / Stdout Contracts

### A. `PreToolUse`
- **Input (`stdin`)**:
  ```json
  {
    "toolCall": {
      "name": "run_command",
      "args": { "CommandLine": "rm -rf /" }
    },
    "stepIdx": 12,
    "conversationId": "..."
  }
  ```
- **Output (`stdout`)**:
  ```json
  {
    "decision": "deny",
    "reason": "Destructive command blocked by safety gate."
  }
  ```
  *(Valid decisions: `"allow"`, `"deny"`, `"ask"`, `"force_ask"`)*

### B. `Stop` Checkpoint (Prevent Premature Exit)
- **Input (`stdin`)**:
  ```json
  {
    "executionNum": 1,
    "terminationReason": "model_stop",
    "fullyIdle": true
  }
  ```
- **Output (`stdout`)**:
  ```json
  {
    "decision": "continue",
    "reason": "Linter failed. Fix syntax errors before completing turn."
  }
  ```

---

## 3. Windows Shell Execution Notes
- Hook commands on Windows are dispatched via `cmd.exe /c` or PowerShell.
- Always use absolute paths or paths relative to the directory containing `hooks.json`.
