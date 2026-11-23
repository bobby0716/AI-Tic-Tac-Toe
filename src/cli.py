"""
AI Tic-Tac-Toe - Console (CLI) Game Interface
Allows playing directly inside the terminal.
"""

from src.engine import Board, MinimaxAI


def print_board(board: Board):
    """Renders clean 3x3 ASCII grid."""
    g = board.grid
    print(f"\n {g[0]} | {g[1]} | {g[2]} ")
    print("---+---+---")
    print(f" {g[3]} | {g[4]} | {g[5]} ")
    print("---+---+---")
    print(f" {g[6]} | {g[7]} | {g[8]} \n")


def play_cli():
    print("=" * 45)
    print("      AI TIC-TAC-TOE (MINIMAX ENGINE)")
    print("=" * 45)

    # 1. Choose Symbol
    human = ""
    while human not in ["X", "O"]:
        human = input("Choose your symbol (X/O) [X moves first]: ").strip().upper()

    ai = "O" if human == "X" else "X"

    # 2. Choose Difficulty
    diff = ""
    while diff not in ["1", "2", "3"]:
        print("\nSelect Difficulty:")
        print("  [1] Easy (Random)")
        print("  [2] Medium (Heuristic)")
        print("  [3] Hard (Unbeatable Minimax)")
        diff = input("Choice (1-3): ").strip()

    diff_map = {"1": "Easy", "2": "Medium", "3": "Hard"}
    difficulty = diff_map[diff]

    board = Board()
    ai_agent = MinimaxAI(ai, human)
    current_player = "X"

    print(f"\nGame Started! You are '{human}', AI is '{ai}' ({difficulty} Mode)")
    print("Cell reference layout: 1 to 9 (top-left to bottom-right)")
    print_board(board)

    # 3. Game Loop
    while not board.is_game_over(human, ai):
        if current_player == human:
            while True:
                try:
                    move = int(input(f"Your move ({human}) [1-9]: ")) - 1
                    if board.make_move(move, human):
                        break
                    print("Cell already occupied or invalid. Try again.")
                except ValueError:
                    print("Please enter a valid number (1-9).")
        else:
            print(f"AI ({ai}) is computing best move...")
            move = ai_agent.get_best_move(board, difficulty=difficulty)
            board.make_move(move, ai)

        print_board(board)

        # Check Outcomes
        if board.check_winner(current_player):
            if current_player == human:
                print("🎉 Congratulations! You won!")
            else:
                print("🤖 Game Over! AI wins!")
            return

        if board.is_draw():
            print("🤝 It's a Draw!")
            return

        current_player = ai if current_player == human else human


if __name__ == "__main__":
    play_cli()