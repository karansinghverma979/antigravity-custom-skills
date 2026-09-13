# Silent Failures & Error Handling Audit Guide

A primary cause of production incidents is silent error suppression—code that fails without adequate logging, user alerting, or actionable diagnostics.

---

## 1. High-Risk Anti-Patterns

### ❌ Pattern 1: Empty or Swallowed Exceptions
```python
# Fatal:
try:
    process_payment(order)
except Exception:
    pass  # Swallowed! User has no idea payment failed.
```
```typescript
// Fatal:
try {
  await syncDatabase();
} catch (e) {
  console.log("error"); // Inadequate context, execution continues blindly.
}
```

### ❌ Pattern 2: Silent Fallbacks Masking Critical State
Falling back to a mock, empty object, or default config when a critical backend service is down without explicit notification.

### ❌ Pattern 3: Overly Broad Catch Blocks
Catching base `Exception` or `catch (err)` when only a specific `FileNotFoundError` or `NetworkTimeout` was expected, inadvertently masking syntax errors, `NameError`s, or critical type mismatches.

---

## 2. Auditor Checklist

When auditing error handling:
1. **Specificity**: Are catch blocks catching only known, anticipated error types?
2. **Contextual Diagnostics**: Does the log include the failing resource ID, operation name, and payload summary?
3. **Actionable Feedback**: If this fails, does the user or operator know what step to take next?
4. **Crash Safety**: Does the system fail fast on configuration or invariant violations instead of decaying into corrupt state?
