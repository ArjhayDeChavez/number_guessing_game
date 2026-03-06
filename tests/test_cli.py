import sys
from io import StringIO

import pytest

from guessing_game import cli, scoreboard


def run_cli_with_args(args):
    """Run cli.main() with fake sys.argv and capture output."""
    old_argv = sys.argv.copy()
    old_stdout = sys.stdout
    sys.argv = [old_argv[0]] + args
    sys.stdout = StringIO()
    try:
        cli.main()
        return sys.stdout.getvalue()
    finally:
        sys.argv = old_argv
        sys.stdout = old_stdout


def test_show_scoreboard_no_games(tmp_path):
    original = scoreboard.SCORE_FILE
    scoreboard.SCORE_FILE = tmp_path / "scores.json"
    try:
        out = run_cli_with_args(["--scoreboard"])
        assert "No games played yet" in out
    finally:
        scoreboard.SCORE_FILE = original


def test_show_score_simple(tmp_path):
    original = scoreboard.SCORE_FILE
    scoreboard.SCORE_FILE = tmp_path / "scores.json"
    try:
        scoreboard.save_score(5, max_attempts=7)
        out = run_cli_with_args(["--show-score"])
        assert "Current high score: 5" in out
    finally:
        scoreboard.SCORE_FILE = original


def test_show_scoreboard_with_data(tmp_path):
    original = scoreboard.SCORE_FILE
    scoreboard.SCORE_FILE = tmp_path / "scores.json"
    try:
        scoreboard.save_score(5, max_attempts=7)
        scoreboard.save_score(6, max_attempts=10)
        out = run_cli_with_args(["--scoreboard"])
        assert "Games played: 2" in out
        assert "Best attempts: 5" in out
        assert "Best round score" in out
        assert "Average score" in out
    finally:
        scoreboard.SCORE_FILE = original

