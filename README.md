# Number Guessing Game

A simple command-line number guessing game written in Python.

## Features

- Play interactive rounds guessing a random number.
- Configurable range and number of attempts via command-line arguments.
- Predefined difficulty levels (`easy`, `medium`, `hard`).
- Persistent scoring system (points per round)—you earn `(max_attempts - attempts + 1)` points per round—and statistics stored in `.scores.json`, including games played, best score, and average.
- Logic separated from I/O for easier testing.
- Unit tests with `pytest`.

## Getting Started

```bash
# clone or download the project, then
cd number_guessing_game
```
# it's a good idea to create a virtual environment first:
python -m venv .venv
source .venv/bin/activate   # or `.\.venv\Scripts\activate` on Windows

# install development requirements (pytest is optional)
pip install -r requirements.txt

# run the game
python main.py

# try a custom range or difficulty
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
│   ├── cli.py        # command-line interface
│   └── game.py       # core game logic
├── tests/            # unit tests
│   └── test_game.py
├── main.py           # entry point
└── README.md
```

Feel free to extend the game with scorekeeping, a GUI, or network play!
