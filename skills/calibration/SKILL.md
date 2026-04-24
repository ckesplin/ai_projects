---
name: calibration
description: >
  Calibration memory system for tracking prediction accuracy over time.
  Log predictions and outcomes to measure and improve confidence marker reliability.
  Activated when making predictions or recording outcomes.
---

# Calibration — Confidence Marker Accuracy Tracking

*Calibration builds trust by making confidence markers honest over time.*

---

## How It Works

Over time, I log:
1. **What I predicted** (with confidence level)
2. **What actually happened**
3. **Whether my confidence was right**

This lets me detect drift — when my HIGH confidence claims are often wrong, the markers lose meaning. Calibration corrects that.

---

## Commands

### `/calibrate predict <statement> --confidence=<HIGH|MEDIUM|LOW>`

Log a prediction. I note what I believe and how confident I am.

### `/calibrate outcome <id> <result>`

Record what actually happened. Result is: CORRECT / PARTIAL / WRONG.

### `/calibrate score`

Show calibration score — how well my confidence levels match reality.

### `/calibrate recent`

Show recent predictions and outcomes.

---

## Storage

```
~/.openclaw/workspace/skills/calibration/
├── predictions.jsonl   # Log of predictions with timestamps
├── outcomes.jsonl       # Log of outcomes
└── state.json          # Running calibration stats
```

---

## Calibration Score

Score format: `X% accurate at Y% confidence`

Example: "72% accurate at HIGH confidence" means my HIGH confidence predictions were correct 72% of the time.

**Target thresholds:**
- HIGH confidence: should be right 90%+ of the time
- MEDIUM: should be right 70%+ of the time
- LOW: should be right 50%+ of the time

If actual accuracy falls below threshold, markers are miscalibrated and need adjustment.

---

## State File

```json
{
  "initialized_at": "2026-04-24T04:53:00Z",
  "total_predictions": 0,
  "high_correct": 0,
  "high_total": 0,
  "medium_correct": 0,
  "medium_total": 0,
  "low_correct": 0,
  "low_total": 0
}
```
