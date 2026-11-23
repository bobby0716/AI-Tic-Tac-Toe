"""
AI Tic-Tac-Toe - Unit Test Suite
Validates win conditions, draw mechanics, and Minimax optimality.
"""

import unittest
from src.engine import Board, MinimaxAI


class TestTicTacToe(unittest.TestCase):

    def test_win_conditions(self):
        """Tests horizontal, vertical, and diagonal win combinations."""
        # Row win
        b_row = Board(["X", "X", "X", " ", " ", " ", " ", " ", " "])
        self.assertTrue(b_row.check_winner("X"))

        # Column win
        b_col = Board(["O", " ", " ", "O", " ", " ", "O", " ", " "])
        self.assertTrue(b_col.check_winner("O"))

        # Diagonal win
        b_diag = Board(["X", " ", " ", " ", "X", " ", " ", " ", "X"])
        self.assertTrue(b_diag.check_winner("X"))

    def test_draw_condition(self):
        """Tests full board draw state."""
        b_draw = Board(["X", "O", "X", "X", "O", "O", "O", "X", "X"])
        self.assertTrue(b_draw.is_draw())
        self.assertFalse(b_draw.check_winner("X"))
        self.assertFalse(b_draw.check_winner("O"))

    def test_minimax_takes_winning_move(self):
        """Verifies AI prioritizes winning immediately over other moves."""
        # AI (O) can win at pos 2
        board = Board(["O", "O", " ", "X", "X", " ", " ", " ", " "])
        ai = MinimaxAI("O", "X")
        move = ai.get_best_move(board, difficulty="Hard")
        self.assertEqual(move, 2)

    def test_minimax_blocks_human_win(self):
        """Verifies AI prioritizes blocking an imminent human win."""
        # Human (X) is about to win at pos 2
        board = Board(["X", "X", " ", " ", "O", " ", " ", " ", " "])
        ai = MinimaxAI("O", "X")
        move = ai.get_best_move(board, difficulty="Hard")
        self.assertEqual(move, 2)

    def test_ai_vs_ai_always_draws(self):
        """
        Mathematical proof of Minimax optimality:
        When two optimal Minimax agents play each other, the outcome MUST be a Draw.
        """
        board = Board()
        ai_x = MinimaxAI("X", "O")
        ai_o = MinimaxAI("O", "X")

        turn = "X"
        while not board.is_game_over("X", "O"):
            if turn == "X":
                move = ai_x.get_best_move(board, difficulty="Hard")
                board.make_move(move, "X")
                turn = "O"
            else:
                move = ai_o.get_best_move(board, difficulty="Hard")
                board.make_move(move, "O")
                turn = "X"

        self.assertTrue(board.is_draw(), "Optimal AI vs AI must result in a Draw!")
        self.assertFalse(board.check_winner("X"))
        self.assertFalse(board.check_winner("O"))


if __name__ == "__main__":
    unittest.main(verbosity=2)