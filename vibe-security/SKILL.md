---
name: vibe-security
description: >-
  Autonomous 5-pass pre-launch security auditor based on battle-tested open-source tools
  (Gitleaks, Bearer, ECC Production Audit, Trail of Bits, ECC Security Review).
  Automatically triggers on web app builds, API routes, database schemas, auth workflows,
  payment integrations, and pre-deployment gates without needing manual prompting.
---

# 🛡️ Vibe-Security: 5-Pass Autonomous Pre-Launch Security Engine

This skill equips the assistant to autonomously audit, harden, and defend applications before deployment. It integrates 5 core security passes modeled on premier industry tools.

```
┌─────────────────────────────────────────────────────────────┐
│                   THE 5 SECURITY AUDIT CHECKS               │
├────┬─────────────────────────────┬──────────────────────────┤
│ 01 │ Secret Leak Prevention      │ Based on Gitleaks        │
│ 02 │ Personal Data Flow Audit    │ Based on Bearer          │
│ 03 │ Pre-Deploy Production Audit │ Based on ECC Audit       │
│ 04 │ Deep Security Audit (Logic) │ Based on Trail of Bits   │
│ 05 │ Attacker's Perspective      │ Based on ECC Security    │
└────┴─────────────────────────────┴──────────────────────────┘
```

---

## 🔒 01. Secret Leak Prevention (Based on Gitleaks)
*Goal: Zero hardcoded secrets, keys, or credentials anywhere in the repository.*

1. **Move All Secrets to Environment Variables**:
   - Check every API key, password, token, database URL, and credential in the codebase.
   - Ensure no secret exists as a string literal in source code, configs, utility files, or comments.
2. **Framework & Vendor-Specific Checks**:
   - **Supabase**: Anon keys only client-side when Row Level Security (RLS) is strictly enabled on every table. Service role keys must NEVER touch client-side code.
   - **Stripe / Payment**: Only publishable keys client-side; secret keys strictly server-side.
   - **Database URLs**: MongoDB, PostgreSQL, Redis connection strings exclusively in environment variables.
   - **OAuth & Auth**: OAuth client secrets and JWT signing secrets must remain server-side.
   - **Third-Party APIs**: OpenAI, SendGrid, Twilio, Firebase Admin, AWS, Resend in env vars only.
3. **Frontend Leak Protection**:
   - Verify that no sensitive secret is prefixed with `NEXT_PUBLIC_`, `VITE_`, or `REACT_APP_`.
4. **Git Hygiene**:
   - Ensure `.env` is listed in `.gitignore`.
   - Maintain a `.env.example` file with placeholder values.
5. **Log & Response Sanitation**:
   - Verify `console.log`, logger statements, error handlers, and API responses never expose tokens or connection strings.
6. **Git History Notice**:
   - If a secret was previously committed, flag it for immediate rotation.

---

## 👤 02. Personal Data Flow Audit (Based on Bearer)
*Goal: Track user PII end-to-end and prevent leakage into logs, caches, or third parties.*

1. **Map Collection Points**: Trace all sensitive user inputs (emails, phones, passwords, names, addresses, payment data, IP addresses, device info).
2. **Clean Logs**: Ensure no logger or print statement outputs user PII or auth tokens. Redact with `[REDACTED]` or eliminate.
3. **Third-Party SDK Audit**: Review analytics, error monitoring (Sentry), email providers, and AI endpoints to ensure only minimal required payloads are transmitted.
4. **Password Security**: Passwords must be hashed using `bcrypt`, `argon2`, or `scrypt` (never raw SHA256/MD5). Plaintext passwords must never be stored or echoed.
5. **Storage & Cookie Hygiene**:
   - Cookies carrying session tokens must have `httpOnly`, `secure`, and `sameSite` flags.
   - Never store user PII or sensitive tokens in `localStorage` (vulnerable to XSS).
6. **API Response Filtering**: Apply field-level response filtering. Never return password hashes, internal server metadata, or cross-tenant records.
7. **Account Deletion**: Provide a clean data deletion / anonymization pathway for user accounts.

---

## 🚀 03. Pre-Deploy Production Audit (Based on ECC Production Audit)
*Goal: Ensure baseline operational resilience and production readiness.*

1. **Env Var Validation**: Enforce startup schema validation (e.g. Zod / Envalid) so the application fails fast if critical variables are missing.
2. **Debug Code Stripping**: Remove test-only routes (`/test`, `/debug`, `/admin-backdoor`), seed scripts, commented-out blocks, and debug flags. Ensure production debug mode defaults to OFF.
3. **Safe Error Handling**: Client error responses must return generic status messages and correlation/trace IDs. Stack traces and database details belong solely to server-side logs.
4. **Security Headers**: Enforce `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Strict-Transport-Security` (HSTS max-age 1 year), and restrictive `Content-Security-Policy`. Use `helmet` or framework equivalents.
5. **Rate Limiting**: Protect auth endpoints (login, signup, OTP, password reset) with strict IP/user rate limiting (e.g., max 5 attempts/min on login).
6. **CORS Restrictions**: Explicitly restrict CORS origins to trusted frontend domains instead of wildcard `*`.
7. **Database Hardening**: Force TLS/SSL on DB connections, eliminate default credentials, and ensure database ports are never exposed publicly.

---

## 🧠 04. Deep Security Audit for Complex Logic (Based on Trail of Bits)
*Goal: Harden core business logic, authentication state machines, and payment flows.*

1. **Authentication & Authorization (Anti-IDOR)**:
   - Check every protected route and API endpoint for server-side ownership verification.
   - Prevent Insecure Direct Object References (IDOR): never fetch records purely by user-supplied IDs without checking session ownership.
   - Password reset tokens must be cryptographically random, single-use, time-limited (max 15 mins), and tied to specific user IDs.
   - JWT tokens must use strong signing secrets, enforce short expiry, and handle invalidation on logout.
2. **Payment & Financial Logic**:
   - Never calculate prices, discounts, taxes, or order totals on the client side.
   - Validate Stripe/Razorpay webhook signatures on raw request bodies before fulfilling orders.
   - Verify transaction status strictly server-side before granting entitlements or subscription tiers.
3. **Input Handling & Injection Defense**:
   - Use parameterized queries or ORM abstractions for all database operations (anti-SQLi).
   - Sanitize all user-rendered input to prevent Cross-Site Scripting (XSS).
   - Validate file uploads server-side (MIME-type verification, magic byte checks, size limits, non-executable storage).

---

## 🎯 05. Attacker's Perspective Review (Based on ECC Security Review)
*Goal: Actively simulate offensive threat vectors before adversaries do.*

1. **ID Manipulation & Multi-Tenancy**: Attempt cross-account access via parameter tampering (`/api/order/102` vs `/api/order/103`).
2. **Authentication Bypasses**: Test malformed JWTs, missing bearer headers, expired session tokens, and default admin credentials.
3. **Privilege Escalation**: Verify that role checks (`user`, `admin`, `moderator`) are strictly evaluated server-side, not merely inferred from UI visibility.
4. **Abuse & Exhaustion**: Verify rate limits against bot registration, SMS/email OTP flooding, mass file upload denial-of-service, and promo code infinite stacking.
5. **Internal Asset Exposure**: Ensure `.git/`, `.env`, database management consoles, health endpoints leaking environment details, and internal Swagger/OpenAPI docs are inaccessible to the public.
6. **Business Logic Exploits**: Check for negative quantities/amounts, currency conversion arbitrage, coupon self-referrals, and unlimited free-trial renewals.
