#!/usr/bin/env python3
"""
Calibration tracking script.
Track predictions and calculate accuracy score.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

PREDICTIONS = Path("/home/clawbot/.openclaw/workspace/skills/calibration/predictions.jsonl")
OUTCOMES = Path("/home/clawbot/.openclaw/workspace/skills/calibration/outcomes.jsonl")

def load_jsonl(path):
    """Load JSONL file."""
    if not path.exists():
        return []
    with open(path) as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

def save_jsonl(path, entries):
    """Save JSONL file."""
    with open(path, "w") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")

def add_prediction(statement, confidence, created_at=None):
    """Add a new prediction."""
    if created_at is None:
        created_at = datetime.utcnow().isoformat() + "Z"
    
    predictions = load_jsonl(PREDICTIONS)
    pred_id = f"pred_{len(predictions)+1:03d}"
    
    prediction = {
        "id": pred_id,
        "statement": statement,
        "confidence": confidence,
        "created_at": created_at
    }
    predictions.append(prediction)
    save_jsonl(PREDICTIONS, predictions)
    
    print(f"Added prediction {pred_id}: {statement} ({confidence})")
    return pred_id

def record_outcome(pred_id, result, outcome="", verified_at=None):
    """Record the outcome of a prediction."""
    if verified_at is None:
        verified_at = datetime.utcnow().isoformat() + "Z"
    
    outcomes = load_jsonl(OUTCOMES)
    
    # Check if outcome already exists
    for o in outcomes:
        if o.get("id") == pred_id:
            o["result"] = result
            o["outcome"] = outcome
            o["verified_at"] = verified_at
            save_jsonl(OUTCOMES, outcomes)
            print(f"Updated outcome for {pred_id}: {result}")
            return
    
    outcome_entry = {
        "id": pred_id,
        "result": result,
        "outcome": outcome,
        "verified_at": verified_at
    }
    outcomes.append(outcome_entry)
    save_jsonl(OUTCOMES, outcomes)
    
    print(f"Recorded outcome for {pred_id}: {result}")

def calculate_score():
    """Calculate calibration score."""
    predictions = load_jsonl(PREDICTIONS)
    outcomes = load_jsonl(OUTCOMES)
    
    # Build outcome lookup
    outcome_lookup = {o["id"]: o for o in outcomes}
    
    # Calculate by confidence level
    levels = {"HIGH": [], "MEDIUM": [], "LOW": []}
    
    for pred in predictions:
        pred_id = pred["id"]
        confidence = pred["confidence"]
        
        if pred_id in outcome_lookup:
            result = outcome_lookup[pred_id]["result"]
            is_correct = result == "CORRECT"
            levels[confidence].append(is_correct)
    
    # Calculate accuracy per level
    print("\n=== CALIBRATION SCORE ===\n")
    
    for level, results in levels.items():
        if results:
            accuracy = sum(results) / len(results) * 100
            count = len(results)
            print(f"{level}: {accuracy:.0f}% ({count} predictions)")
        else:
            print(f"{level}: No outcomes recorded")
    
    print("")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  track.py predict <statement> <HIGH|MEDIUM|LOW>")
        print("  track.py outcome <pred_id> <CORRECT|INCORRECT> <outcome>")
        print("  track.py score")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "predict":
        statement = sys.argv[2]
        confidence = sys.argv[3]
        add_prediction(statement, confidence)
    
    elif cmd == "outcome":
        pred_id = sys.argv[2]
        result = sys.argv[3]
        outcome = " ".join(sys.argv[4:]) if len(sys.argv) > 4 else ""
        record_outcome(pred_id, result, outcome)
    
    elif cmd == "score":
        calculate_score()
    
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
