import tkinter
from tkinter import ttk


class ChessField(ttk.Label):

    UNICODE_FIGURES = {
        None: "\u2003",
        "white pawn": "♙",
        "white knight": "♘",
        "white bishop": "♗",
        "white rook": "♖",
        "white queen": "♕",
        "white king": "♔",
        "black pawn": "♟",
        "black knight": "♞",
        "black bishop": "♝",
        "black rook": "♜",
        "black queen": "♛",
        "black king": "♚",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.figure = None

    @property
    def figure(self):
        return self._figure

    @figure.setter
    def figure(self, figure):
        self["text"] = self.UNICODE_FIGURES[figure]
        self._figure = figure


if __name__ == '__main__':
    cf = ChessField(font="default 50")
    cf.figure = "black pawn"
    cf.pack()