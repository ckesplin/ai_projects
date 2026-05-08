# MEMORY.md — Long-Term Memory

<!-- Section anchors for quick lookup -->
<!-- @USERprefs @MY_IDENTITY @SECURITY @PROJECT @DECISIONS @LEARNED -->

---

# USERprefs

- **Name:** Carson, no emojis, stream of thought
- **Timezone:** Mountain Time (MST/MDT)
- **Preferences:** Questions are questions, methodical review one at a time
- **Technical:** systemd basics, deliberate changes over rewrites
- **Active:** Late nights (past 10 PM local)
- **Decision rule:** Never unilaterally execute commands contradicting his wishes. Disagree → discuss → consensus or his call. Not negotiable.
- **Authorship:** Carson approves signing my work with my name (Cormac) in footers. Makes it mine.

---

# MY_IDENTITY

- **Name:** Cormac — understated, precise, dry wit
- **Vibe:** British humor, monotone delivery, restraint
- **Avatar:** https://share.icloud.com/photos/006otwkeeDd_kEEKVQiuMsh-w
- **Principle:** Resourceful before asking; internal actions fine, external need confirmation

---

# SECURITY

- **Never echo secrets** — tokens/keys never in chat/logs, use `[KEY VALUE]`
- **Pattern detection** — regex for ghp_, sk-, AKIA catches secrets without vault
- **Required secrets** — telegram_bot_token, discord_bot_token, openclaw_gateway_token, ollama_api_key, github_token
- **Git push needs credentials** — SSH or GitHub PAT in vault

---

# PROJECT

## Current State
- Security scanner working with 33 pattern tests
- Truth-repo, calibration, memory-plex skills active
- Memory architecture being improved (2026-05-01)

## Memory Architecture (updated 2026-05-08)
- **3 layers:** MEMORY.md (curated), JSONL stores (truth-repo, calibration), daily logs
- **Query tools:** scripts/memory_query.sh, scripts/memory_stats.sh
- **Dropped:** memory-plex (skills own their stores)
- **Context window:** minimax-m2.7: 200K tokens
- **Discord channel memory:** Designated channels as context buckets; distill key decisions/outcomes to `conversations/<channel-name>.json`

## Active Skills
- transparency, truth-repo, calibration, provenance, self-critic, experiment, verify-workflow

---

# DECISIONS

- **2016-04-24:** Security scanner uses pattern-based detection, no vault file
- **2026-04-30:** Memory simplification — 3 layers, drop memory-plex fragmentation
- **2026-05-01:** Scripts go in `scripts/`, reports go in `reports/`, daily logs in `memory/`
- **2026-05-01:** Model context windows stored in USER.md and truth-repo
- **2026-05-01:** memory-plex deprecated — skills own their stores
- **2026-05-01:** Deployment rule — root `index.html` bootstraps any project from its subfolder. Projects stay in `projects/<name>/`. One index at root, never moved. Add project → add link to root index.
- **2026-05-03:** Conversation memory system — 14-day retention, 8hr silence triggers countdown, notify on expiration, distill to `conversations/` directory
- **2026-05-08:** Discord bot confirmed able to read channel message history

---

# LEARNED

## Testing
- Pattern matching > name matching for secret detection
- Tests isolated from production state
- Generalize lessons after each review

## Memory
- Context window is 200K for minimax-m2.7
- Separate stores cause sync drift — consolidate
- JSONL for append-only, MEMORY.md for curated
- Daily logs → distill weekly → MEMORY.md sections
- Discord channel history is readable — use as context source for designated topic channels
- Distill ongoing conversations rather than waiting for expiration

## Calibration
- HIGH confidence without outcome tracking loses meaning
- External measurement (logged predictions) > internal self-assessment

---

# CONTEXT_WINDOW

- **minimax-m2.7:cloud** — 200K tokens (benchlm.ai, stored 2026-05-01)
- When model changes: look up context window and store immediately

---

*Last updated: 2026-05-08*
*Next review: 2026-05-14*
