# Memory Architecture — Running Report

*A living document. Append entries as work progresses.*

---

## Changelog

| Date | Entry | Summary |
|------|-------|---------|
| 2026-04-30 | Initial Analysis | Simulated week, extrapolated to year. Identified fragmentation problem. |
| 2026-05-01 | Architecture Decision | 3-layer architecture chosen: MEMORY.md + JSONL stores + daily logs |
| 2026-05-01 | Phase 1 Complete | Directory structure, MEMORY.md restructured, query scripts, memory-plex deprecated |
| 2026-05-01 | Heartbeat Updated | Daily log creation, calibration logging, distillation cadence enabled |

---

## Entry: 2026-04-30 — Initial Analysis

### Situation

Multiple overlapping systems causing fragmentation:
- MEMORY.md (human-written, curated)
- memory-plex stores (mostly empty)
- truth-repo/truths.jsonl (17 entries)
- calibration stores (3 predictions)
- daily notes (directory missing)

### Week Simulation

| Day | Work Area | Memory Generated |
|-----|-----------|------------------|
| 1 | Security Scanner | Pattern detection decisions |
| 2 | Multi-Agent Work | Task → agent config mapping |
| 3 | API Integration | Rate limit handling patterns |
| 4 | Skill Improvement | Skill usage vs documentation |
| 5 | Project Review | Architecture rejection reasons |

**Weekly totals:** 20-30 learnings, 5-10 facts, 3-5 predictions, 2-3 open questions

### Extrapolation

- **Month:** 80-120 learnings, MEMORY.md +50 lines if distilled weekly
- **Year:** MEMORY.md 600+ lines (unusable), truth-repo 300+ entries

### Core Problem

Not storage — retrieval under context constraints.

### Proposed Architecture

**3 layers:**
1. **MEMORY.md** — curated, sectioned (not flat)
2. **JSONL stores** — truth-repo, calibration (append-only, tool-queried)
3. **Daily logs** — raw capture, auto-created, weekly distillation

### Tools Considered

- `sqlite` — indexed queries if >500 entries
- `jq` — JSONL processing
- `semantic search` — conceptual recall (deferred)

### Recommendations

| Timeline | Actions |
|----------|---------|
| Immediate | Create memory/, add anchors, write query script, drop memory-plex |
| Short-term | Enable distillation, instrument calibration, log rotation |
| Medium-term | Semantic search evaluation, provenance logging, stats dashboard |

---

## Entry: 2026-05-01 — Architecture Decision

### Decision Made

Simplify to 3 layers. Skills own their stores. memory-plex deprecated.

### Migration Path

| Was | Now |
|:---|:---|
| memory-plex/facts.store | truth-repo/truths.jsonl |
| memory-plex/recent.store | memory/YYYY-MM-DD.md |
| memory-plex/learn.store | MEMORY.md/LEARNED |
| memory-plex/context.store | Daily logs + session |

### Directory Structure Created

```
workspace/
├── memory/              # Daily logs (gitignored)
├── reports/             # Formal reports
├── scripts/             # Query and stats tools
├── MEMORY.md            # Curated, sectioned
└── skills/
    ├── truth-repo/      # Verified facts (JSONL)
    ├── calibration/     # Predictions/outcomes (JSONL)
    └── memory-plex/     # DEPRECATED
```

### Context Window

- **minimax-m2.7:cloud** — 200K tokens (benchlm.ai, stored 2026-05-01)
- Context usage baseline: 56k/197k (29%)

---

## Entry: 2026-05-01 — Phase 1 Complete

### Completed

| Component | Status | Verification |
|-----------|--------|---------------|
| Directory structure | DONE | memory/, reports/, scripts/ exist |
| MEMORY.md restructured | DONE | 90 lines (was 108), 7 section anchors |
| Query script | DONE | memory_query.sh tested |
| Stats script | DONE | memory_stats.sh tested |
| memory-plex deprecated | DONE | SKILL.md updated |

### MEMORY.md Sections

```
# USERprefs       — user preferences (max ~50 lines)
# MY_IDENTITY     — who I am (max ~30 lines)
# SECURITY        — security lessons (max ~40 lines)
# PROJECT         — current state (~100 lines)
# DECISIONS       — high-impact decisions only (~50 lines)
# LEARNED         — distilled lessons (~100 lines)
# CONTEXT_WINDOW  — model context windows
```

### Scripts Created

- `scripts/memory_query.sh` — unified search across stores
- `scripts/memory_stats.sh` — dashboard output

### Baseline Stats (2026-05-01)

```
MEMORY.md: 90 lines
truth-repo: 18 entries
calibration: 3 predictions, 1 outcome
daily logs: 2 files
context usage: 29%
```

---

## Entry: 2026-05-01 — Heartbeat Updated

### New Heartbeat Tasks

1. **Daily Log Check** — create if not exists
2. **Calibration Logging** — log predictions, check pending outcomes
3. **Weekly Distillation** — run if 7+ days since last
4. **Weekly Stats** — run if 7+ days since last

### Cadence

- **Heartbeat:** every ~30 min (checks batched)
- **Distillation:** weekly (triggered by heartbeat)
- **Stats:** weekly (triggered by heartbeat)
- **Phase cadence:** removed — act immediately, analyze weekly

### Note

`memory/` directory is gitignored (raw logs may contain sensitive content). Stats tracked via script only.

---

## Entry: 2026-05-07 — [PENDING]

*To be filled after first weekly review*

---

## Success Metrics (Track Weekly)

| Metric | Target | Actual |
|--------|--------|--------|
| Daily logs created | 7/7 days | — |
| Entries distilled | 5+/week | — |
| Calibration predictions | 3+/week | — |
| Calibration score | >70% | — |
| Forgotten items | decreasing | — |
| MEMORY.md size | <150 lines | 90 |

---

## Open Questions (Deferred)

1. Daily log granularity — one line vs richer structure?
2. Archive strategy — when do old logs get summarized?
3. Skills vs stores — where write self-critic/experiment output?
4. Trust threshold — verifications before ground truth?

---

*Report maintained: append entries above. Remove this section when question resolved.*
