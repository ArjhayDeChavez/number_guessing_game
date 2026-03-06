"""Persistent high‑score and scoring statistics for the guessing game."""

import json
from pathlib import Path
from typing import Dict, Any

SCORE_FILE = Path(".scores.json")


# structure stored in the JSON file
# {
#     "best_attempts": 5,
#     "games_played": 3,
#     "total_score": 12,
#     "best_score": 5
# }


def _default_stats() -> Dict[str, Any]:
    return {
        "best_attempts": None,
        "games_played": 0,
        "total_score": 0,
        "best_score": None,
    }


def load_score() -> Dict[str, Any]:
    """Load the scoreboard statistics.

    Always returns a dictionary with keys as shown in `_default_stats`.
    If the file is missing or corrupted, defaults are returned.
    """
    try:
        with SCORE_FILE.open() as f:
            data = json.load(f)
        stats = _default_stats()
        stats.update({k: data.get(k, stats[k]) for k in stats})
        return stats
    except Exception:
        return _default_stats()


def _compute_score(attempts: int, max_attempts: int, difficulty_multiplier: float = 1.0) -> int:
    """Compute score based on:
    - Base score: 10 points for guessing correctly
    - Bonus: 5 points per unused attempt
    - Multiplier: difficulty level multiplier (easy=1.0x, medium=1.5x, hard=2.0x)
    """
    base_score = 10
    points_per_unused = 5
    unused_attempts = max_attempts - attempts
    
    score = base_score + (unused_attempts * points_per_unused)
    final_score = int(score * difficulty_multiplier)
    return final_score


def save_score(attempts: int, max_attempts: int, difficulty_multiplier: float = 1.0) -> Dict[str, Any]:
    """Record the result of one round and update statistics.

    Args:
        attempts: Number of attempts used
        max_attempts: Maximum attempts allowed
        difficulty_multiplier: Difficulty level multiplier (easy=1.0, medium=1.5, hard=2.0)

    Returns the updated statistics dictionary.
    """
    stats = load_score()
    stats["games_played"] += 1
    score = _compute_score(attempts, max_attempts, difficulty_multiplier)
    stats["total_score"] += score

    if stats["best_score"] is None or score > stats["best_score"]:
        stats["best_score"] = score

    if stats["best_attempts"] is None or attempts < stats["best_attempts"]:
        stats["best_attempts"] = attempts

    try:
        with SCORE_FILE.open("w") as f:
            json.dump(stats, f)
    except Exception:
        pass
    return stats

