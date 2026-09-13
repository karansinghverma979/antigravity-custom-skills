---
name: profile
description: >-
  Permanent immutable personal baseline engine and biographical dossier governor for ~/.gemini/Profile.md.
  Maintains verified physical metrics, PST standards, academic credentials, and cutoff age calculations.
  Use whenever inspecting personal profile, verifying PST standards, calculating exam eligibility, or invoking /profile.
---

# 👤 Personal Profile & Baseline Dossier Engine

Use this skill to inspect, verify, update, or audit the user's permanent personal profile, biographical baseline, academic credentials, and physical milestones in `~/.gemini/Profile.md`.

---

## 🎮 Invocation Modes

| Command / Trigger | Purpose | Execution Protocol |
| :--- | :--- | :--- |
| `/profile` | Inspect baseline dossier | Direct read-only extraction of requested section. Zero unsolicited mutations. |
| `/profile age [cutoff_date]` | Calculate age & cutoff eligibility | Runs `scripts/calculate_age.py` for exact Years/Months/Days against standard brackets. |
| `/profile update <text>` | Mutate / Update profile | Executes the **6-Stage Dossier Lifecycle Pipeline** with backup safety. |
| `/profile audit` | Validate data integrity | Scans for chronological consistency, placeholder sections, and formatting integrity. |
| `/profile rollback` | Restore previous version | Restores `~/.gemini/Profile.md` from `~/.gemini/Profile.md.bak`. |

---

## 🏛️ 6-Stage Dossier Lifecycle Pipeline

Every modification to `~/.gemini/Profile.md` must strictly follow this procedure:

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ 1. Triage Intent │ ──► │ 2. Section Route │ ──► │ 3. Pre-Diff View │
└──────────────────┘     └──────────────────┘     └──────────────────┘
                                                           │
                                                           ▼
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ 6. Verify Backup │ ◄── │ 5. Execute Write │ ◄── │ 4. User Approval │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

1. **Triage & Separation**: Ensure information belongs in `Profile.md` (permanent identity/credentials) and NOT dynamic living reality (`Intel.md`), tactical operations (`campaigns.sqlite`), or AI directives (`GEMINI.md`).
2. **Section Routing**: Map input to the standard taxonomy:
   - `Section 1`: Core Demographics & Identity (Name, DOB, permanent contact coordinates).
   - `Section 2`: Academic & Certification Baseline (Degrees, board marks, professional certifications).
   - `Section 3`: Physical & Biometric Standards (PST metrics, height, endurance times, benchmarks).
   - `Section 4`: Technical Capabilities & Tools Inventory.
   - `Section 5`: Strategic Timelines & Milestones.
3. **Pre-Mutation Diff**: Present field, prior value, and proposed change to the user.
4. **User Confirmation**: Require explicit approval before writing.
5. **Atomic Backup & Write**: Save `Profile.md.bak` prior to overwriting `Profile.md` in UTF-8.
6. **Integrity Validation**: Ensure no duplicate contradictory fields exist in the ledger.

---

## ⏱️ Dynamic Age & Cutoff Engine

When checking exam or recruitment age eligibility:

```powershell
python "~/.gemini/antigravity-cli/skills/profile/scripts/calculate_age.py" "<cutoff_date>"
```

*Computes exact chronological age as of `<cutoff_date>` (DD-MM-YYYY) and checks compliance against statutory brackets.*
