import pytest

from guessing_game.game import NumberGuessingGame, Settings


def test_check_guess_too_low():
    settings = Settings(min_num=1, max_num=10, max_attempts=3)
    game = NumberGuessingGame(settings)
    game.number_to_guess = 5  # bypass randomness

    assert game.check_guess(3) == "low"
    assert game.attempts == 1


def test_check_guess_too_high():
    settings = Settings(min_num=1, max_num=10, max_attempts=3)
    game = NumberGuessingGame(settings)
    game.number_to_guess = 5

    assert game.check_guess(7) == "high"
    assert game.attempts == 1


def test_check_guess_correct():
    settings = Settings(min_num=1, max_num=10, max_attempts=3)
    game = NumberGuessingGame(settings)
    game.number_to_guess = 5

    assert game.check_guess(5) == "correct"
    assert game.attempts == 1


def test_has_attempts_left():
    settings = Settings(min_num=1, max_num=10, max_attempts=2)
    game = NumberGuessingGame(settings)
    game.number_to_guess = 1

    # before any guesses
    assert game.has_attempts_left()
    game.check_guess(1)
    assert game.has_attempts_left()  # one attempt used
    game.check_guess(1)
    assert not game.has_attempts_left()


def test_start_new_round_resets_state(monkeypatch):
    settings = Settings(min_num=1, max_num=100, max_attempts=5)
    game = NumberGuessingGame(settings)

    # patch random.randint to produce a predictable value
    monkeypatch.setattr("random.randint", lambda a, b: 42)
    game.start_new_round()
    assert game.number_to_guess == 42
    assert game.attempts == 0

    # using guess should increment attempts
    game.check_guess(41)
    assert game.attempts == 1
