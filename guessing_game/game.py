import random
from dataclasses import dataclass
from typing import Optional


@dataclass
class Settings:
    min_num: int = 1
    max_num: int = 100
    max_attempts: int = 7


class NumberGuessingGame:
    """Core logic for the number guessing game.

    The game generates a random number within a range and allows the
    caller to supply guesses.  This class is intentionally separated from
    any input/output to make it easier to test and reuse.
    """

    def __init__(self, settings: Settings = Settings()):
        self.settings = settings
        self.number_to_guess: Optional[int] = None
        self.attempts: int = 0

    def start_new_round(self) -> None:
        """Begin a new round by picking a random number and resetting state."""
        self.number_to_guess = random.randint(self.settings.min_num, self.settings.max_num)
        self.attempts = 0

    def check_guess(self, guess: int) -> str:
        """Check a single guess and return one of 'low', 'high', or 'correct'.

        The method also increments the attempt counter.
        """
        if self.number_to_guess is None:
            raise RuntimeError("Round has not been started")

        self.attempts += 1
        if guess < self.number_to_guess:
            return "low"
        elif guess > self.number_to_guess:
            return "high"
        else:
            return "correct"

    def has_attempts_left(self) -> bool:
        return self.attempts < self.settings.max_attempts
