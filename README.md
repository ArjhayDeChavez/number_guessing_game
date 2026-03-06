# Number Guessing Game

A simple command-line number guessing game written in Python.

## Features

- Play interactive rounds guessing a random number.
- Interactive difficulty menu when running without arguments.
- Configurable range and number of attempts via command-line arguments.
- Predefined difficulty levels (`easy`, `medium`, `hard`).
- Advanced scoring system with:
  - Base score: 10 points for guessing correctly
  - Bonus: 5 points per unused attempt
  - Difficulty multiplier: 1.0× (Easy), 1.5× (Medium), 2.0× (Hard)
- Persistent statistics stored in `.scores.json`: games played, best score, best attempts, and average score.
- Logic separated from I/O for easier testing.
- Unit tests with `pytest`.

## Getting Started

```bash
# clone or download the project, then
cd number_guessing_game

# it's a good idea to create a virtual environment first:
python -m venv .venv
source .venv/bin/activate   # or `.\.venv\Scripts\activate` on Windows

# install development requirements (pytest is optional)
pip install -r requirements.txt

# run the game (with interactive menu)
python main.py

# or run with specific difficulty/settings
python main.py --difficulty hard
python main.py --min 1 --max 500 --attempts 10

# view the current high score (simple)
python main.py --show-score
(or `python -m guessing_game --show-score`)

# show full scoreboard/stats
python main.py --scoreboard
(or `python -m guessing_game --scoreboard`)
```

## Running Tests

```bash
python -m pytest -q
```

## Project Structure

```
number_guessing_game/
├── guessing_game/
│   ├── __init__.py
│   ├── cli.py           # command-line interface
│   ├── game.py          # core game logic
│   └── scoreboard.py    # score tracking and statistics
├── tests/               # unit tests
│   ├── test_cli.py
│   ├── test_game.py
│   └── test_scoreboard.py
├── main.py              # entry point
├── requirements.txt
└── README.md
```

## Scoring System

Each successful round earns you points based on:
- **Base Score**: 10 points
- **Unused Attempts Bonus**: 5 points per unused attempt
- **Difficulty Multiplier**: 1.0× (Easy), 1.5× (Medium), 2.0× (Hard)

**Example**: Medium difficulty, guess in 3 attempts = (10 + 4×5) × 1.5 = **45 points**
