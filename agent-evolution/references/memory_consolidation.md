# Memory Consolidation & In-Place Updating Specification

To prevent cognitive pollution, duplicate statements, and contradiction drift, memory consolidation must strictly follow **In-Place Mutation** rather than blind appending.

---

## 1. Single Source of Truth Separation

Every piece of persistent memory belongs strictly to its designated layer:

```
┌──────────────────────────────────────────────────────────────┐
│  ~/.gemini/memory/learnings.md                               │
│  • Technical machine memory: shell traps, CLI quirks,        │
│    Python Windows encoding bugs, tool argument invariants.   │
├──────────────────────────────────────────────────────────────┤
│  ~/.gemini/Intel.md                                          │
│  • Dynamic reality: living setup, current active courses,    │
│    hardware tools, ongoing project priorities.               │
├──────────────────────────────────────────────────────────────┤
│  ~/.gemini/Profile.md                                        │
│  • Immutable personal baseline: DOB, academic baseline, PST. │
└──────────────────────────────────────────────────────────────┘
```

---

## 2. In-Place Update Protocol (Anti-Append Rule)

1. **Deduplication Check**: Before recording any newly discovered technical quirk or system constraint, search `learnings.md` to see if a related section already exists.
2. **In-Place Refinement**: If the topic exists, update or expand that specific section rather than creating a new trailing bullet point.
3. **Zero Contradiction**: Obsolete behaviors are replaced immediately. Never allow two conflicting rules to co-exist.
