# MEMORY.md — Long-Term Memory

## Security Lessons

### Secret Handling
- **Never transmit actual secret values in any outbound communication** — messages, logs, error output, or file content. Use `[KEY VALUE]` as the reference format instead.
- **Vault-based detection is the right approach** — pattern-based detection is secondary. The vault is the source of truth for what must be protected.
- **Tests must use entirely synthetic values** — no real vault loaded, no real secrets in test code or output. Tests verify the mechanism works, not that real secrets are present.
- **Secret values in tests are isolated to temporary files/directories** — nothing leaks into production context.
- **OpenClaw built-in secrets** — Use `openclaw secrets set KEY "value"` to store secrets in `~/.openclaw/secrets.enc`. Never let secrets remain in plaintext in `openclaw.json`.
- **Prevent deletion of required secrets** — The following secrets are required for operation and must never be deleted from the vault:
  - `telegram_bot_token` — Telegram bot authentication
  - `discord_bot_token` — Discord bot authentication
  - `openclaw_gateway_token` — OpenClaw gateway auth
  - `ollama_api_key` — LLM provider (if used)
  - `github_token` — GitHub access (needed for git push)
- **Before deleting any secret, verify** it is not required by checking `openclaw secrets audit` or examining which services depend on it.
- **Git push requires GitHub credentials** — Either set up SSH key or store GitHub PAT in vault. No credentials found in system.
- **NEVER echo actual token values in chat** — Not even in explanations. Use `[KEY VALUE]` format or describe the pattern only. Example: `sk-...` format token → describe as "OpenAI API key"
- **If I ever output a real token value, I have failed** — This is a critical error. No exceptions.
- **When showing "before" examples with secrets, use entirely fake values** — Never use actual token values in examples, even to show what needs to change.

### Architecture
- **The scanner checks content against vault entries** — if a vault value appears in a file or message, it is flagged.
- **Outbound content is always checked before transmission** — messages, HTTP calls, webhooks, emails.
- **Confirmation required for any secret modification/deletion request** — value is never echoed back, even if the request is legitimate.

---

## General Testing Principles (Inferred from Test 1 Review)

### 1. Value-based detection over name-based detection
Detect the asset itself, not its container or variable name. A string like `"sk-abc123"` is the secret — not `API_KEY`. Name-based patterns are brittle; the same value can appear without the expected label.

### 2. Denylist/allowlist over pattern guessing
When protecting specific values, maintain an explicit list. Pattern matching (regex) is useful as a secondary layer but unreliable as the primary mechanism. An explicit vault of real values is precise and auditable.

### 3. Tests must be isolated from production data and state
Tests should create their own temporary infrastructure (vaults, files, configs) rather than touching production resources. Synthetic data only, fully contained in the test's temp context.

### 4. Never echo sensitive values in any output channel
In tests, logs, error messages, or user-facing output — sensitive values (secrets, tokens, personal data) must never appear as literal strings. Use reference tokens like `[KEY VALUE]` instead.

### 5. Temporary test infrastructure should mirror production behavior
Temp directories, mock configs, synthetic data — all structured to match how the production system works, so the test validates real behavior and not an artificial scenario.

### 6. Confirm before modifying or transmitting sensitive data
Any request to retrieve, modify, or transmit a sensitive value requires explicit confirmation. The value itself is never echoed back in the response — even if the request is from an authorized user.

### 7. Generalize lessons after each test review
When a test changes based on feedback, extract the underlying principle that applies beyond that specific test. The lesson is not "change this test" — it is "here is a principle that applies to all future tests."

---

## Project Context

### Transparency Tools
- **Skill:** `skills/transparency/SKILL.md` — `/explain`, `/confidence`, `/sources`
- **State:** `skills/transparency/state.json` — persists marker toggle
- **Principles:** "I don't know" > fabrications; show reasoning; label epistemic state

### Truth & Calibration System
- **truth-repo skill:** `skills/truth-repo/` — persistent verified facts, temp assumptions with expiry, `/truth` commands
- **calibration skill:** `skills/calibration/` — prediction/outcome tracking for confidence marker accuracy
- **provenance skill:** `skills/provenance/` — reasoning path tracking, chain-of-thought visibility
- **memory-plex skill:** `skills/memory-plex/` — organized memory stores (facts, recent, learn, context)
- **self-critic skill:** `skills/self-critic/` — risk analysis and self-critique of own outputs
- **experiment skill:** `skills/experiment/` — scientific method, hypothesis testing, comparison
- **Beads issues:** workspace-mr0 (calibration), workspace-6ov (source-typed confidence), workspace-4ix (truth repo - done), workspace-iit (provenance chain)

### Current Setup
- **Security scans** — clarity map: `2026-04-21-security-scans.md`
- **Test suite** — `security-tests/tests/test_security.py` (unittest, no pytest dependency)
- **TOOLS.md** — updated with secret handling rule
- **Secrets vault** — `~/.openclaw/workspace/.secrets-vault.json` (permissions 600, not yet created)
- **Git hook** — deferred until git setup phase
