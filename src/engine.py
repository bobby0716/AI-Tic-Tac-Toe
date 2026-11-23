"""
AI Tic-Tac-Toe - Minimax Decision Engine
Implements zero-sum game tree search with 3 difficulty modes.
"""

from typing import List, Optional, Tuple
import random


class Board:
    WIN_COMBINATIONS = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]

    def __init__(self, state: Optional[List[str]] = None):
        # 9 cells: indices 0 to 8
        self.grid = state.copy() if state else [" " for _ in range(9)]

    def available_moves(self) -> List[int]:
        """Returns all unoccupied cell indices."""
        return [i for i, cell in enumerate(self.grid) if cell == " "]

    def make_move(self, position: int, symbol: str) -> bool:
        """Places symbol at position if cell is empty."""
        if 0 <= position <= 8 and self.grid[position] == " ":
            self.grid[position] = symbol
            return True
        return False

    def undo_move(self, position: int) -> None:
        """Clears a cell (used during Minimax backtracking)."""
        self.grid[position] = " "

    def check_winner(self, symbol: str) -> bool:
        """Returns True if the given symbol has 3 in a row."""
        for a, b, c in self.WIN_COMBINATIONS:
            if self.grid[a] == self.grid[b] == self.grid[c] == symbol:
                return True
        return False

    def is_draw(self) -> bool:
        """Returns True if no empty spaces remain and neither player has won."""
        return " " not in self.grid

    def is_game_over(self, player1: str, player2: str) -> bool:
        """Checks if current state is terminal (win or draw)."""
        return self.check_winner(player1) or self.check_winner(player2) or self.is_draw()


class MinimaxAI:
    def __init__(self, ai_symbol: str, human_symbol: str):
        self.ai = ai_symbol
        self.human = human_symbol

    def _minimax(self, board: Board, depth: int, is_maximizing: bool) -> int:
        """
        Recursive Minimax tree search.
        Depth penalty (+10 - depth / -10 + depth) favors swift wins and delayed losses.
        """
        if board.check_winner(self.ai):
            return 10 - depth
        if board.check_winner(self.human):
            return depth - 10
        if board.is_draw():
            return 0

        if is_maximizing:
            best_score = -1000
            for move in board.available_moves():
                board.make_move(move, self.ai)
                score = self._minimax(board, depth + 1, False)
                board.undo_move(move)
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = 1000
            for move in board.available_moves():
                board.make_move(move, self.human)
                score = self._minimax(board, depth + 1, True)
                board.undo_move(move)
                best_score = min(best_score, score)
            return best_score

    def get_best_move(self, board: Board, difficulty: str = "Hard") -> int:
        """
        Determines the next move based on the selected difficulty:
          - Easy: 100% random move.
          - Medium: Opportunistic heuristic (takes win, blocks human win, else 50% random).
          - Hard: Pure optimal Minimax (unbeatable).
        """
        available = board.available_moves()
        if not available:
            raise ValueError("No available moves left on board.")

        diff = difficulty.capitalize()

        # 1. Easy Mode: Pure Random
        if diff == "Easy":
            return random.choice(available)

        # 2. Medium Mode: Smart Heuristic
        elif diff == "Medium":
            # Can AI win in this move?
            for move in available:
                board.make_move(move, self.ai)
                if board.check_winner(self.ai):
                    board.undo_move(move)
                    return move
                board.undo_move(move)

            # Must AI block human from winning?
            for move in available:
                board.make_move(move, self.human)
                if board.check_winner(self.human):
                    board.undo_move(move)
                    return move
                board.undo_move(move)

            # Otherwise, 50% chance of optimal move, 50% random
            if random.random() < 0.5:
                return random.choice(available)

        # 3. Hard Mode: Pure Minimax Search
        best_score = -1000
        best_moves = []

        for move in available:
            board.make_move(move, self.ai)
            score = self._minimax(board, depth=0, is_maximizing=False)
            board.undo_move(move)

            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        return random.choice(best_moves)