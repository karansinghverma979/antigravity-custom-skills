---
name: swarm-orchestrator
description: >-
  Multi-agent swarm supervisor, parallel subagent dispatcher, and state coordinator.
  Use whenever breaking complex coding tasks into parallel workstreams, dispatching specialized subagents
  (Researcher, Architect, Implementer, Sentinel) via invoke_subagent, coordinating cross-agent handoffs,
  or managing subagent lifecycle without context pollution.
---

# 🔀 Swarm Orchestrator: Multi-Agent Parallel Engineering Suite

Use this skill when decomposing large architecture and implementation tasks across specialized subagents in Antigravity.

---

## 🏛️ Swarm Architecture & Roles

Antigravity supports concurrent subagent spawning via `invoke_subagent` and dynamic definition via `define_subagent`.

For role definitions and handoff specifications:
- [Specialized Subagent Archetypes](./references/swarm_roles.md)
- [Handoff & Reconciliation Protocol](./references/handoff_protocol.md)

---

## 🔄 Swarm Execution Workflow

### Step 1: Decompose into Isolated Streams
Identify tasks that can execute in parallel:
- **Stream A**: Survey dependencies & docs (Assigned to `research` subagent).
- **Stream B**: Design data contracts & schemas (Assigned to `architect` subagent).

### Step 2: Concurrent Dispatch
Invoke all subagents in a single `invoke_subagent` tool call with explicit, scoped prompts:

```javascript
invoke_subagent({
  Subagents: [
    { TypeName: "research", Role: "Schema Inspector", Prompt: "Extract all database tables in /db.", Model: "inherit" },
    { TypeName: "research", Role: "Route Auditor", Prompt: "List all unauthenticated routes in /api.", Model: "inherit" }
  ]
});
```

### Step 3: Reactive State Consolidation
- Stop calling tools to allow subagents to execute in background.
- Upon automatic wakeup, synthesize findings and direct implementation.
- Hand off final diffs to `code-sentinel` for quality review.
