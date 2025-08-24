import tkinter
from tkinter import ttk


class ChessBoard(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = []
        font = ("fixed", 30, "normal")
        white_black_switcher = 0
        for ir, row in enumerate(" 87654321 "):
            for ic, column in enumerate(" abcdefgh "):
                if row == " ":
                    ttk.Label(self, text=column, font=font).grid(
                        row=ir, column=ic, sticky="nesw")
                    continue
                elif column == " ":
                    ttk.Label(self, text=row, font=font).grid(
                        row=ir, column=ic, sticky="nesw")
                    continue
                elif row == column == " ":
                    ttk.Label(self, text="\u2003").grid(
                        row=ir, column=ic, sticky="nesw")
                    continue
                color = ["white", "black"][white_black_switcher]
                if color == "black":
                    background = "grey"
                else:
                    background = "white"
                field = ChessField(root, font=font, background=background)
                field.bind("<ButtonRelease>", self.touch_figure)
                field.grid(in_=self, row=ir, column=ic, sticky="nesw")
                self.fields.append(field)
                white_black_switcher ^= 1
            white_black_switcher ^= 1

    def touch_figure(self, event):
        if event.widget.was_touched:
            event.widget["foreground"] = "black"
            event.widget.was_touched = False
            return
        event.widget["foreground"] = "green"
        event.widget.was_touched = True

    def update(self, figures):
        for field, figure in zip(self.fields, figures):
            field.figure = figure


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
        self.was_touched = False

    @property
    def figure(self):
        return self._figure

    @figure.setter
    def figure(self, figure):
        self["text"] = self.UNICODE_FIGURES[figure]
        self._figure = figure


if __name__ == "__main__":
    root = tkinter.Tk()
    chess_board = ChessBoard(root)
    chess_board.pack(in_=root, fill="both", expand=True)
    chess_board.update(ChessField.UNICODE_FIGURES)