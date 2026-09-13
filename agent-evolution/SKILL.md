---
name: agent-evolution
description: >-
  Autonomous self-improvement, trajectory reflection, and memory consolidation engine.
  Use whenever analyzing failed tool executions, extracting durable learnings from conversation transcripts,
  evolving SKILL.md instructions based on execution friction, or consolidating machine memory into learnings.md.
---

# 🧬 Agent Evolution: Closed-Loop Self-Improvement & Reflection Suite

Inspired by Nous Research's Hermes Agent and GEPA optimization loops, this skill enables continuous, closed-loop self-improvement of skills, prompts, and machine learnings without fine-tuning weights.

---

## 🏛️ Core Principles & Architecture

Self-evolution operates via **Reflective Text Optimization**:
1. **Harvest Trajectories**: Extract failure points, syntax crashes, and tool errors from `transcript.jsonl`.
2. **Diagnose Friction**: Identify *why* the failure happened (missing invariant, ambiguous prompt, wrong Windows path format).
3. **Targeted In-Place Mutation**:
   - Update `learnings.md` in-place for system invariants.
   - Mutate `SKILL.md` (or its `description:`) to prevent repeat failures.

For detailed methodology:
- [Reflective Evolution Framework](./references/reflective_evolution.md)
- [Memory Consolidation & In-Place Rules](./references/memory_consolidation.md)

---

## 🔄 Self-Evolution Workflow

### Step 1: Harvest Friction from Recent Trajectories
Run the trajectory harvester to find recent errors across session transcripts:

```bash
python ~/.gemini/antigravity-cli/skills/agent-evolution/scripts/harvest_trajectories.py
```

### Step 2: Extract Invariants & Consolidate
When a new tool quirk or OS invariant is discovered, consolidate it directly into `learnings.md`:

```bash
python ~/.gemini/antigravity-cli/skills/agent-evolution/scripts/consolidate_learnings.py "Windows PowerShell Traps" "Always force UTF-8 stream encoding on Python stdout."
```

### Step 3: Evolve Target Skills
- If a skill undertriggered, edit its `description:` in frontmatter to add high-recall keywords.
- Validate using `skill-forge` to ensure line budgets (<500 lines) and valid schemas are maintained.
