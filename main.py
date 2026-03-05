import random


def get_guess():
    while True:
        try:
            guess = int(input("Enter your guess (1-100): "))
            if 1 <= guess <= 100:
                return guess
            else:
                print("Please enter a number between 1 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def play_round():
    number_to_guess = random.randint(1, 100)
    chances = 7
    attempts = 0
    while chances > 0:
        print(f"You have {chances} chances left.")
        guess = get_guess()
        attempts += 1
        chances -= 1
        if guess < number_to_guess:
            print("Too low! Try again.")
        elif guess > number_to_guess:
            print("Too high! Try again.")
        else:
            print(f"Congratulations! You've guessed the number in {attempts} attempts.")
            break
    else:
        print(f"Game over! The number was {number_to_guess}.")


def main():
    print("Welcome to the Number Guessing Game!")
    while True:
        play_round()
        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again != 'yes':
            print("Thanks for playing! Goodbye!")
            break

if __name__ == "__main__":
    main()