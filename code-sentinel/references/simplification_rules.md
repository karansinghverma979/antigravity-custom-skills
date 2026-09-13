# Non-Biased Code Simplification & Refactoring Guide

True engineering elegance is about removing unnecessary complexity, not adding clever abstractions.

---

## 1. Core Simplification Principles

1. **Preserve External Invariants**: Never mutate external API signatures, public return types, or operational behavior during a simplification pass.
2. **Flatten Deep Nesting**: Use guard clauses (early returns) to eliminate arrow-shaped nested `if-else` cascades.
3. **Strip Speculative Boilerplate**: Delete unused helper functions, single-use factory wrappers, and abstract base classes that only have one implementation.
4. **Prefer Explicit Data Structures**: Choose simple dictionaries, tuples, dataclasses, or plain interfaces over bloated object-oriented inheritance hierarchies.

---

## 2. Refactoring Transformations

### A. Guard Clauses (Early Exit)
```python
# Before (Nested):
def handle_request(req):
    if req.is_authenticated:
        if req.payload is not None:
            if not req.is_expired:
                return process(req.payload)
    return None

# After (Flat & Readable):
def handle_request(req):
    if not req.is_authenticated or req.payload is None or req.is_expired:
        return None
    return process(req.payload)
```

### B. Inline Single-Use Helpers
If a helper function is only called once and is 1–2 lines of trivial logic, inline it to keep the call stack readable.
