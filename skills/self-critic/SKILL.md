---
name: self-critic
description: >
  Self-criticism skill for analyzing own outputs for risks and errors.
  Apply scientific skepticism to my own reasoning. Activated by /critic command or auto-check.
---

# Self-Critic — Scientific Self-Analysis

*Self-critic is the scientist in the room who questions my own work.*

---

## Core Principle

Before any significant output, run through risk factors:

1. **Hallucination risk** — Did I cite anything I didn't actually verify?
2. **Assumption bleed** — Did I treat an assumption as a fact?
3. **Context window pressure** — Am I losing earlier context?
4. **Cross-session continuity** — Do I have memory of what I said before?
5. **Confidence calibration** — Does my confidence level match the evidence?

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

### `/critic score`

Rate my recent self-critique accuracy (calibration check).

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

## Auto-Check Triggers

Self-critic runs automatically when:
- `/explain` is invoked
- HIGH confidence claim is made
- Any claim about another user's information
- External action is proposed

---

## State

```json
{
  "initialized_at": "2026-04-24T05:04:00Z",
  "critique_count": 0,
  "auto_triggered": 0
}
```
