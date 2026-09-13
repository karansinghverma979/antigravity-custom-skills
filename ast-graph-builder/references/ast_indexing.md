# AST Indexing & Token-Free Codebase Mapping Guide

Dumping entire source files into LLM context windows to understand project architecture wastes tokens and degrades reasoning. Abstract Syntax Tree (AST) indexing extracts symbols, signatures, and call hierarchies in milliseconds with zero LLM token cost.

---

## 1. Core Principles of AST Pre-Processing

```
┌────────────────────────────────────────────────────────┐
│ Raw Codebase (50+ Files, 100k Lines)                   │
└──────────────────────────┬─────────────────────────────┘
                           │ [Local Python AST Parser <50ms]
                           ▼
┌────────────────────────────────────────────────────────┐
│ Compact Symbol Index (<500 tokens)                     │
│ • File Paths & Line Ranges                             │
│ • Class Signatures & Method Names                      │
│ • Cross-File Import Graphs                             │
└──────────────────────────┬─────────────────────────────┘
                           │ [Targeted view_file on 1-2 lines]
                           ▼
┌────────────────────────────────────────────────────────┐
│ Surgical, High-Precision Code Modifications            │
└────────────────────────────────────────────────────────┘
```

---

## 2. When to Use AST Graphing

1. **New Repo Onboarding**: Mapping the entrypoints and domain models of an unfamiliar repository.
2. **Refactoring Blast Radius**: Checking which other files import a function before renaming or altering its signature.
3. **Circular Dependency Detection**: Tracing import chains across modules.
