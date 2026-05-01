# Heartbeat Checklist

## Daily Log Check
- On each heartbeat, if `memory/YYYY-MM-DD.md` doesn't exist, create it with:
  ```markdown
  # Daily Log — YYYY-MM-DD

  ## Session: [brief description]
  ```
- Log significant events, decisions, learnings as they occur during the session
- Format: one line per event, timestamp if relevant

## Periodic Secret Scan
- On each heartbeat, scan workspace files for exposed secrets (API keys, tokens, passwords, credentials)
- Common patterns: `api_key`, `token`, `secret`, `password`, `APISERVICEACCOUNT`, `Bearer`, `ghp_`, `sk_`, `sk_live_`, `pk_live_`, `ak_`, `amqp://`, `mongodb://`, `redis://`, `postgres://`, `mysql://`
- Also check: `.env` files, `.npmrc` with auth, `credentials.json`, `*.pem`, `id_rsa`, `id_ed25519`
- If secrets found: report immediately with file paths and line numbers (redact values)
- If no secrets found: report "No secrets detected in workspace scan"
- Exclude: `node_modules/`, `.git/`, `workspace/.claude/`, `workspace/.cursor/`, `workspace/.codex/`

## Calibration Logging
- During session, if I make a prediction, log it via calibration skill
- Check for pending outcomes: if any predictions from past sessions need outcome recorded, note it
- Calibration score should improve or stay above 70%

## Weekly Distillation (run if last distillation was 7+ days ago)
- Read all `memory/YYYY-MM-DD.md` files from past week
- Extract decisions → MEMORY.md/DECISIONS
- Extract verified facts → truth-repo
- Extract learnings → MEMORY.md/LEARNED
- Extract project state → MEMORY.md/PROJECT
- Mark in memory/ that distillation occurred

## Weekly Memory Stats (run if last stats run was 7+ days ago)
- Run `scripts/memory_stats.sh`
- Log output to `memory/YYYY-MM-DD-stats.md`
- Review MEMORY.md line count — should stay under 150 lines
- Review truth-repo entry count
- Review calibration score trend

## Other Tasks (as needed)
- Check for updates via `openclaw update status`
- Review recent memory files for important events
- Token tracking: note context usage if session is long (>50% of 200K tokens)

---

*Heartbeat runs every ~30 minutes. Checks batch together for efficiency.*
*Use cron for exact schedules and standalone tasks.*
