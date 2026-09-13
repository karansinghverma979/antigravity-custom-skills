# Antigravity Skill Architectural Standards

This reference documents the official design patterns, directory hierarchies, and technical constraints for building skills in the Google Antigravity (AGY) ecosystem.

---

## 1. Skill Directory Anatomy

Every skill is a self-contained directory containing instructions, optional scripts, and modular reference docs:

```text
skills/<skill-name>/
├── SKILL.md                 # REQUIRED: Primary instruction entrypoint with YAML frontmatter
├── scripts/                 # OPTIONAL: Executable helper scripts for deterministic/repetitive tasks
├── references/              # OPTIONAL: Modular, progressive deep-dive documentation
├── examples/                # OPTIONAL: Sample code, configs, or reference outputs
└── resources/               # OPTIONAL: Static assets, data templates, or schemas
```

---

## 2. Progressive Disclosure Hierarchy

To keep token usage minimal and context focused, skills operate on a 3-tier progressive disclosure model:

| Level | Component | Loading Behavior | Token Budget |
| :--- | :--- | :--- | :--- |
| **Tier 1** | `name` & `description` (Frontmatter) | Injected into System Prompt unconditionally. | ~50–100 words |
| **Tier 2** | `SKILL.md` Body | Injected into context ONLY when triggered by user/model. | <500 lines (<2500 tokens) |
| **Tier 3** | `references/` & `scripts/` | Read on-demand or executed without loading into prompt. | Unlimited |

### Rules for Progressive Hierarchy:
1. **Never dump complete manuals into `SKILL.md`**: Put comprehensive API specs, deep SQL schemas, or reference manuals into `references/<topic>.md`.
2. **Link with Relative Paths**: Always link reference files from `SKILL.md` using standard markdown links: `[Spec Doc](./references/spec.md)`.
3. **Table of Contents**: For any reference file exceeding 250 lines, include a quick Table of Contents at the top.

---

## 3. YAML Frontmatter Specification

`SKILL.md` **must** begin with a clean YAML frontmatter block:

```markdown
---
name: skill-name
description: >-
  Action-oriented, high-recall description specifying WHAT the skill does and
  EXACTLY WHEN it must trigger.
---
```

### Frontmatter Fields:
- **`name`** (string, required): Lowercase, hyphen-separated identifier (e.g. `skill-forge`, `db-optimizer`). No spaces or special characters.
- **`description`** (string, required): The single most critical triggering vector. Must be written in 3rd person ("Use this skill when...").

---

## 4. Windows & Shell Execution Invariants

When writing helper scripts or terminal instructions for skills running on Windows:
1. **Path Handling**: Always use `pathlib.Path` in Python or handle backslashes cleanly.
2. **Encoding**: Force UTF-8 explicitly (`encoding="utf-8"`) on all file read/write operations to avoid Windows `cp1252` encoding errors.
3. **PowerShell Quoting**: When documenting CLI commands, ensure PowerShell string escaping rules are respected (avoid single-quote token splitting in nested subshells).
4. **Line Endings**: Normalize line endings to avoid CRLF diff pollution in Git repositories.
