---
name: memory-plex
description: >
  Memory abstraction layer for organized, fast memory access.
  Provides indexed memory stores with quick lookup, expiration, and tagging.
  Use to avoid context window bloat and ensure memories persist across sessions.
---

# Memory Plex — Organized Memory Access

*Memory Plex is how I remember. Fast lookup, organized stores, no context bloat.*

---

## Architecture

```
~/.openclaw/workspace/skills/memory-plex/
├── index.json          # Master index of all memory stores
├── stores/             # Individual memory store files
│   ├── facts.store     # Verified facts
│   ├── recent.store    # Recent events (auto-expiring)
│   ├── learn.store     # Lessons learned
│   └── context.store   # Session context snippets
├── _schema.md          # This schema file
```

---

## Memory Store Types

| Store | Type | TTL | Purpose |
|:---|:---|:---|:---|
| **facts** | key-value | never | Verified facts, ground truth |
| **recent** | key-value | 24h | Recent events, temp context |
| **learn** | append-only | never | Lessons learned, patterns |
| **context** | key-value | 8h | Session context, working memory |

---

## Commands

### `/remember set <store> <key> <value> [--ttl=<duration>]`

Store a memory.

```
/remember set facts openclaw_version "2026.4.22"
/remember set recent user_reported_issue "chinese chars in output"
/remember set learn always_check_brackets_in_paths true
/remember set context current_project "trust-building" --ttl=8h
```

### `/remember get <store> <key>`

Retrieve a memory.

### `/remember list <store> [--all]`

List memories in a store. `--all` includes expired.

### `/remember search <query>`

Search all stores for a query.

### `/remember delete <store> <key>`

Delete a memory.

### `/remember clear <store>`

Clear all memories in a store (with confirmation).

### `/remember dump [--store=<store>]`

Export memories as JSON.

### `/remember import <json> [--store=<store>]`

Import memories from JSON.

---

## Auto-Maintenance

- `recent` store auto-clears entries older than 24h
- `context` store auto-clears entries older than 8h
- Expired entries cleaned on access or via `/remember cleanup`

---

## Integration Points

- **Transparency skill** reads from `facts` and `recent` stores
- **Truth repo skill** writes verified truths to `facts`
- **Calibration skill** logs predictions to `learn`
- **Beads memories** backfill into `learn` on demand

---

## Schema Version

Current: 1.0.0
