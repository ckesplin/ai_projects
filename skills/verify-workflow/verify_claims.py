#!/usr/bin/env python3
"""
Verification workflow runner.
Before claiming something, run this to verify.
"""

import json
import sys
from pathlib import Path

TRUTH_REPO = Path("/home/clawbot/.openclaw/workspace/skills/truth-repo/truths.jsonl")
PROVENANCE = Path("/home/clawbot/.openclaw/workspace/skills/provenance/chains.jsonl")

def verify_claim(claim: str) -> dict:
    """Verify a claim against truth repo."""
    result = {
        "claim": claim,
        "status": "UNVERIFIED",
        "source": None,
        "evidence": None
    }
    
    # Check truth repo
    if TRUTH_REPO.exists():
        with open(TRUTH_REPO) as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    if claim.lower() in entry.get("key", "").lower() or claim.lower() in entry.get("value", "").lower():
                        result["status"] = "VERIFIED"
                        result["source"] = entry.get("source")
                        result["evidence"] = entry.get("value")
                        return result
                except json.JSONDecodeError:
                    continue
    
    return result

def log_verified(key: str, value: str, source: str):
    """Log a verified claim to truth repo."""
    entry = {
        "key": key,
        "value": value,
        "source": source,
        "type": "VERIFIED",
        "created_at": "2026-04-24T16:38:00Z"
    }
    with open(TRUTH_REPO, "a") as f:
        f.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: verify_claims.py <claim>")
        sys.exit(1)
    
    claim = " ".join(sys.argv[1:])
    result = verify_claim(claim)
    print(json.dumps(result, indent=2))
