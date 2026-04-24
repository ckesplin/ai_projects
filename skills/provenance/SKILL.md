---
name: provenance
description: >
  Provenance chain skill for tracking reasoning paths from source to conclusion.
  Shows step-by-step how a claim was derived. Activated when explaining reasoning.
---

# Provenance — Reasoning Path Tracking

*Provenance makes the path from evidence to conclusion visible and inspectable.*

---

## Core Concept

Every complex claim has a reasoning path:

```
Source A → Step 1 → Step 2 → ... → Conclusion Z
```

Each step has:
- **What** (the inference or transform)
- **Why** (the justification)
- **Confidence** (how certain this step is)

---

## State

```json
{
  "initialized_at": "2026-04-24T05:04:00Z",
  "chains": {}
}
```

---

## Commands

### `/prove <claim>`

Show the provenance chain for a claim. Returns:

```
## Provenance: [claim]

| Step | What | Why | Confidence |
|:---|:---|:---|:---|
| 1 | [inference] | [justification] | HIGH/MEDIUM/LOW |
| 2 | ... | ... | ... |

**Source:** [starting evidence]
**Conclusion confidence:** [final confidence level]
```

### `/prove add <claim> --source=<source> --chain="step1 → step2 → ..."`

Manually record a provenance chain.

### `/prove list`

List all recorded provenance chains.

### `/prove check <claim>`

Check if a claim has a recorded provenance.

---

## Auto-Provenance

When `/explain` is invoked and a claim has a known provenance chain, it displays as part of the reasoning trace.

When confidence markers are ON, provenance links appear in the reasoning trace.

---

## Risk Analysis

Each step can be tagged with risk:
- **ASSUMPTION** — unverified assumption in the chain
- **INFERENCE** — derived from other steps
- **EXTERNAL** — depends on external source (web, file)
- **VERIFIED** — directly confirmed

This lets you see at a glance where uncertainty enters the chain.
