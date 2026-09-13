---
name: code-sentinel
description: >-
  Elite multi-pass code reviewer, vulnerability auditor, and complexity simplifier.
  Use whenever reviewing pull requests, inspecting recent git diffs, checking for silent error suppressions,
  simplifying over-engineered code, or performing pre-merge quality gates, even if the user just asks to "review my changes" or "simplify this code."
---

# 🛡️ Code Sentinel: Multi-Pass Code Review & Simplification Engine

Use this skill when conducting deep code reviews, auditing pull requests, identifying hidden failure modes, or refactoring complex code into clean, maintainable logic.

---

## 🏛️ The 4-Pass Review Architecture

Superficial code reviews miss silent bugs and creeping complexity. Code Sentinel enforces a systematic **4-Pass Review**:

```
┌────────────────────────────────────────────────────────┐
│                   4-Pass Review Radar                  │
├────────────────────────────────────────────────────────┤
│ 1. 🔍 Logic & Silent Failures (Unchecked errors/nulls) │
│ 2. 🛡️ Security & Injection Surface (SQL/Command/Auth)  │
│ 3. 🧹 Non-Biased Simplification (Anti-overengineering) │
│ 4. 🧪 Test & Edge Case Coverage (Boundary conditions)  │
└────────────────────────────────────────────────────────┘
```

For specialized standards:
- [Silent Failures Audit Checklist](./references/silent_failures.md)
- [Simplification & Refactoring Rules](./references/simplification_rules.md)
- [5-Pass Pre-Launch Security Engine](../vibe-security/SKILL.md)

---

## 🔄 Review & Simplification Workflow

### Step 1: Automated Diff Inspection
Run the diff analyzer to catch dangerous syntax anti-patterns:

```bash
python ~/.gemini/antigravity-cli/skills/code-sentinel/scripts/audit_diff.py <repo_path>
```

### Step 2: Pass 1 — Silent Bug & Failure Analysis
Inspect all modified error-handling blocks:
- Are exceptions caught specifically or broadly?
- Are errors logged with actionable context?
- Does any fallback mask a failure?

### Step 3: Pass 2 — Security & Vulnerability Check
- Verify input sanitization, parameterized queries, and safe subshell execution.
- Ensure API tokens, secrets, or sensitive session data are never logged.

### Step 4: Pass 3 — Non-Biased Simplification
- Flatten deep nesting using guard clauses.
- Remove redundant intermediate wrappers and unused boilerplate.
- Preserve 100% of public API contracts.

### Step 5: Pass 4 — Synthesize Actionable Feedback
Deliver structured findings:
- **`[CRITICAL]`**: Bugs, security vulnerabilities, silent failures.
- **`[SIMPLIFY]`**: Refactoring opportunities to reduce cyclomatic complexity.
- **`[NIT]`**: Minor naming or style suggestions.
