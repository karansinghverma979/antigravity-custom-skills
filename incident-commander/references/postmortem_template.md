# Blameless Postmortem & Root Cause Analysis (5 Whys) Template

A blameless postmortem focuses on systemic vulnerabilities, missing automated guards, and brittle assumptions rather than individual error.

---

## 1. Postmortem Markdown Structure

```markdown
# 🚨 Incident Postmortem: [Title]
- **Date**: YYYY-MM-DD
- **Severity**: SEV1 / SEV2 / SEV3
- **Duration**: [Start Time] - [Resolution Time] (X minutes)

---

### 1. Executive Summary
Brief high-level description of what occurred, user impact, and immediate resolution.

### 2. Incident Timeline (UTC / IST)
- `HH:MM` — Defect introduced (Commit / Deploy / DB mutation)
- `HH:MM` — Anomaly detected (Alert / User report)
- `HH:MM` — Mitigation initiated
- `HH:MM` — Full recovery confirmed

### 3. Root Cause Analysis (5 Whys)
1. *Why did the system fail?* — [Immediate symptom]
2. *Why did that occur?* — [Trigger event]
3. *Why wasn't it caught?* — [Missing test or linter]
4. *Why was the architecture vulnerable?* — [Underlying design gap]
5. *Why is the root systemic cause present?* — [Core policy or pattern deficit]

### 4. Corrective Action Items
| Action Item | Type (Prevent / Detect / Mitigate) | Owner / Strike | Status |
| :--- | :--- | :--- | :--- |
| Add unit test for edge case | Prevent | Engineering | Pending |
| Add PreToolUse safety gate | Prevent | Hook Master | Pending |
```
