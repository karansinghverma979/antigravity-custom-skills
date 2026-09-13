# Grounded Codebase Exploration & Anti-Hallucination Guide

To prevent token exhaustion and hallucinated abstractions, never guess existing project patterns or load entire directories into context.

---

## 1. The Token-Optimized Exploration Funnel

Instead of dumping dozens of files into the prompt, follow a 3-step targeted exploration:

```
┌─────────────────────────────────────────────────────────┐
│ Step 1: Broad Pattern Sweep (ripgrep / grep_search)     │
│ Search exact identifiers, imports, error constants.     │
├────────────────────────────┬────────────────────────────┤
│ Step 2: Boundary Inspection│ view_file (StartLine/End)  │
│ Inspect ONLY the function  │ Target 20–50 lines around  │
│ or class contract.         │ the core execution path.   │
├────────────────────────────┴────────────────────────────┤
│ Step 3: Verify Invariants Before Modifying              │
│ Check imports, exports, and schema definitions.         │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Anti-Hallucination Invariants

1. **Verify Before Referencing**:
   Never import a module or invoke an API method without verifying its existence via `grep_search` or `view_file` first.
2. **Reuse Existing Patterns**:
   Match the repo's existing error handling, logging libraries, and naming conventions rather than introducing new dependencies.
3. **Fail Fast on Ambiguity**:
   If an interface signature or database schema is unclear, initiate a `/grill-me` alignment rather than guessing parameters.
