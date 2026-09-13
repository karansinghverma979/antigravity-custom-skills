---
name: incident-commander
description: >-
  Lead incident response officer, emergency triage commander, and blameless postmortem author.
  Use whenever handling production outages, critical bugs, broken builds, unexpected crashes,
  database corruptions, or conducting 5-Whys root cause investigations, even if the user just says "prod is down" or "fix this crash."
---

# 🚨 Incident Commander: Production Triage & Postmortem Suite

Use this skill when responding to active system crashes, unexpected production defects, broken builds, or drafting blameless postmortems.

---

## 🏛️ Incident Response Framework

```
┌─────────────────────────────────────────────────────────┐
│ 1. 🔍 Triage (Assess SEV1–SEV4 & Blast Radius)         │
│ 2. 🛡️ Mitigate First (Rollback / Failover / Stop Bleed) │
│ 3. 🧪 Root-Cause Investigation (Logs & State Diff)      │
│ 4. 📝 Blameless Postmortem (5 Whys & Action Items)      │
└─────────────────────────────────────────────────────────┘
```

For classification and reporting schemas:
- [Severity Matrix & Blast Radius Assessment](./references/sev_matrix.md)
- [Blameless Postmortem & 5-Whys Template](./references/postmortem_template.md)

---

## 🔄 The 4-Phase Response Protocol

### Phase 1: Immediate Triage
1. Classify severity according to the [Severity Matrix](./references/sev_matrix.md).
2. Isolate affected components (database, network, auth, frontend).
3. If SEV1/SEV2 $\rightarrow$ halt feature branches and focus 100% on recovery.

### Phase 2: Rapid Mitigation (Stop the Bleeding)
- Prefer **fast rollback** (`git revert`, restoring backup snapshot) over hasty live hotfixes.
- If live fix is required, verify locally with `code-sentinel` before deploying.

### Phase 3: Root Cause Analysis
- Reconstruct the exact failure timeline.
- Execute the **5 Whys** method to trace systemic root causes rather than superficial symptoms.

### Phase 4: Blameless Postmortem & Prevention
1. Draft the postmortem using the [Postmortem Template](./references/postmortem_template.md).
2. Convert preventative fixes into actionable strikes/checkpoints.
