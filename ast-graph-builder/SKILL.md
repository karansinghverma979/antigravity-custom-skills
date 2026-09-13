---
name: ast-graph-builder
description: >-
  Ultra-fast Abstract Syntax Tree (AST) dependency graph generator and zero-token codebase mapper.
  Use whenever analyzing new codebases, mapping cross-file imports and class/method hierarchies,
  calculating refactoring blast radius, or indexing Python/JS symbols without reading entire files into context.
---

# ⚡ AST Graph Builder: Zero-Token Codebase Intelligence Suite

Inspired by Grok-Build and modern language server engines, this skill enables instant, token-free mapping of codebases using Abstract Syntax Tree (AST) parsers.

---

## 🏛️ Core Philosophy

Never dump multi-thousand line files into an LLM context window to find where a function or class lives.

For indexing methodology:
- [AST Indexing & Blast Radius Guide](./references/ast_indexing.md)

---

## 🔄 Quickstart & Usage

Run the bundled AST generator on any project repository:

```bash
python ~/.gemini/antigravity-cli/skills/ast-graph-builder/scripts/generate_ast_graph.py <project_directory>
```

### Output:
- Instant tree of all classes, line numbers, attached methods, and top-level functions across files in <50ms.
- Use the line coordinates to execute targeted `view_file` calls with exact `StartLine` and `EndLine` ranges.
