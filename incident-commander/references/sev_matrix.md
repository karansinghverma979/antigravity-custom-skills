# Incident Severity Classification & Blast Radius Matrix

When outages, production crashes, or silent data corruptions occur, classify severity immediately:

---

## 1. Severity Levels

| Level | Definition | Impact Radius | Response Protocol |
| :--- | :--- | :--- | :--- |
| **SEV1** | **Critical Outage / Data Loss** | Entire service down, core database corrupt, active security breach. | Immediate halt on all feature work; all focus on mitigation. |
| **SEV2** | **Major Degradation** | High-impact flow broken (e.g. auth failing, 50% API timeout). | Immediate mitigation within 1 hour; work continues with high priority. |
| **SEV3** | **Moderate Issue** | Non-critical feature broken or partial UI failure with workaround. | Mitigate in current work cycle. |
| **SEV4** | **Minor Defect / Metric Flake** | Low-impact bug, cosmetic flaw, or non-blocking log noise. | Queue into backlog. |

---

## 2. Blast Radius Assessment Checklist
1. **Affected Systems**: Which services, databases, or API endpoints are failing?
2. **Data Integrity**: Has persistent state been corrupted, or is it transient?
3. **Rollback Feasibility**: Can the change be rolled back immediately via `git revert` or backup restoration?
