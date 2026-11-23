### AI Tic-Tac-Toe (Unbeatable Minimax Engine)

An intelligent Tic-Tac-Toe game featuring an unbeatable game engine powered by the Minimax algorithm, interactive difficulty selection, a live scoreboard, and both Desktop GUI and Terminal CLI modes.

## How the Minimax Algorithm Works

Tic-Tac-Toe is a zero-sum, perfect-information game. The Minimax algorithm performs a recursive depth-first search across all possible future states to evaluate the optimal strategic move:

                    [Current State]
                             │
       ┌─────────────────────┼─────────────────────┐
     Move 1                Move 2                Move 3
       │                     │                     │
   (Human)               (Human)               (Human)

   Minimizes Score Minimizes Score Minimizes Score -10 0 +10

   
- **Evaluation Function:**
  - AI Wins: $+10 - \text{depth}$ *(favors swift wins)*
  - Human Wins: $\text{depth} - 10$ *(delays inevitable defeat)*
  - Draw: $0$
- **Mathematical Optimality:** In **Hard** mode, the AI plays with mathematical perfection. It is impossible to defeat—the best possible outcome for any human player is a **Draw**.

---

##  Features

- **🎮 Dual Interfaces:** 
  - **Modern Desktop GUI (Tkinter):** Sleek dark theme, symbol toggling ($X$ or $O$), live scoreboard, and winning line highlights.
  - **Console CLI Mode:** Fast terminal gameplay using `python main.py --cli`.
- ** 3 Difficulty Levels:**
  - 🟢 **Easy:** Casual / Random moves.
  - 🟡 **Medium:** Smart heuristic (capitalizes on winning moves and blocks immediate threats).
  - 🔴 **Hard (Unbeatable):** 100% pure Minimax algorithm.
- ** 100% Zero-Dependency:** Written entirely using standard library Python (no third-party pip dependencies required).
- ** Unit Test Suite:** Includes automated mathematical proof that AI vs AI matches always terminate in a Draw.

---

##  Project Structure

```text
AI-Tic-Tac-Toe/
├── src/
│   ├── __init__.py
│   ├── engine.py          # Minimax decision tree & Board logic
│   ├── gui.py             # Modern Tkinter desktop application
│   └── cli.py             # Interactive console game loop
├── tests/
│   ├── __init__.py
│   └── test_game.py       # Unit test suite & AI vs AI validation
├── main.py                # Multi-mode launcher entrypoint
├── .gitignore             # Enforces clean version control
└── README.md              # Project documentation

### Quickstart Guide

1. Run the Desktop GUI

python main.py

2. Run in Terminal CLI Mode

python main.py --cli

3. Run Automated Tests

python -m unittest tests.test_game -v