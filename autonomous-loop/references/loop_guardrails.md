# Autonomous Loop Guardrails & Error Healing Framework

The autonomous repair loop enables closed-loop iteration (`Execute -> Catch Error -> Apply Diff -> Re-verify`) without human intervention on trivial syntax/logic bugs.

---

## 1. Safety Guardrails & Bounds

1. **Max Iteration Budget**: Hard limit of **5 to 8 iterations** per task. If tests still fail after 8 passes, halt and report diagnostics to prevent runaway token burn.
2. **Automated Rollback**: If a patch causes new compilation failures or test regressions, automatically `git checkout -- <file>` to return to the last known green baseline before trying a different approach.
3. **AST / Regex Error Targeting**: Parse the exact file and line number from compiler or test stack traces instead of modifying unrelated code.

---

## 2. The Healing State Machine

```
┌────────────────────────────────────────────────────────┐
│  1. Execute Test / Build Command                       │
│     (pytest, npm test, cargo check, python script)     │
├──────────────────────────┬─────────────────────────────┤
│  2. If Exit Code == 0    │  3. If Exit Code != 0       │
│     • Commit green state │     • Parse stack trace     │
│     • Terminate loop ✅  │     • Formulate minimal fix │
│                          │     • Apply code edit       │
│                          │     • Increment iteration   │
│                          │     • Repeat Loop 🔄        │
└──────────────────────────┴─────────────────────────────┘
```
