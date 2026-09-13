# Specialized Subagent Roles & Archetypes

When orchestrating multi-agent workflows in Antigravity, decompose tasks into specialized subagent personas using `define_subagent` and `invoke_subagent`.

---

## 1. Core Swarm Archetypes

| Subagent Role | Type Name | Tool Groups | Primary Objective |
| :--- | :--- | :--- | :--- |
| **Codebase Researcher** | `research` | Read-only (grep, find, view, web) | Fast non-polluting code survey, dependency inspection, and documentation lookup. |
| **System Architect** | `architect` | Read + Subagent tools | Interface definition, API schema design, and dependency graph planning. |
| **Feature Implementer** | `self` / `worker` | Read + Write + Command | Isolated module coding, database migration execution, and unit test authoring. |
| **Quality Sentinel** | `sentinel` | Read-only + Diff analysis | Independent 4-pass code review, silent bug hunting, and security auditing. |

---

## 2. Invocation Pattern via `invoke_subagent`

```javascript
// Parallel subagent launch:
invoke_subagent({
  Subagents: [
    {
      TypeName: "research",
      Role: "Dependency Researcher",
      Prompt: "Analyze the database schema in /models and summarize all active Foreign Keys.",
      Model: "inherit"
    },
    {
      TypeName: "research",
      Role: "API Interface Surveyor",
      Prompt: "Inspect /routes and list all HTTP endpoints requiring authentication.",
      Model: "inherit"
    }
  ]
});
```
