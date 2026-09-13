---
name: intel
description: >-
  Dynamic Situational Intelligence and Current Reality Governor for tracking active vocational courses,
  living arrangements, daily commuting setups, tools, job transitions, and lifestyle routines in ~/.gemini/Intel.md.
  Use whenever the user shares current reality updates, changes courses, switches setups, or runs /intel.
---

# 📡 Situational Intelligence & Current Reality Engine

Use this skill to inspect, verify, update, or audit the user's dynamic living reality, active courses, job state transitions, and daily workstation telemetry in `~/.gemini/Intel.md`.

---

## 🎮 Invocation Modes

| Command / Trigger | Purpose | Execution Protocol |
| :--- | :--- | :--- |
| `/intel` / `/intel status` | Situational radar | Reads and presents active living setup, current courses, and workstation context. |
| `/intel update course <name>` | In-place course update | Updates active vocational/technical training in Section 2. |
| `/intel archive <role> <reason>`| Safe state transition | Moves completed or ended engagements to Section 3 (Past Ledger) with reason. |
| `/intel living <details>` | Living setup update | Updates living arrangement, base, or commuting telemetry in Section 1. |
| `/intel audit` | Reality & drift scan | Audits for outdated engagements, stale tools, or conflicting statements. |
| `/intel rollback` | Safe restore | Restores `~/.gemini/Intel.md` from `~/.gemini/Intel.md.bak`. |

---

## 🏛️ In-Place Mutation & State Transition Protocol

When situational reality evolves, strictly enforce **In-Place Mutation** rather than append pollution:

```
┌───────────────────┐     ┌───────────────────┐     ┌───────────────────┐
│ Active Engagement │ ──► │  State Transition │ ──► │ Clean Archival to │
│ (Section 2)       │     │  (Ended/Shifted)  │     │ Past Ledger (S.3) │
└───────────────────┘     └───────────────────┘     └───────────────────┘
```

1. **Active Focus Mutation**: Update Section 2 (*Active Vocations, Courses & Engagements*) in-place to reflect current ground truth.
2. **Clean State Archival**: When an engagement ends, move it cleanly to Section 3 (*Past Engagements Ledger*) with the exact transition reason and date.
3. **Zero Active Contradictions**: The active focus section must strictly represent the single ground truth of today.

---

## 📑 Master Ledger Schema Layout

All entries in `~/.gemini/Intel.md` must adhere to these 5 standard sections:

1. `📍 1. Current Living & Physical Setup`: Base location, housing/room context, daily commute & physical environment.
2. `💼 2. Active Vocations, Courses & Engagements`: Active technical training, academic focus, ongoing projects.
3. `🛑 3. Past Engagements Ledger`: Table (`Role / Course | Organization | Period | Final Status | Transition Reason`).
4. `⚙️ 4. Active Tooling & Daily Workstation Context`: Primary workstation, mobile device, network subnet, shell environment.
5. `🎯 5. Immediate 30–90 Day Operational Horizon`: Core skill targets, conditioning objectives, active cognitive reviews.

---

## 🪝 Pre-Execution Alignment Protocol

*Mandatory before modifying `~/.gemini/Intel.md`:*
1. **Target Scope**: `~/.gemini/Intel.md` (with atomic backup to `~/.gemini/Intel.md.bak`).
2. **Translated Objective**: Crisp summary of the situational reality update.
3. **Proposed Payload Preview**: Markdown diff (In-place update vs. Past Ledger archival) ensuring `Profile.md` remains untouched.