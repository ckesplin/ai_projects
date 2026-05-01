# Memory Architecture Report

## Situation

Current setup has multiple overlapping systems:
- MEMORY.md (human-written, curated)
- memory-plex stores (fragmented, mostly empty)
- truth-repo/truths.jsonl (17 entries, active)
- calibration stores (3 predictions, active)
- daily notes (directory doesn't exist)

Storage fragmentation will cause losses. The question is what architecture prevents that.

---

## Week Simulation

### Day 1 — Security Scanner
**Memory generated:**
- Pattern X catches secrets in YAML but not in .env
- User prefers false-positive over false-negative for API keys
- Scanner should skip node_modules by default
- Decision: include .tf and .vars files in Terraform scanning

### Day 2 — Multi-Agent Work
**Memory generated:**
- Subagents need 5+ iterations before converging on complex tasks
- Carson reviews one test at a time, not batches
- Prefer isolated sessions for parallel work, main for sequential
- learn: task type → agent configuration mapping

### Day 3 — External API Integration
**Memory generated:**
- Rate limit handling: exponential backoff with jitter
- API credentials rotate every 90 days, need refresh reminder
- Error messages should link to docs, not just describe the error
- learn: which error types require human attention

### Day 4 — Skill Improvement
**Memory generated:**
- Carson used `/plan` twice but never `/remember`
- Calibration tracking underutilized — I predict but forget to log
- Skill commands are friction — natural language capture works better
- learn: which skills actually get invoked vs documented

### Day 5 — Project Review
**Memory generated:**
- Project A went through 3 architecture changes before settling
- Reason for rejection: over-engineered for initial requirements
- Decision: start simple, add complexity only when justified
- Preference: incremental commits over feature branches

### Weekly Totals
- 20-30 discrete learnings (decisions, patterns, lessons)
- 5-10 verified facts (ground truths, user preferences)
- 3-5 predictions logged
- 2-3 open questions / blocked items
- 1-2 project state snapshots

---

## Extrapolation

### Month (4 weeks)
- 80-120 new learnings
- 20-40 new verified facts
- 12-20 new predictions
- MEMORY.md grows by ~50 lines if condensed weekly

### Year (12 months)
- 960-1,440 new learnings
- 240-480 new verified facts
- 144-240 new predictions
- **MEMORY.md becomes unusable** — 600+ lines without structure
- **JSONL stores grow** — truth-repo: 300+ entries, calibration: 200+ entries

---

## The Core Problem

| Storage Type | Problem at Scale |
|--------------|------------------|
| Flat files (MEMORY.md) | Must load everything to find anything |
| Append-only JSONL | Need filtering without full context load |
| Multiple stores | Sync overhead causes drift |

**The bottleneck isn't storage — it's retrieval under context constraints.**

I can store everything. I can't load everything when context is limited.

---

## Proposed Architecture

### Principle: Retrieval-Oriented Design

Design for the question "what do I need right now?" not "where should I put this?"

### Layer 1: Frequently Written, Frequently Read
**MEMORY.md** — but restructured with anchors

Current structure is linear. Proposed structure with section anchors:

```markdown
# USERprefs — never exceeds 50 lines
# MY_IDENTITY — static, 30 lines
# SECURITY — security lessons, 40 lines  
# PROJECT_STATE — current work summary, ~100 lines
# DECISIONS — high-impact decisions only, ~50 lines
```

Sections stay small. New content replaces old in same section, not appends.

### Layer 2: Structured Append-Only Stores
**Keep what works:**
- truth-repo/truths.jsonl — verified facts with source
- calibration/predictions.jsonl + outcomes.jsonl — confidence tracking

**Query pattern:** Never load full file. Use shell tools.

```bash
# Get facts about "user" without loading everything
grep "user" ~/.openclaw/workspace/skills/truth-repo/truths.jsonl

# Get calibration score without full context
tail -20 ~/.openclaw/workspace/skills/calibration/predictions.jsonl
```

### Layer 3: Daily Logs (auto-created)
**Path:** `memory/YYYY-MM-DD.md`

Format: one line per event, minimal structure

```markdown
## 2026-05-01
- scanner: added .tf pattern detection
- decision: skip node_modules by default
- learn: exponential backoff works for rate limits
- blocked: need Carson review of test_007
```

**Distillation:** Weekly heartbeat reads daily files and:
- Extract decisions → MEMORY.md/DECISIONS
- Extract verified facts → truth-repo
- Extract learnings → MEMORY.md or calibration/learn.store
- Archive or discard rest

---

## Tools and Skills Evolution

### Current Gap
memory_search uses semantic search on MEMORY.md. Skills have their own stores. No unified query interface.

### Proposed: Unified Retrieval Layer

Build a lightweight query script (`memory query <terms>`) that searches:
1. MEMORY.md (section-based grep)
2. truth-repo (grep by key or value)
3. calibration recent (tail + grep)
4. today's daily log (if exists)

**Example:**
```bash
$ memory query user preferences emoji
# Returns: MEMORY.md:USERprefs, truth-repo entries matching "emoji"
```

### Skills That Need Writing Attention

**self-critic:** After significant outputs, log:
- What I was uncertain about
- What I caught vs missed
- What I'd do differently

**experiment:** After A/B testing approaches:
- Hypothesis
- Test method
- Results summary
- Decision

**provenance:** For complex reasoning chains:
- Initial problem
- Steps taken
- Key decision points
- Conclusion

---

## External Libraries

### Candidate: sqlite for structured memory

JSONL is append-only but unindexed. SQLite solves this:

```python
import sqlite3

conn = sqlite3.connect('memory.db')
conn.execute('''
    CREATE TABLE IF NOT EXISTS truths (
        key TEXT PRIMARY KEY,
        value TEXT,
        source TEXT,
        type TEXT,
        created_at TIMESTAMP
    )
''')

# Query without loading everything
conn.execute('SELECT * FROM truths WHERE key LIKE ?', ('%user%',))
```

**Pros:** Indexable, queryable, relational
**Cons:** External dependency, more complex than JSONL

### Candidate: jq for JSONL manipulation

```bash
# Extract all entries of type VERIFIED
cat truths.jsonl | jq 'select(.type == "VERIFIED")'

# Get recent facts only
cat truths.jsonl | jq -s 'sort_by(.created_at) | reverse | .[:10]'
```

**Pros:** Native JSONL processing, no new dependency
**Cons:** Still requires loading into context for complex queries

### Candidate: semantic search (local embeddings)

For conceptual recall — "what did we learn about error handling?" when you don't remember the exact phrase.

```python
# Pseudocode using sentence-transformers
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
query_embedding = model.encode("error handling patterns")
# Compare against stored embeddings, return top-k matches
```

**Pros:** Matches intent, not keywords
**Cons:** Requires embedding model, more complexity

---

## Recommendations

### Immediate (this week)
1. Create `memory/` directory, start daily logging
2. Add section anchors to MEMORY.md
3. Write `memory query` script for unified retrieval
4. Drop memory-plex (stores are empty, skills have their own)

### Short-term (this month)
1. Enable auto-distillation in weekly heartbeat
2. Add sqlite backing for truth-repo if JSONL exceeds 500 entries
3. Instrument calibration — log predictions more consistently
4. Add daily log rotation: keep 7 days hot, archive older

### Medium-term (this quarter)
1. Evaluate semantic search if conceptual recall feels limited
2. Add provenance logging for complex multi-step reasoning
3. Build a simple dashboard: `memory stats` showing entry counts by store
4. Consider auto-summary of MEMORY.md sections to keep them bounded

---

## What This Requires From Me

- **Proactive capture:** Not wait to be asked — log significant events
- **Regular distillation:** Weekly review of daily logs
- **Query discipline:** Use tools to retrieve, not dump everything into context
- **Honesty about uncertainty:** If I don't know something, say it rather than filling gaps with plausible guesses

---

## Open Questions

1. **Granularity tradeoff:** One line per event in daily logs vs richer structure?
2. **Archive strategy:** When do old daily logs get collapsed/summarized?
3. **Skills vs stores:** Should self-critic/experiment write to JSONL or MEMORY.md sections?
4. **Trust threshold:** How many times must something be verified before it becomes a "ground truth"?

---

## Summary

Simplify to three layers:
- **MEMORY.md** — curated, sectioned, human-written
- **JSONL stores** — append-only, tool-queried (truth-repo, calibration)
- **Daily logs** — raw capture, auto-created, weekly distillation

Tools support retrieval without context bloat. Skills write to stores when they run.

Drop memory-plex. Let skills own their stores. Build unified query layer on top.

---

*Report generated: 2026-04-30*
*Next review: 2026-05-07*
