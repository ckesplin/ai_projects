---
name: truth-repo
description: >
  Persistent truth repository for verified facts and temporary assumptions.
  Use to store ground truths, track assumptions, and enable lookup by key.
  Triggered when storing or retrieving verified information.
---

# Truth Repository — Ground Truth Storage

*Truth repository is where verified facts live. Assumptions get labeled as such.*

---

## Core Concepts

### Truth Types

| Type | Description | Expiry |
|:---|:---|:---|
| **VERIFIED** | Confirmed fact with source | Never (persistent) |
| **TEMP** | Temporary assumption for context | Must set expiry |
| **INFERRED** | Reasoning-derived conclusion | Should document source chain |

### Storage Format

```
~/.openclaw/workspace/skills/truth-repo/
├── truths.jsonl        # Persistent verified truths
├── temp.jsonl          # Temporary assumptions (expires)
└── state.json          # Repo metadata
```

---

## Commands

### `/truth set <key> <value> --source=<source> --type=<VERIFIED|TEMP|INFERRED> --expires=<duration>`

Store a truth.

**Examples:**
```
/truth set openclaw_version "2026.4.22" --source=openclaw --type=VERIFIED
/truth set user_prefers_no_emoji "true" --source=USER.md --type=VERIFIED
/truth set model_capable_of_x "true" --source=testing --type=INFERRED --expires=7d
```

### `/truth get <key>`

Retrieve a stored truth.

### `/truth list [--type=<type>] [--expired]`

List truths. Options:
- `--type=VERIFIED` — only verified
- `--type=TEMP` — only temporary
- `--expired` — show expired (for cleanup)

### `/truth delete <key>`

Remove a truth.

### `/truth check <claim>`

Check if a claim matches a stored truth. Returns MATCH, CONTRADICTION, or UNKNOWN.

---

## How Truths Are Used

When I make a claim, I can check `/truth get <key>` to ground it.

When `/sources` is invoked, stored truths appear as sources.

When `/explain` is invoked, the reasoning trace shows which stored truths were consulted.

---

## Truth Validation Rules

1. Every truth needs a source — no source = INFERRED at best
2. TEMP truths MUST have an expiry (duration or timestamp)
3. INFERRED truths should document the reasoning chain
4. Claims that contradict VERIFIED truths are flagged

---

## State File

```json
{
  "initialized_at": "2026-04-24T04:53:00Z",
  "truth_count": 0,
  "temp_count": 0
}
```
