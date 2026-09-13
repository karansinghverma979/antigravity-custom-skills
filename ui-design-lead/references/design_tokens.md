# Design Tokens & Aesthetic System Specification

A distinctive interface relies on an intentional, highly restrained token system rather than generic CSS utility sprawl.

---

## 1. Palette Architecture (4–6 Tokens)

Avoid arbitrary colors. Define 4 to 6 named semantic tokens grounded in the domain's subject matter:

```css
:root {
  --color-canvas: #0f1117;    /* Base background */
  --color-surface: #181b24;   /* Elevated layer */
  --color-border: #262b3a;    /* Structural divider */
  --color-text-primary: #f0f3f8; /* High-contrast foreground */
  --color-text-muted: #8b95a8;   /* Secondary metadata */
  --color-accent: #3b82f6;       /* Single memorable focal accent */
}
```

---

## 2. Typographic Rhythm & Scale

1. **Scale Hierarchy**:
   - Display: 2.5rem–3.5rem (Distinctive weight/character)
   - Headings (H1/H2): 1.5rem–2.0rem
   - Body: 1.0rem (16px baseline, line-height 1.5–1.6)
   - Caption/Meta: 0.8125rem (13px, line-height 1.4)
2. **Line Length Constraint**:
   Keep body text constrained to `<75ch` (`max-width: 65ch`–`75ch`) for optimal readability.

---

## 3. Spacing & Structural Rhythm
Use a 4px/8px modular base scale:
- `space-1`: 4px | `space-2`: 8px | `space-4`: 16px | `space-6`: 24px | `space-8`: 32px
