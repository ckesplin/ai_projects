# Heartbeat Checklist

## Periodic Secret Scan
- On each heartbeat, scan workspace files for exposed secrets (API keys, tokens, passwords, credentials)
- Common patterns to check: `api_key`, `token`, `secret`, `password`, `APISERVICEACCOUNT`, `Bearer`, `ghp_`, `sk_`, `sk_live_`, `pk_live_`, `ak_`, `amqp://`, `mongodb://`, `redis://`, `postgres://`, `mysql://`
- Also check for accidentally committed `.env` files, `.npmrc` with auth, `credentials.json`, `*.pem` private keys, `id_rsa`, `id_ed25519`
- If secrets found: report immediately to user with file paths and line numbers (redact the actual secrets)
- If no secrets found: report "✅ No secrets detected in workspace scan"
- Locations to scan: workspace root and subdirectories, but exclude `node_modules/`, `.git/`, `workspace/.claude/`, `workspace/.cursor/`, `workspace/.codex/`

## Other Tasks (as needed)
- Check for updates via `openclaw update status`
- Review recent memory files for important events