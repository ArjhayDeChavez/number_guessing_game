import json

from guessing_game import scoreboard


def test_scoreboard_initial(tmp_path):
    original = scoreboard.SCORE_FILE
    scoreboard.SCORE_FILE = tmp_path / "scores.json"
    try:
        stats = scoreboard.load_score()
        assert stats["games_played"] == 0
        assert stats["total_score"] == 0
        assert stats["best_attempts"] is None
        assert stats["best_score"] is None
    finally:
        scoreboard.SCORE_FILE = original


def test_scoreboard_updates(tmp_path):
    original = scoreboard.SCORE_FILE
    scoreboard.SCORE_FILE = tmp_path / "scores.json"
    try:
        # first round: 5 attempts out of 7 -> score = 3
        stats = scoreboard.save_score(5, max_attempts=7)
        assert stats["games_played"] == 1
        assert stats["total_score"] == 3
        assert stats["best_score"] == 3
        assert stats["best_attempts"] == 5

        # second round worse attempts but better score
        stats = scoreboard.save_score(6, max_attempts=10)
        # new score: 10-6+1 = 5
        assert stats["games_played"] == 2
        assert stats["total_score"] == 8
        assert stats["best_score"] == 5
        assert stats["best_attempts"] == 5  # still first round is best attempts

        # third round perfect
        stats = scoreboard.save_score(1, max_attempts=5)
        assert stats["games_played"] == 3
        assert stats["total_score"] == 8 + 5  # previous total + (5-1+1)
        assert stats["best_score"] == 5 or stats["best_score"] == 5
        assert stats["best_attempts"] == 1
    finally:
        scoreboard.SCORE_FILE = original

