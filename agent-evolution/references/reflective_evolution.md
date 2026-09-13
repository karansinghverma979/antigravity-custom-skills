# Reflective Skill Evolution & Trajectory Analysis Guide

Inspired by Nous Research's Hermes Agent and GEPA (Generative Error-driven Prompt Alignment), this reference defines the closed-loop optimization framework for evolving agent skills.

---

## 1. The Reflective Evolution Loop

Rather than fine-tuning neural network weights, text-level self-evolution optimizes the **procedural instructions** (`SKILL.md`), **trigger boundaries** (`description:`), and **in-context rules** based on real execution traces.

```
┌────────────────────────────────────────────────────────┐
│ 1. Collect Execution Trajectories (transcript.jsonl)   │
│    Filter tool errors, user corrections, retry loops.  │
├──────────────────────────┬─────────────────────────────┤
│ 2. Reflective Diagnosis   │ 3. Targeted Mutation        │
│    Analyze WHY it failed  │ Refine instructions/rules   │
│    (missing invariant,    │ to make failure impossible  │
│    poor formatting).      │ in future trajectories.     │
├──────────────────────────┴─────────────────────────────┤
│ 4. Validation & In-Place Update                        │
│    Verify syntax and progressive line budgets (<500).  │
└────────────────────────────────────────────────────────┘
```

---

## 2. Failure Mode Taxonomy

When analyzing trajectory friction, categorize into 3 distinct targets:

| Failure Mode | Diagnosis | Evolution Target |
| :--- | :--- | :--- |
| **Tool Undertriggering** | Model didn't activate the skill when it should have. | Expand `description:` in frontmatter with explicit trigger keywords. |
| **Tool Call Error** | Tool crashed due to invalid params, wrong types, or OS quirks. | Add input sanitization or explicit invariant notes in `SKILL.md`. |
| **User Correction** | User intervened to correct tone, path, or workflow assumptions. | Refine procedural step in `SKILL.md` or log invariant to `learnings.md`. |
