#!/bin/bash
# Unified memory query script
# Searches: MEMORY.md sections, truth-repo, calibration recent, today's daily log
# Usage: ./memory_query.sh <terms>

set -e

WORKSPACE="/home/clawbot/.openclaw/workspace"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
TRUTH_REPO="$WORKSPACE/skills/truth-repo/truths.jsonl"
CALIB_PRED="$WORKSPACE/skills/calibration/predictions.jsonl"
CALIB_OUT="$WORKSPACE/skills/calibration/outcomes.jsonl"
TODAY_LOG="$WORKSPACE/memory/$(date +%Y-%m-%d).md"

if [ -z "$1" ]; then
    echo "Usage: $0 <search terms...>"
    echo "Example: $0 user preferences"
    exit 1
fi

SEARCH_TERM="$1"
RESULTS_FILE=$(mktemp)

echo "=== Memory Query Results for: $SEARCH_TERM ===" >> "$RESULTS_FILE"
echo "Timestamp: $(date -Iseconds)" >> "$RESULTS_FILE"
echo "" >> "$RESULTS_FILE"

# Search MEMORY.md (section-based)
if [ -f "$MEMORY_FILE" ]; then
    MATCHES=$(grep -i -n "$SEARCH_TERM" "$MEMORY_FILE" 2>/dev/null || true)
    if [ -n "$MATCHES" ]; then
        echo "--- MEMORY.md ---" >> "$RESULTS_FILE"
        echo "$MATCHES" >> "$RESULTS_FILE"
        echo "" >> "$RESULTS_FILE"
    fi
fi

# Search truth-repo
if [ -f "$TRUTH_REPO" ]; then
    MATCHES=$(grep -i "$SEARCH_TERM" "$TRUTH_REPO" 2>/dev/null || true)
    if [ -n "$MATCHES" ]; then
        echo "--- Truth Repository ---" >> "$RESULTS_FILE"
        echo "$MATCHES" >> "$RESULTS_FILE"
        echo "" >> "$RESULTS_FILE"
    fi
fi

# Search calibration predictions
if [ -f "$CALIB_PRED" ]; then
    MATCHES=$(grep -i "$SEARCH_TERM" "$CALIB_PRED" 2>/dev/null || true)
    if [ -n "$MATCHES" ]; then
        echo "--- Calibration Predictions ---" >> "$RESULTS_FILE"
        echo "$MATCHES" >> "$RESULTS_FILE"
        echo "" >> "$RESULTS_FILE"
    fi
fi

# Search today's daily log
if [ -f "$TODAY_LOG" ]; then
    MATCHES=$(grep -i "$SEARCH_TERM" "$TODAY_LOG" 2>/dev/null || true)
    if [ -n "$MATCHES" ]; then
        echo "--- Today's Daily Log ---" >> "$RESULTS_FILE"
        echo "$MATCHES" >> "$RESULTS_FILE"
        echo "" >> "$RESULTS_FILE"
    fi
fi

# Output results
if [ -s "$RESULTS_FILE" ]; then
    cat "$RESULTS_FILE"
else
    echo "No results found for: $SEARCH_TERM"
fi

rm -f "$RESULTS_FILE"
