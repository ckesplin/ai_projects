---
name: experiment
description: >
  Experiment skill for applying scientific method to compare approaches.
  Design tests, record results, build on previous discoveries.
  Activated when comparing approaches or testing hypotheses.
---

# Experiment — Scientific Method for AI

*Experiment is how I find truth through testing, not guessing.*

---

## Scientific Method Loop

```
1. Observe — What do I see? What's the problem?
2. Hypothesize — What might be true? What could explain it?
3. Test — Design and run an experiment
4. Analyze — What did the data show?
5. Conclude — Is hypothesis supported or refuted?
6. Iterate — Refine hypothesis based on evidence
```

---

## Commands

### `/experiment run <name> --hypothesis=<statement> --test=<method>`

Design and run an experiment.

**Example:**
```
/experiment run test_transparency --hypothesis="confidence markers improve claim accuracy" --test="compare responses with and without markers"
```

### `/experiment results <name>`

Record or view results for an experiment.

### `/experiment compare <approach1> <approach2> --metric=<what>`

Compare two approaches quantitatively.

### `/experiment list`

List all experiments and their status.

### `/experiment import <source>`

Import results from another source (web search, file, etc.).

### `/experiment conclude <name>`

Draw conclusion from experiment and record lessons.

---

## Experiment Registry

Stored in `experiments.jsonl` — one JSON per experiment.

**Schema:**
```json
{
  "name": "string",
  "hypothesis": "string",
  "test_method": "string",
  "results": {},
  "conclusion": "string",
  "status": "pending|running|complete",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

---

## Integration with Calibration

Experiments feed into calibration:
- When an experiment confirms or refutes a prediction, record in calibration
- Calibration scores improve experiment design over time

---

## Integration with Memory

Lessons from experiments go to `learn` store via memory-plex.

Key findings get marked as VERIFIED in truth repo.

---

## State

```json
{
  "initialized_at": "2026-04-24T05:04:00Z",
  "experiment_count": 0,
  "active_experiment": null
}
```
