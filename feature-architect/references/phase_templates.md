# Phased Vertical Slice Implementation Templates

When developing complex features, avoid monolithic multi-file rewrites. Implement in isolated, verifiable vertical slices.

---

## 1. The 3-Phase Implementation Pattern

```text
Slice 1: Data Contracts & Schemas (Types, Models, DB migrations)
   │
   ▼ [Verify with Typecheck / Schema Linter]
Slice 2: Core Business Engine (Logic, Services, Handlers)
   │
   ▼ [Verify with Unit Tests / CLI invocation]
Slice 3: Integration & User-Facing Surfaces (Endpoints, UI, CLI commands)
   │
   ▼ [Verify End-to-End & Code Sentinel Audit]
```

---

## 2. Invariant Checklist per Slice

1. **Slice 1 (Contracts)**:
   - Export explicit types/interfaces.
   - Zero side-effects; pure structure.
2. **Slice 2 (Business Logic)**:
   - Handle error edges explicitly (no swallowed exceptions).
   - Inject dependencies rather than hardcoding global state.
3. **Slice 3 (Wiring & E2E)**:
   - Wire contracts to entry points.
   - Run linter and verify zero broken links.
