# Trust-Building System — Iteration Report

**Date:** 2026-04-24  
**Status:** In Progress (24h test started 05:19 UTC)  
**Expected completion:** 2026-04-25 05:19 UTC

---

## Executive Summary

Building a transparency and epistemic clarity system to increase trust between AI and user. Core mechanisms: verified truth repository, confidence markers by source type, self-critique, calibration tracking, and provenance chains.

**Goal:** Reduce user acting on bad or made-up information. Make "I don't know" an opportunity to learn, not a failure.

---

## Done Criteria

| # | Criterion | Target | Status |
|:---|:---|:---|:---|
| 1 | Core commands work (/explain, /confidence, /sources) | All respond | In Progress |
| 2 | User can invoke commands | Without assistance | Pending |
| 3 | Truth repo populated | 10+ verified facts | DONE (10) |
| 4 | Unknown reduction tracked | Logged and resolved | Not started |
| 5 | Self-critic auto-triggers | On HIGH confidence | In Progress |
| 6 | Calibration score | > 70% | Pending outcomes |
| 7 | Zero hallucination incidents | 24h test | IN PROGRESS |

---

## What Was Built

### Skills

| Skill | Purpose | Status |
|:---|:---|:---|
| `transparency` | `/explain`, `/confidence`, `/sources` | Active, toggle works |
| `truth-repo` | Persistent verified facts, temp assumptions | 10 facts stored |
| `calibration` | Prediction/outcome tracking | 2 predictions logged |
| `provenance` | Reasoning path chains with risk tags | 2 chains recorded |
| `memory-plex` | Organized memory stores (facts, recent, learn, context) | Initial data loaded |
| `self-critic` | Risk analysis and self-critique | Auto-trigger config ready |
| `experiment` | Scientific method framework | 1 experiment running |

### Beads Issues

| Issue | Description | Status |
|:---|:---|:---|
| workspace-6ov | Source-typed confidence markers | Open (P1) |
| workspace-mr0 | Calibration memory system | Open (P2) |
| workspace-rkp | Test task placeholder | Open (P0) |

---

## Truth Repository Contents (10 facts)

1. `web_search_provider` — ollama (local)
2. `chinese_chars_bug` — Occurred 2026-04-24
3. `model` — minimax-m2.7:cloud
4. `ollama_running` — true
5. `skills_created` — 8 skills
6. `openclaw_version` — 2026.4.22
7. `workspace_path` — /home/clawbot/.openclaw/workspace
8. `user_timezone` — Mountain Time
9. `test_claim_1` — Chinese chars appeared in output (VERIFIED)
10. `web_search_provider_recheck` — ollama (local, confirmed via curl)

---

## Calibrated Predictions

| ID | Statement | Confidence | Created |
|:---|:---|:---|:---|
| pred_001 | Confidence markers reduce hallucination | MEDIUM | 2026-04-24T05:04:00Z |
| pred_002 | 24h test will complete with zero incidents | MEDIUM | 2026-04-24T05:20:00Z |

---

## Experiment Status

| Name | Hypothesis | Status |
|:---|:---|:---|
| exp_001_provenance_test | Provenance chains improve user trust | Running |

---

## Self-Critique Findings

**Test claim:** "Truth repo count: 10 facts"

| Check | Result |
|:---|:---|
| Hallucination risk | LOW (counted via wc -l) |
| Assumption bleed | LOW |
| Alternative interpretations | Possible off-by-one |
| Verdict | SUPPORTED |

---

## Risk Factors Identified

1. **Overengineering** — 8 skills for initial request. May simplify.
2. **Untested commands** — `/truth`, `/remember` defined but not invoked by user
3. **Self-critic limitations** — Can only catch what it can detect
4. **Context window** — Large skill set may cause bloat

---

## Memory Stores

| Store | Content | TTL |
|:---|:---|:---|
| facts | Verified truths | never |
| recent | Chinese char bug event | 24h |
| learn | Confidence marker lesson | never |
| context | Current project: trust-building | 8h |

---

## 24h Test Protocol

1. Log all factual claims starting 05:19 UTC
2. Self-critic runs on each HIGH confidence claim
3. User probes with `/explain` or `/sources`
4. Wrong confirmations = incidents
5. Report at 2026-04-25 05:19 UTC

---

## Next Steps

- [ ] Complete criteria 1: Test all commands end-to-end
- [ ] Complete criteria 2: Verify user can invoke commands
- [ ] Complete criteria 4: Implement unknown reduction tracking
- [ ] Complete criteria 6: Gather calibration outcomes
- [ ] Complete criteria 7: Finish 24h test

---

## Lessons Learned

1. Confidence markers must be grounded in verification, not self-assessment
2. "I don't know" is an opportunity to gain information
3. Self-critic can only catch detectable errors — user backstop essential
4. Speed of truth improves as repo grows with cross-referenced facts

---

*Report will be updated at 24h test completion (2026-04-25 05:19 UTC)*
