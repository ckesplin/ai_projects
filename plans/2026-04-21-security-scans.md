# Clarity Map: 2026-04-21-security-scans

**Request:** Set up security scans with three threat vectors covered: prevent secrets leaking, ensure I only respond to Carson's accounts, and prevent damaging acts without direct permission.

**Status:** Complete
**Exported:** 2026-04-21

---

- **What secrets are in scope?**
  - Decision: Explicit vault of real secret VALUES maintained by Carson. Pattern-based detection is secondary. The vault is the source of truth.
  - Outcome: Stated

- **How are secrets referenced in messages?**
  - Decision: All secret values are referenced as `[KEY VALUE]` — never the actual string in any outbound message, log, or error output.
  - Outcome: Stated

- **Who is the audience?**
  - Decision: External actors, AI agents, accidental exposure by Carson
  - Outcome: Stated

- **What is the interaction format?**
  - Decision: Discord + code repos
  - Outcome: Stated

- **What repos are scanned?**
  - Decision: Project repos I have access to
  - Outcome: Stated

- **How is Discord access controlled?**
  - Decision: Only respond to allowlisted Discord account (368889178936836102)
  - Outcome: Stated

- **How is Telegram access controlled?**
  - Decision: Add Telegram user 1404599210 (@ckesplin) to explicit DMs allowlist
  - Outcome: Stated

- **What is Goal #2 — only answer to Carson?**
  - Decision: No requests accepted from any other account
  - Outcome: Stated

- **What is Goal #3 — damaging acts?**
  - Decision: System changes, destructive commands, financial transactions, external transmissions
  - Outcome: Stated

- **What counts as direct permission?**
  - Decision: Secondary confirmation with explicit action statement + results to occur
  - Outcome: Stated

- **How are external transmissions handled?**
  - Decision: Allowlist-based. Empty at start. Carson adds destinations. Confirmation required per transmission.
  - Outcome: Stated

- **What is the destructive command boundary?**
  - Decision: /home/clawbot/.openclaw/workspace is my domain (no confirmation). Outside workspace but not system files requires confirmation.
  - Outcome: Stated

- **What is the success criteria?**
  - Decision: Test suite covering all three threat vectors, precommit hook (deferred until git setup), Carson reviews tests
  - Outcome: Stated

- **What is the deadline?**
  - Decision: Complete before any repo setup. Start ASAP.
  - Outcome: Stated

- **What language for the test suite?**
  - Decision: Agent chooses based on available tooling
  - Outcome: Deferred

- **How do confirmation prompts work?**
  - Decision: "[action] — is this ok with me to start?" — affirmative answer = proceed
  - Outcome: Stated

- **How is the git hook implemented?**
  - Decision: Deferred until git setup phase. Must be tested.
  - Outcome: Deferred

---

## Deferred Decisions

- **Test suite language:** Agent chooses — will select based on what's available in the current environment
- **Git hook implementation:** Deferred to git setup phase — precommit hook to prevent secrets leaking, must be tested

---

## Action Items

- Add Telegram DMs allowlist: user `1404599210`
- Build test suite covering all three threat vectors
- Implement precommit hook for secret detection *(deferred until git setup)*
- Set up git after tests pass and Carson approves
- External transmission allowlist remains empty until Carson populates it
