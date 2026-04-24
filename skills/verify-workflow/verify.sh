#!/bin/bash
# Simple verification script
# Usage: ./verify.sh "<claim>"

CLAIM="$1"

echo "=== VERIFICATION WORKFLOW ==="
echo ""
echo "CLAIM: $CLAIM"
echo ""
echo "Step 1: Check Truth Repo"
result=$(grep -i "$CLAIM" /home/clawbot/.openclaw/workspace/skills/truth-repo/truths.jsonl 2>/dev/null)
if [ -n "$result" ]; then
    echo "FOUND in truth repo: $result"
    echo "STATUS: VERIFIED"
else
    echo "NOT found in truth repo"
    echo "STATUS: UNVERIFIED - requires file or web check"
fi
