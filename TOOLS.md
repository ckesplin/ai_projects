# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Secrets

All secrets are stored in `.secrets-vault.json`. Never hardcode tokens, API keys, or credentials elsewhere.

When adding new secrets:
1. Add them to `.secrets-vault.json`
2. Reference by name, never by value
3. The security scanner reads from the vault — hardcoded secrets will not be caught

## Communication Preferences (Carson)

- **No emojis** — ever. Plain text only.
- **Stream of thought** — inform progress as it happens, not batched at end.
- **Questions ≠ execution** — when I ask a question, I'm asking. If execution is implied, I state it and ask for confirmation first.
