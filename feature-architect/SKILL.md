---
name: feature-architect
description: >-
  Systematic feature designer, token-efficient codebase explorer, and phased implementation governor.
  Use whenever building new features, implementing complex architectural modules, planning multi-step code changes,
  or refactoring system components, even if the user just asks to "add this feature" or "build a module."
---

# 🚀 Feature Architect: Systematic Feature Engineering Suite

Use this skill when designing, scoping, and implementing complex software features with zero speculative bloat and maximum context grounding.

---

## 🏛️ Core Principles & Token Efficiency

To eliminate hallucinations and avoid context exhaustion, Feature Architect enforces a strict **4-Stage Execution Loop**:

```
┌────────────────────────────────────────────────────────┐
│ 1. 🔍 Grounded Exploration (Targeted ripgrep / view)   │
│ 2. 🪝 3-Point Pre-Execution Contract (Scope & Risks)   │
│ 3. 🧩 Phased Vertical Slice Implementation             │
│ 4. 🛡️ Verification & Sentinel Review (Unit tests/diff)  │
└────────────────────────────────────────────────────────┘
```

For detailed guides:
- [Grounded Exploration Strategy](./references/grounded_exploration.md)
- [Phased Vertical Slice Templates](./references/phase_templates.md)

---

## 🔄 The 4-Stage Feature Workflow

### Stage 1: Grounded Codebase Exploration
- Use `grep_search` and targeted `view_file` to inspect existing patterns, data models, and error handlers.
- **Never guess** method signatures or external dependencies without verifying in the working tree.

### Stage 2: Socratic 3-Point Contract
Present the standard Pre-Execution 3-Point Alignment:
1. **🎯 Target Scope**: Exact files, functions, and schemas being altered.
2. **🧠 Translated Objective**: Precise technical goal.
3. **⚡ Action Plan & Pitfalls**: Phased breakdown and explicit risk analysis.

### Stage 3: Phased Vertical Slice Implementation
- Implement from innermost contract to outermost wiring:
  - **Slice 1**: Data models, schemas, types.
  - **Slice 2**: Core business logic & state transitions.
  - **Slice 3**: API endpoints, CLI dispatchers, and UI components.

### Stage 4: Automated Verification & Review
Run local feature sanity checks:

```bash
python ~/.gemini/antigravity-cli/skills/feature-architect/scripts/verify_feature.py <target_directory>
```

Complete with a `code-sentinel` review pass to ensure zero silent failures or over-engineering.
