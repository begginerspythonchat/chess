import tkinter
from tkinter import ttk


class ChessField(ttk.Label):

    UNICODE_FIGURES = {
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
        None: "\u2003",
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
    root = tkinter.Tk()
    row = column = switcher = 0
    for figure in ChessField.UNICODE_FIGURES:
        if column == 6:
            row += 1
            switcher ^= 1
            column = 0
        if not switcher:
            background = "grey"
        else:
            background = "white"
        cf = ChessField(root, font="Arial 50", background=background)
        cf.figure = figure
        cf.grid(in_=root, row=row, column=column)
        column += 1
        switcher ^= 1