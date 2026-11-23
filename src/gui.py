"""
AI Tic-Tac-Toe - Modern Tkinter Desktop GUI
Features: Difficulty modes, scoreboard, turn indicators, and winning line highlights.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List
from src.engine import Board, MinimaxAI


class TicTacToeGUI:
    # Modern Color Palette
    BG_COLOR = "#1e1e2e"       # Deep slate/dark background
    CARD_COLOR = "#252538"     # Slightly lighter panel background
    TEXT_COLOR = "#cdd6f4"     # Soft white text
    X_COLOR = "#89b4fa"        # Soft modern blue
    O_COLOR = "#f38ba8"        # Soft coral/red
    WIN_COLOR = "#a6e3a1"      # Mint green for winning cells
    GRID_BTN_BG = "#313244"    # Cell button background

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("AI Tic-Tac-Toe (Minimax)")
        self.root.geometry("420x580")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG_COLOR)

        # Game State Variables
        self.human_symbol = "X"
        self.ai_symbol = "O"
        self.difficulty_var = tk.StringVar(value="Hard")
        self.board = Board()
        self.ai = MinimaxAI(self.ai_symbol, self.human_symbol)
        self.current_turn = "X"
        self.game_active = True

        # Score Tracking
        self.score_human = 0
        self.score_ai = 0
        self.score_draws = 0

        self._build_header()
        self._build_controls()
        self._build_board()
        self._build_scoreboard()

    def _build_header(self):
        """Top title and turn banner."""
        self.header_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.header_frame.pack(pady=(15, 5))

        self.title_label = tk.Label(
            self.header_frame,
            text="TIC-TAC-TOE AI",
            font=("Helvetica", 18, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR,
        )
        self.title_label.pack()

        self.status_label = tk.Label(
            self.header_frame,
            text="Your Turn (X)",
            font=("Helvetica", 11),
            fg=self.X_COLOR,
            bg=self.BG_COLOR,
        )
        self.status_label.pack(pady=(2, 0))

    def _build_controls(self):
        """Controls for difficulty and symbol selection."""
        ctrl_frame = tk.Frame(self.root, bg=self.CARD_COLOR, padx=10, pady=6)
        ctrl_frame.pack(fill="x", padx=30, pady=8)

        # Difficulty Selector
        tk.Label(ctrl_frame, text="Difficulty:", font=("Helvetica", 10), fg=self.TEXT_COLOR, bg=self.CARD_COLOR).grid(row=0, column=0, padx=5)
        diff_combo = ttk.Combobox(
            ctrl_frame,
            textvariable=self.difficulty_var,
            values=["Easy", "Medium", "Hard"],
            state="readonly",
            width=8,
        )
        diff_combo.grid(row=0, column=1, padx=5)

        # Symbol Toggle
        tk.Label(ctrl_frame, text="Play as:", font=("Helvetica", 10), fg=self.TEXT_COLOR, bg=self.CARD_COLOR).grid(row=0, column=2, padx=(15, 5))
        self.sym_btn = tk.Button(
            ctrl_frame,
            text="X (First)",
            font=("Helvetica", 9, "bold"),
            bg=self.GRID_BTN_BG,
            fg=self.X_COLOR,
            activebackground=self.GRID_BTN_BG,
            activeforeground=self.X_COLOR,
            relief="flat",
            command=self._toggle_symbol,
            padx=8,
        )
        self.sym_btn.grid(row=0, column=3, padx=5)

    def _build_board(self):
        """Builds the 3x3 interactive grid."""
        board_container = tk.Frame(self.root, bg=self.BG_COLOR)
        board_container.pack(pady=10)

        self.buttons: List[tk.Button] = []
        for i in range(9):
            btn = tk.Button(
                board_container,
                text=" ",
                font=("Helvetica", 22, "bold"),
                width=4,
                height=2,
                bg=self.GRID_BTN_BG,
                fg=self.TEXT_COLOR,
                activebackground="#45475a",
                relief="flat",
                bd=0,
                command=lambda pos=i: self._on_cell_click(pos),
            )
            btn.grid(row=i // 3, column=i % 3, padx=4, pady=4)
            self.buttons.append(btn)

    def _build_scoreboard(self):
        """Bottom score counter and reset button."""
        score_frame = tk.Frame(self.root, bg=self.CARD_COLOR, padx=15, pady=8)
        score_frame.pack(fill="x", padx=30, pady=(10, 5))

        self.score_label = tk.Label(
            score_frame,
            text="Player: 0  |  AI: 0  |  Draws: 0",
            font=("Helvetica", 10, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.CARD_COLOR,
        )
        self.score_label.pack(side="left")

        reset_btn = tk.Button(
            score_frame,
            text="New Game",
            font=("Helvetica", 9, "bold"),
            bg="#f38ba8",
            fg="#11111b",
            relief="flat",
            padx=10,
            command=self._reset_board,
        )
        reset_btn.pack(side="right")

    def _toggle_symbol(self):
        """Swaps player symbol between X and O."""
        if self.human_symbol == "X":
            self.human_symbol = "O"
            self.ai_symbol = "X"
            self.sym_btn.config(text="O (Second)", fg=self.O_COLOR)
        else:
            self.human_symbol = "X"
            self.ai_symbol = "O"
            self.sym_btn.config(text="X (First)", fg=self.X_COLOR)

        self.ai = MinimaxAI(self.ai_symbol, self.human_symbol)
        self._reset_board()

    def _on_cell_click(self, pos: int):
        """Handles human move on grid click."""
        if not self.game_active or self.board.grid[pos] != " " or self.current_turn != self.human_symbol:
            return

        self._execute_move(pos, self.human_symbol)

        if self._check_game_end(self.human_symbol):
            return

        # Hand over turn to AI with slight natural delay
        self.current_turn = self.ai_symbol
        self.status_label.config(text="AI is thinking...", fg=self.O_COLOR)
        self.root.after(350, self._ai_turn)

    def _ai_turn(self):
        """Queries Minimax engine and executes AI move."""
        if not self.game_active:
            return

        difficulty = self.difficulty_var.get()
        ai_move_pos = self.ai.get_best_move(self.board, difficulty=difficulty)
        self._execute_move(ai_move_pos, self.ai_symbol)

        if not self._check_game_end(self.ai_symbol):
            self.current_turn = self.human_symbol
            self.status_label.config(text=f"Your Turn ({self.human_symbol})", fg=self.X_COLOR if self.human_symbol == "X" else self.O_COLOR)

    def _execute_move(self, pos: int, symbol: str):
        """Updates board state and button graphic."""
        self.board.make_move(pos, symbol)
        color = self.X_COLOR if symbol == "X" else self.O_COLOR
        self.buttons[pos].config(text=symbol, fg=color, state="disabled")

    def _highlight_winning_cells(self, symbol: str):
        """Highlights the 3 winning squares in green."""
        for combo in Board.WIN_COMBINATIONS:
            if self.board.grid[combo[0]] == self.board.grid[combo[1]] == self.board.grid[combo[2]] == symbol:
                for idx in combo:
                    self.buttons[idx].config(bg=self.WIN_COLOR, fg="#11111b")
                break

    def _check_game_end(self, last_player: str) -> bool:
        """Evaluates win/draw and updates scoreboard."""
        if self.board.check_winner(last_player):
            self.game_active = False
            self._highlight_winning_cells(last_player)
            if last_player == self.human_symbol:
                self.score_human += 1
                self.status_label.config(text="🎉 You Won!", fg=self.WIN_COLOR)
            else:
                self.score_ai += 1
                self.status_label.config(text="🤖 AI Won!", fg=self.O_COLOR)
            self._update_score_display()
            return True

        if self.board.is_draw():
            self.game_active = False
            self.score_draws += 1
            self.status_label.config(text="🤝 It's a Draw!", fg=self.TEXT_COLOR)
            self._update_score_display()
            return True

        return False

    def _update_score_display(self):
        """Refreshes scoreboard text."""
        self.score_label.config(
            text=f"Player: {self.score_human}  |  AI: {self.score_ai}  |  Draws: {self.score_draws}"
        )

    def _reset_board(self):
        """Resets the grid for a new game without resetting score counters."""
        self.board = Board()
        self.game_active = True
        self.current_turn = "X"

        for btn in self.buttons:
            btn.config(text=" ", bg=self.GRID_BTN_BG, fg=self.TEXT_COLOR, state="normal")

        if self.human_symbol == "X":
            self.status_label.config(text="Your Turn (X)", fg=self.X_COLOR)
        else:
            self.status_label.config(text="AI is thinking...", fg=self.O_COLOR)
            self.root.after(350, self._ai_turn)


def launch_gui():
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()