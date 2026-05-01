# Memory Process Project — Implementation Plan

## Overview

This is an **outcome project** with a **process discipline**: build the systems and discipline to achieve measurable memory improvements over time. The goal is improved recall effectiveness, not just following a process.

Every component has verification, regular review cadence, and improvement loops with measurable success criteria.

---

## Phase 1: Foundation (Week 1)

### 1.1 Create Directory Structure

**Actions:**
- [x] Create `memory/` directory (exists, report moved)
- [x] Create `reports/` directory (done)
- [x] Document directory structure in AGENTS.md (added Reports section)
- [x] Created `scripts/` directory with query and stats tools

**Data to gather:**
- List current directory structure
- Identify any missing parent directories

**Verification:**
- `ls -la memory/` shows directory exists
- Report exists in `reports/`
- Scripts are executable and tested

**Cadence:** One-time setup — COMPLETE

---

### 1.2 Restructure MEMORY.md with Section Anchors — COMPLETE

**Actions:**
- [x] Rewrote MEMORY.md with section anchors (USERprefs, MY_IDENTITY, SECURITY, PROJECT, DECISIONS, LEARNED, CONTEXT_WINDOW)
- [x] Reduced to 90 lines (was ~108)
- [x] Added review date comment

**Verification:**
- `wc -l MEMORY.md` = 90 lines
- All anchors present via HTML comments
- Human-readable without context loading

**Status:** COMPLETE 2026-05-01

---

### 1.3 Build Unified Query Script — COMPLETE

**Actions:**
- [x] Created `scripts/memory_query.sh`
- [x] Created `scripts/memory_stats.sh`
- [x] Tested — working with `user` query

**Verification:**
- `./memory_query.sh user` returns relevant results
- `./memory_stats.sh` shows correct counts (MEMORY.md: 90, truth-repo: 18, calibration: 3/1)
- No secrets exposed

**Status:** COMPLETE 2026-05-01

---

### 1.4 Deprecate memory-plex — COMPLETE

**Actions:**
- [x] Updated SKILL.md with deprecation notice
- [x] Documented migration path
- [x] Confirmed truth-repo and calibration work independently

**Verification:**
- memory-plex stores remain but unused
- truth-repo has 18 entries, calibration has 3 predictions
- Skills own their stores

**Status:** COMPLETE 2026-05-01

---

## Phase 1 Summary — COMPLETE 2026-05-01

| Component | Status | Verification |
|-----------|--------|---------------|
| Directory structure | COMPLETE | memory/, reports/, scripts/ exist |
| MEMORY.md restructured | COMPLETE | 90 lines, section anchors |
| Query script | COMPLETE | Tested, working |
| memory-plex deprecated | COMPLETE | SKILL.md updated |

**Next phase starts:** 2026-05-07 (Phase 2: Query Layer)

---

## Phase 2: Query Layer (Week 2)

### 2.1 Token Tracking

**Actions:**
- [ ] Create `scripts/token_estimator.py` or use existing session tracking
- [ ] Store token counts periodically during long sessions
- [ ] Log when context exceeds 50%, 75%, 90% thresholds

**Data to gather:**
- Token count at session start, mid-session, end
- Threshold crossings per session

**Verification:**
- Token logs created during session
- Threshold crossings noted in daily log

**Cadence:** Every session, logged to daily

---

### 2.2 Calibration Instrument

**Actions:**
- [ ] Enable calibration skill — log predictions consistently
- [ ] Create reminder in heartbeat for pending outcomes
- [ ] Track calibration score over time

**Data to gather:**
- Predictions logged per week
- Outcome resolution rate
- Calibration score trend

**Verification:**
- `python3 skills/calibration/track.py score` works
- Score improves or stays stable over 4 weeks

**Cadence:** Log every prediction; score monthly

---

### 2.3 Daily Log Auto-creation

**Actions:**
- [ ] Heartbeat creates `memory/YYYY-MM-DD.md` if not exists
- [ ] Format: one line per event, minimal structure
- [ ] Archive logs older than 7 days (compress)

**Data to gather:**
- Daily log entry count per day
- Events captured: decisions, learnings, blocked items, facts

**Verification:**
- Daily log exists for today with timestamp header
- Older logs compressed after 7 days

**Cadence:** Daily creation, weekly archive

---

## Phase 3: Refinement (Week 3-4)

### 3.1 Auto-Distillation

**Actions:**
- [ ] Weekly heartbeat reads daily files
- [ ] Extract: decisions → MEMORY.md/DECISIONS
- [ ] Extract: verified facts → truth-repo
- [ ] Extract: learnings → MEMORY.md/LEARNED
- [ ] Archive or discard processed logs

**Data to gather:**
- Entries distilled per week
- MEMORY.md growth rate
- truth-repo entries added

**Verification:**
- MEMORY.md/DECISIONS has new entries from past week
- truth-repo has new verified facts
- Daily logs show distillation marker

**Cadence:** Weekly (every Sunday)

---

### 3.2 Memory Stats Dashboard

**Actions:**
- [ ] Create `scripts/memory_stats.sh`:
  ```bash
  # Output:
  # MEMORY.md: X lines
  # truth-repo: X entries
  # calibration: X predictions, X outcomes, score: X
  # daily logs: X days
  # last distillation: YYYY-MM-DD
  ```
- [ ] Run on demand and include in weekly review

**Data to gather:**
- Store entry counts over time
- MEMORY.md line count over time

**Verification:**
- Stats match actual counts
- Trends visible across weeks

**Cadence:** Weekly, on-demand

---

### 3.3 SQLite Evaluation

**Actions:**
- [ ] Monitor truth-repo JSONL size
- [ ] If > 500 entries, evaluate sqlite migration
- [ ] Create migration script if needed

**Data to gather:**
- truth-repo entry count per week
- JSONL file size
- Query performance before/after

**Verification:**
- SQLite query returns same results as JSONL
- Performance improved

**Cadence:** Monthly evaluation

---

## Phase 4: Improvement Over Time (Ongoing)

### 4.1 Monthly Review Process

**Actions:**
- [ ] First week of month: review previous month's memory
- [ ] Analyze: what was remembered well? What was lost?
- [ ] Identify: patterns in forgotten items
- [ ] Adjust: capture discipline, storage strategy, query approach

**Data to gather:**
- MEMORY.md growth
- Forgotten items (things that needed re-explanation)
- Query frequency data

**Verification:**
- Review documented in memory/YYYY-MM-monthly-review.md
- Adjustments made and tested

**Cadence:** Monthly (first week)

---

### 4.2 Calibration Score Tracking

**Actions:**
- [ ] Track calibration score per week
- [ ] Goal: score improves or stays above 70%
- [ ] If score drops, analyze why

**Data to gather:**
- Weekly calibration score
- Predictions vs outcomes ratio
- High-confidence prediction accuracy

**Verification:**
- Scorecard in memory/calibration-trend.md
- If score < 60% for 2 weeks, investigate

**Cadence:** Weekly score, monthly analysis

---

### 4.3 Query Effectiveness Survey

**Actions:**
- [ ] After each project milestone, ask: "Did memory help?"
- [ ] Track: queries that returned useful info
- [ ] Track: queries that returned nothing useful

**Data to gather:**
- Query success rate
- False negative rate (should have found but didn't)

**Verification:**
- Metrics in memory/query-effectiveness.md
- Process adjusted based on findings

**Cadence:** Per milestone

---

## Verification Schedule

| Component | Initial Verification | Regular Verification |
|-----------|---------------------|---------------------|
| Directory structure | `ls` check | Monthly |
| MEMORY.md sections | Line count, readability | Weekly distill |
| Query script | Manual test queries | Weekly stats |
| memory-plex deprecation | Skills still work | Quarterly |
| Token tracking | Session log exists | Per session |
| Calibration | Score visible | Weekly score |
| Daily log creation | Today's log exists | Daily |
| Auto-distillation | MEMORY.md updated | Weekly |
| Stats dashboard | Output matches reality | Monthly |
| SQLite evaluation | Query equivalence | Monthly |

---

## Success Metrics

**Process metrics (measure the system):**
- Daily logs created: target 7/7 days
- Entries distilled: target 5+ per week
- Calibration predictions logged: target 3+ per week
- Query script usage: track monthly

**Outcome metrics (measure effectiveness):**
- Forgotten items: count per week (should decrease)
- Context reloads needed: count per session (should decrease)
- MEMORY.md size: stays bounded (< 400 lines)
- Calibration score: stays above 70%

---

## Document Changelog

| Date | Change | Notes |
|------|--------|-------|
| 2026-05-01 | Created | Initial implementation plan |
| 2026-05-01 | Phase 1-4 defined | Foundation through improvement |

---

*Next review: 2026-05-07 (Phase 1 verification)*
