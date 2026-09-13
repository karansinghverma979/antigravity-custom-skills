# High-Recall Trigger Engineering Guide

The `description` field in YAML frontmatter is the primary signal used by the LLM system to decide whether to activate a skill. If the description is too narrow, generic, or passive, the model will **undertrigger** and fail to activate the skill when needed.

---

## 1. Anatomy of an Effective Trigger Description

A high-recall description consists of 4 vital components:

```
[Role/Capability Definition] + [Core Procedures] + [Explicit Trigger Keywords] + [Anti-Undertriggering Catch-all]
```

### Example Comparison:

| ❌ Weak / Passive Description | ✅ High-Recall / Robust Description |
| :--- | :--- |
| `description: Manage database tables.` | `description: >-`<br>&nbsp;&nbsp;`Comprehensive database optimizer, schema inspector, and query tuner.`<br>&nbsp;&nbsp;`Use whenever creating tables, modifying migrations, tuning slow queries,`<br>&nbsp;&nbsp;`or inspecting SQLite/Postgres schemas, even if the user only asks to "fix this query."` |

---

## 2. Best Practices for Formulating Triggers

1. **Third-Person Imperative**: Always frame from the system router's perspective:
   - *"Use this skill when the user..."*
   - *"Activate when..."*
2. **Explicit Keyword Ingestion**:
   List variations, acronyms, related file extensions, and common slang:
   - *Example*: `"Trigger on mentions of: .sql, sqlite, postgres, db migrate, schema drift, slow index."`
3. **Intent Fallbacks (The "Even If" Pattern)**:
   Add a defensive clause targeting shorthand or indirect prompts:
   - *"Use when inspecting network traffic, debugging 500 errors, or analyzing API latency, even if the user does not explicitly ask for a diagnostic run."*
4. **Boundary Clarity (Negative Guardrails)**:
   If a skill could collide with another skill, state what it should NOT handle:
   - *"Do not use for general frontend styling — use modern-web-guidance instead."*

---

## 3. Description Length Budget

- **Target**: 30 to 80 words.
- **Hard Limit**: Keep under 120 words to avoid occupying unnecessary system prompt tokens.
