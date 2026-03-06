"""Command-line interface for the number guessing game."""

import argparse
from typing import Callable

from .game import NumberGuessingGame, Settings
from . import scoreboard


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Play a number guessing game.")
    parser.add_argument("--min", type=int, default=1, help="Lowest number in range")
    parser.add_argument("--max", type=int, default=100, help="Highest number in range")
    parser.add_argument(
        "--attempts", type=int, default=7, help="Maximum guesses per round"
    )
    parser.add_argument(
        "--difficulty",
        choices=["easy", "medium", "hard"],
        help="Shortcut for preconfigured settings",
    )
    parser.add_argument(
        "--show-score",
        action="store_true",
        help="Display the current high score and exit (alias for --scoreboard)",
    )
    parser.add_argument(
        "--scoreboard",
        action="store_true",
        help="Show full game statistics and exit",
    )

    return parser.parse_args()


def get_guess(prompt: str, input_func: Callable = input) -> int:
    """Prompt the user repeatedly until a valid integer in range is entered."""
    while True:
        try:
            value = int(input_func(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_difficulty_multiplier(max_attempts: int) -> float:
    """Determine difficulty multiplier based on max attempts.
    
    Easy (10 attempts): 1.0x
    Medium (7 attempts): 1.5x
    Hard (5 attempts): 2.0x
    Custom: interpolated based on attempts
    """
    if max_attempts >= 10:
        return 1.0
    elif max_attempts == 7:
        return 1.5
    elif max_attempts <= 5:
        return 2.0
    else:
        # Interpolate for custom values
        return 1.0 + (10 - max_attempts) * 0.1


def run_interactive_game(settings: Settings) -> None:
    game = NumberGuessingGame(settings)
    difficulty_multiplier = get_difficulty_multiplier(settings.max_attempts)
    while True:
        game.start_new_round()
        print(
            f"I'm thinking of a number between {settings.min_num} and {settings.max_num}."
        )

        while game.has_attempts_left():
            print(f"You have {settings.max_attempts - game.attempts} attempts left.")
            guess = get_guess("Enter your guess: ")
            result = game.check_guess(guess)
            if result == "low":
                print("Too low!")
            elif result == "high":
                print("Too high!")
            else:
                print(
                    f"Congratulations! You guessed the number in {game.attempts} guesses."
                )
                # update statistics and compute round score
                stats = scoreboard.save_score(game.attempts, settings.max_attempts, difficulty_multiplier)
                # Compute score for display using the same formula
                base_score = 10
                unused_attempts = settings.max_attempts - game.attempts
                round_score = int((base_score + (unused_attempts * 5)) * difficulty_multiplier)
                print(f"You scored {round_score} points this round.")
                print(f"  (Base: 10 + Bonus: {unused_attempts * 5} × {difficulty_multiplier:.1f}x)")
                if stats["best_score"] == round_score:
                    print("That's your best score so far!")
                if stats["best_attempts"] == game.attempts:
                    print("New best attempt count! 🏆")
                break
        else:
            print(
                f"Sorry, you've used all {settings.max_attempts} guesses. "
                f"The number was {game.number_to_guess}."
            )

        again = input("Play again? (y/N): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


def show_difficulty_menu() -> Settings:
    """Display an interactive menu to select difficulty."""
    print("\n=== Number Guessing Game ===\n")
    print("Choose a difficulty level:")
    print("  1. Easy   (1-50, 10 attempts)")
    print("  2. Medium (1-100, 7 attempts)")
    print("  3. Hard   (1-200, 5 attempts)")
    print("  4. Custom")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        if choice == "1":
            return Settings(min_num=1, max_num=50, max_attempts=10)
        elif choice == "2":
            return Settings(min_num=1, max_num=100, max_attempts=7)
        elif choice == "3":
            return Settings(min_num=1, max_num=200, max_attempts=5)
        elif choice == "4":
            try:
                min_num = int(input("Enter minimum number: "))
                max_num = int(input("Enter maximum number: "))
                max_attempts = int(input("Enter maximum attempts: "))
                if min_num >= max_num:
                    print("Error: minimum must be less than maximum.")
                    continue
                if max_attempts <= 0:
                    print("Error: attempts must be positive.")
                    continue
                return Settings(min_num=min_num, max_num=max_num, max_attempts=max_attempts)
            except ValueError:
                print("Invalid input. Please enter valid numbers.")
                continue
        else:
            print("Invalid choice. Please enter 1-4.")


def main() -> None:
    args = parse_args()

    # handle standalone operations first
    if args.show_score or args.scoreboard:
        stats = scoreboard.load_score()
        # basic high score
        if stats["best_attempts"] is None:
            print("No games played yet.")
            return
        if args.show_score and not args.scoreboard:
            # backward-compatible simple view
            print(f"Current high score: {stats['best_attempts']} attempts")
            return

        # full scoreboard
        avg_score = (
            stats["total_score"] / stats["games_played"]
            if stats["games_played"] > 0
            else 0
        )
        print("Scoreboard:")
        print(f"  Games played: {stats['games_played']}")
        print(f"  Best attempts: {stats['best_attempts']}")
        print(f"  Best round score: {stats['best_score']}")
        print(f"  Average score: {avg_score:.2f}")
        return

    if args.difficulty:
        if args.difficulty == "easy":
            settings = Settings(min_num=1, max_num=50, max_attempts=10)
        elif args.difficulty == "medium":
            settings = Settings(min_num=1, max_num=100, max_attempts=7)
        else:  # hard
            settings = Settings(min_num=1, max_num=200, max_attempts=5)
    elif args.min == 1 and args.max == 100 and args.attempts == 7:
        # No custom arguments provided, show interactive menu
        settings = show_difficulty_menu()
    else:
        settings = Settings(
            min_num=args.min, max_num=args.max, max_attempts=args.attempts
        )

    run_interactive_game(settings)
