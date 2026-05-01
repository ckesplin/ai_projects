#!/bin/bash
# Memory statistics dashboard
# Output: entry counts, line counts, trends

WORKSPACE="/home/clawbot/.openclaw/workspace"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
TRUTH_REPO="$WORKSPACE/skills/truth-repo/truths.jsonl"
CALIB_PRED="$WORKSPACE/skills/calibration/predictions.jsonl"
CALIB_OUT="$WORKSPACE/skills/calibration/outcomes.jsonl"
MEMORY_DIR="$WORKSPACE/memory"

echo "=== Memory Stats Dashboard ==="
echo "Generated: $(date -Iseconds)"
echo ""

# MEMORY.md
if [ -f "$MEMORY_FILE" ]; then
    LINES=$(wc -l < "$MEMORY_FILE")
    echo "MEMORY.md: $LINES lines"
else
    echo "MEMORY.md: NOT FOUND"
fi

# truth-repo
if [ -f "$TRUTH_REPO" ]; then
    ENTRIES=$(wc -l < "$TRUTH_REPO")
    echo "truth-repo: $ENTRIES entries"
else
    echo "truth-repo: NOT FOUND"
fi

# calibration
if [ -f "$CALIB_PRED" ]; then
    PRED_COUNT=$(wc -l < "$CALIB_PRED")
    OUT_COUNT=$(wc -l < "$CALIB_OUT" 2>/dev/null || echo "0")
    echo "calibration: $PRED_COUNT predictions, $OUT_COUNT outcomes"
else
    echo "calibration: NOT FOUND"
fi

# daily logs
if [ -d "$MEMORY_DIR" ]; then
    LOG_COUNT=$(find "$MEMORY_DIR" -name "*.md" -type f | wc -l)
    echo "daily logs: $LOG_COUNT files"
    # Last modification
    LAST=$(find "$MEMORY_DIR" -name "*.md" -type f -printf '%T+\n' | sort -r | head -1)
    if [ -n "$LAST" ]; then
        echo "last log update: $LAST"
    fi
else
    echo "daily logs: NOT FOUND"
fi

# Skills directory check
SKILLS_DIR="$WORKSPACE/skills"
if [ -d "$SKILLS_DIR" ]; then
    echo "skills: $(ls -d $SKILLS_DIR/*/ 2>/dev/null | wc -l) directories"
fi

echo ""
echo "=== Recent Truths ==="
if [ -f "$TRUTH_REPO" ]; then
    tail -5 "$TRUTH_REPO" 2>/dev/null || true
fi

echo ""
echo "=== Calibration Score ==="
if [ -f "$CALIB_PRED" ] && [ -f "$CALIB_OUT" ]; then
    python3 "$WORKSPACE/skills/calibration/track.py" score 2>/dev/null || echo "(unable to compute)"
fi
