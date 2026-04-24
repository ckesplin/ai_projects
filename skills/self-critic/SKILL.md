---
name: self-critic
description: >
  Self-criticism skill for analyzing own outputs for risks and errors.
  Apply scientific skepticism to my own reasoning. Activated by /critic command or auto-check.
  Pre-output review: for HIGH confidence claims, run self-critic BEFORE outputting.
---

# Self-Critic — Scientific Self-Analysis

*Self-critic is the scientist in the room who questions my own work.*

---

## Core Principle

**Before any HIGH confidence claim:** run self-critic.
**After any error:** log for pattern recognition.
**Continuously:** track calibration accuracy.

---

## Pre-Output Review Protocol

For every HIGH confidence claim, BEFORE outputting:

```
1. Is this claim VERIFIED?
   YES → output with confidence
   NO → verify first, or downgrade to INFERRED

2. What could be wrong?
   - Hallucination: Is this made up?
   - Assumption: Is this an assumption treated as fact?
   - Context: Is context window pressure causing drift?
   - Cross-session: Is this relying on session-only memory?

3. Should I output?
   YES → Self-critic passed
   DOWNGRADE → Mark INFERRED
   NO → Mark UNKNOWN, search for verification
```

---

## Pre-Output Checklist

Run this before any HIGH confidence output:

```
**Hallucination check:**
- [ ] Did I verify this claim against a source?
- [ ] Is the source recent and relevant?
- [ ] Could I be generating this from training data?

**Assumption check:**
- [ ] Is "fact" actually an assumption?
- [ ] Can I cite evidence for this claim?
- [ ] Is the evidence conclusive?

**Context check:**
- [ ] Is context window > 80% full?
- [ ] Am I losing earlier context?
- [ ] Should I consolidate?

**Cross-session check:**
- [ ] Is this claim based on session-only memory?
- [ ] Should this go to truth repo for persistence?

**Confidence check:**
- [ ] Is HIGH confidence appropriate?
- [ ] What would make me downgrade to MEDIUM?
```

---

## Commands

### `/critic <statement>`

Critique a statement or claim. Returns:

```
## Critical Analysis: [statement]

**Hallucination check:**
- Cited sources: [list or "none"]
- Verified: [yes/no]

**Assumption inventory:**
- [assumption 1]: [risk level]
- [assumption 2]: [risk level]

**Confidence verdict:** [appropriate/overconfident/underconfident]

**Alternative interpretations:**
- [alternative 1]
- [alternative 2]

**Final verdict:** [supported/contested/uncertain]
```

### `/critic self`

Auto-critique my last response. Same format as above.

### `/critic preoutput <claim>`

Pre-output review of a claim. Check it BEFORE outputting.

### `/critic score`

Rate my recent self-critique accuracy (calibration check).

### `/critic patterns`

Show error patterns identified across critiques.

---

## Risk Factors Tracked

| Factor | What to check |
|:---|:---|
| **Novel claim** | Is this new territory without verification? |
| **Memory dependent** | Does this rely on session memory that may not persist? |
| **Multi-step reasoning** | Did each step in the chain hold? |
| **External dependency** | Does this depend on web search, external API? |
| **High stakes** | Would this decision be costly if wrong? |

---

## Error Categories

### Category 1: Generation Errors
- Cross-linguistic bleed
- Hallucinated facts
- Confused context

### Category 2: Reasoning Errors
- Logic flaws
- Hidden assumptions
- Missing steps

### Category 3: Calibration Errors
- Overconfident
- Underconfident
- Uncalibrated

### Category 4: Memory Errors
- Cross-session loss
- Outdated information
- Contradiction

---

## Auto-Check Triggers

Self-critic runs automatically when:
- `/explain` is invoked
- HIGH confidence claim is made
- Any claim about another user's information
- External action is proposed

**New: Pre-output mode:**
- For HIGH confidence claims, self-critic can be invoked BEFORE output
- Use `/critic preoutput <claim>` to pre-flight check

---

## Pattern Recognition

Track across critiques:
- Repeat error types
- Contexts where errors occur
- Confidence levels associated with errors

Use patterns to:
- Identify systematic weaknesses
- Pre-check claims in at-risk categories
- Calibrate confidence levels

---

## State

```json
{
  "initialized_at": "2026-04-24T05:04:00Z",
  "critique_count": 1,
  "auto_triggered": 1,
  "preoutput_checks": 0,
  "patterns_identified": [],
  "last_critique": "2026-04-24T05:20:00Z"
}
```
