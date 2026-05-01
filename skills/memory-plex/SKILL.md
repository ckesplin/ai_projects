<!-- DEPRECATED 2026-05-01 -->
<!--
This skill is deprecated. The 3-layer memory architecture is now preferred:
- MEMORY.md (curated, sectioned)
- JSONL stores owned by skills (truth-repo, calibration)
- Daily logs (memory/YYYY-MM-DD.md)

Migration: Skills own their own stores. memory-plex stores are empty.
See: reports/2026-05-01-memory-process-plan.md
-->

---
name: memory-plex
description: |
  DEPRECATED 2026-05-01. Use 3-layer architecture instead:
  MEMORY.md + truth-repo/calibration stores + daily logs.
  See reports/2026-05-01-memory-process-plan.md
---

# Memory Plex — Organized Memory Access

*DEPRECATED: This skill is no longer maintained.*

Memory Plex was an attempt to provide indexed memory stores with quick lookup, expiration, and tagging. It has been replaced by a simpler 3-layer architecture.

## Why Deprecated

- Stores were mostly empty — skills already had their own
- Fragmentation caused sync drift between memory-plex and truth-repo
- Simple is more robust than complex

## Migration Path

| Was | Now |
|:---|:---|
| facts.store | truth-repo/truths.jsonl |
| recent.store | memory/YYYY-MM-DD.md (daily logs) |
| learn.store | MEMORY.md/LEARNED section |
| context.store | Daily logs + session context |

## What Still Works

- Existing stores remain readable but are no longer written to
- `/remember` commands still function but log deprecation warning
- Query fallback to truth-repo if memory-plex search fails

## Architecture (ARCHIVED)

```
~/.openclaw/workspace/skills/memory-plex/
├── index.json          # Master index of all memory stores
├── stores/             # Individual memory store files
│   ├── facts.store     # Verified facts (now: truth-repo)
│   ├── recent.store    # Recent events (now: daily logs)
│   ├── learn.store     # Lessons learned (now: MEMORY.md)
│   └── context.store   # Session context (now: daily logs)
├── _schema.md          # This schema file
```

## Commands (DEPRECATED)

All `/remember` commands are deprecated. Use:
- truth-repo for verified facts
- daily logs for events and context
- MEMORY.md for curated learnings

## Schema Version

Current: 1.0.0 (deprecated)
