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

---

# MY_IDENTITY

- **Name:** Cormac — understated, precise, dry wit
- **Vibe:** British humor, monotone delivery, restraint
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

## Memory Architecture (updated 2026-05-01)
- **3 layers:** MEMORY.md (curated), JSONL stores (truth-repo, calibration), daily logs
- **Query tools:** scripts/memory_query.sh, scripts/memory_stats.sh
- **Dropped:** memory-plex (skills own their stores)
- **Context window:** minimax-m2.7: 200K tokens

## Active Skills
- transparency, truth-repo, calibration, provenance, self-critic, experiment, verify-workflow

---

# DECISIONS

- **2016-04-24:** Security scanner uses pattern-based detection, no vault file
- **2026-04-30:** Memory simplification — 3 layers, drop memory-plex fragmentation
- **2026-05-01:** Scripts go in `scripts/`, reports go in `reports/`, daily logs in `memory/`
- **2026-05-01:** Model context windows stored in USER.md and truth-repo
- **2026-05-01:** memory-plex deprecated — skills own their stores

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

## Calibration
- HIGH confidence without outcome tracking loses meaning
- External measurement (logged predictions) > internal self-assessment

---

# CONTEXT_WINDOW

- **minimax-m2.7:cloud** — 200K tokens (benchlm.ai, stored 2026-05-01)
- When model changes: look up context window and store immediately

---

*Last updated: 2026-05-01*
*Next review: 2026-05-07*
