# Multi-Agent Handoff & State Reconciliation Protocol

To prevent context exhaustion in multi-agent swarms, adhere to strict message boundaries between parent and child agents.

---

## 1. Zero-Polling & Reactive Wakeup Invariant

- When subagents are launched via `invoke_subagent`, the parent agent **MUST NOT** poll in a loop.
- The runtime automatically halts and re-activates the parent agent when subagents complete or send messages via `send_message`.

---

## 2. High-Density Return Schema

Subagents must return crisp, structured summaries rather than raw transcript dumps:

```markdown
### 🎯 Subagent Findings: [Role Name]
- **Status**: Completed ✅ / Blocked ⚠️
- **Key Discoveries / Mutations**:
  - `file/path.py`: Updated `handle_request` signature.
- **Critical Edge Cases**:
  - Found potential null pointer on empty payloads.
- **Recommended Next Move for Parent**:
  - Proceed with integrating `route.py`.
```
