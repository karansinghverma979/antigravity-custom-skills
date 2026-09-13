---
name: skill-forge
description: >-
  Architectural designer, validator, and builder for custom Antigravity skills.
  Use whenever creating a new skill, auditing or refactoring existing skills,
  optimizing trigger descriptions to prevent undertriggering, or validating skill directory
  structure against official Antigravity standards.
---

# 🛠️ Skill Forge: Antigravity Skill Builder & Governor

Use this skill when designing, authoring, auditing, or optimizing custom skills for Google Antigravity (AGY).

---

## 🏛️ Core Principles & Official Specifications

Skills in Antigravity follow a strict **Progressive Disclosure** architecture:
1. **Tier 1 (Metadata)**: `name` & `description` in YAML frontmatter. Must be concise (~50–100 words), high-recall, and written in 3rd person.
2. **Tier 2 (Core Runbook)**: `SKILL.md` body. Must stay under **500 lines**. Provides actionable step-by-step procedures.
3. **Tier 3 (Deep Resources)**: Detailed documentation goes into `./references/`, repetitive deterministic commands into `./scripts/`, and templates into `./resources/`.

For complete architectural patterns and trigger optimization guidelines:
- [Antigravity Skill Standards](./references/agy_standards.md)
- [High-Recall Trigger Engineering Guide](./references/trigger_engineering.md)

---

## 🔄 End-to-End Skill Creation Workflow

### Step 1: Raw Intent Extraction & Scope Definition
Extract the core objective from the user's prompt or ongoing conversation:
1. **Capability**: What concrete procedure, API, tool, or runbook should the agent learn?
2. **Triggers**: What phrases, file extensions, keywords, or error codes should activate this skill?
3. **Guardrails**: What should this skill *not* handle? (Prevent overlap with other skills).

### Step 2: Directory & File Scaffolding
Create the standard directory layout inside your target skills root (e.g. `~/.gemini/antigravity-cli/skills/<skill-name>/` or `.agents/skills/<skill-name>/`):

```text
skills/<skill-name>/
├── SKILL.md
├── references/
└── scripts/
```

### Step 3: Authoring `SKILL.md`
- **Frontmatter**: Ensure valid YAML with `name` (lowercase, hyphenated) and `description` (action-oriented with explicit keywords).
- **Imperative Voice**: Write crisp, direct instructions.
- **Progressive Links**: Move reference tables, large schemas, or extensive manual text into `references/<doc>.md` and link relatively.

### Step 4: Verification & Integrity Check
Run the native validator script on the created skill:

```bash
python ~/.gemini/antigravity-cli/skills/skill-forge/scripts/validate_skill.py <path-to-skill-directory>
```

---

## ⚡ Execution Directives
- **Zero Pollution**: Ensure skills never contradict `GEMINI.md` or pollute global state.
- **Windows Invariant**: Helper scripts in `scripts/` must be UTF-8 safe and handle Windows paths properly.
