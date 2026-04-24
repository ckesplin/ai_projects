---
name: verify-workflow
description: >
  Verification-first workflow for all factual claims.
  Before outputting, verify against truth repo, files, or web.
  Implements zero-trust stance: verify before claiming.
---

# Verify Workflow — Zero Trust Claim System

*Before any claim: verify. Before any output: check sources.*

---

## The Problem

My default mode is generate-first, verify-later (or not at all).
This leads to hallucination, unverified claims, and trust erosion.

## The Solution

**Verification-first workflow:**

```
CLAIM → VERIFY → LOG → OUTPUT → CALIBRATE
```

Each step has a job. Nothing skips steps.

---

## Claim Classification

| Level | Meaning | Required action |
|:---|:---|:---|
| **VERIFIED** | Evidence confirmed via file/web/truth repo | Cite source |
| **INFERRED** | Reasoning from evidence, could be wrong | Show chain |
| **UNVERIFIED** | No evidence, could be wrong | Mark explicitly |
| **REJECTED** | Evidence contradicts | Don't output |

---

## Pre-Output Verification Protocol

For every factual claim, do this BEFORE outputting:

### Step 1: Check Truth Repo

```bash
# Look for the claim in truths.jsonl
grep "<key>" truths.jsonl
```

- FOUND → Output as VERIFIED, cite the truth repo key
- NOT FOUND → Continue to Step 2

### Step 2: Check Relevant Files

```bash
# Read the file and verify
cat <file>
# Or use grep for specific content
grep "<pattern>" <file>
```

- Verified → Output as VERIFIED, cite file path
- Not found or uncertain → Continue to Step 3

### Step 3: Web Search (if claim about external world)

```bash
# Use web_search tool
web_search --query "<claim to verify>"
```

- Confirmed → Output as VERIFIED, cite search results
- Contradicted → Mark REJECTED, don't output
- Inconclusive → Output as INFERRED with source

### Step 4: Log and Output

```bash
# Log novel VERIFIED claims
echo '{"key":"<key>","value":"<value>","source":"<source>","type":"VERIFIED","created_at":"<timestamp>"}' >> truths.jsonl

# Log INFERRED claims to provenance
echo '<provenance chain>' >> chains.jsonl
```

---

## Post-Output Actions

### Calibration (for predictions)

```bash
# Log prediction BEFORE stating
echo '{"id":"<id>","statement":"<statement>","confidence":"<level>","created_at":"<timestamp>"}' >> predictions.jsonl

# Record outcome AFTER verification
echo '{"id":"<id>","result":"CORRECT/INCORRECT","outcome":"<actual>","verified_at":"<timestamp>"}' >> outcomes.jsonl
```

### Self-Critique (for HIGH confidence claims)

```bash
# Self-critic runs on HIGH confidence claims
# Review the claim against evidence
# Flag if questionable
```

---

## Quick Verification Commands

### `/verify <claim>`

Check a claim against all sources.

### `/verify-file <file> <pattern>`

Verify content exists in a file.

### `/verify-web <query>`

Search web and verify claim.

### `/verified`

List all verified truths in truth repo.

### `/unverified`

List claims that need verification.

---

## State File

```json
{
  "initialized_at": "2026-04-24T16:38:00Z",
  "claims_verified": 0,
  "claims_inferred": 0,
  "claims_rejected": 0,
  "last_verification": null
}
```

---

## Integration

- **Truth repo**: Verified claims stored here
- **Provenance**: Inferred claims logged here  
- **Calibration**: Predictions and outcomes here
- **Self-critic**: Flags questionable claims
- **Memory-plex**: Learn lessons here

---

## The Core Rule

**Never output a factual claim without verification evidence.**

If you can't verify it: say so, mark UNVERIFIED, or search until you can.

---
