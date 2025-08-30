import itertools

import tkinter
from tkinter import ttk

from chess_console import Game
from functions import get_cordinats


class GameFrame(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chess_board = ChessBoard()
        self.chess_board.pack()
        self.label_game_info = ttk.Label()
        self.label_game_info.pack()
        self.game = Game()
        self.update()
        self.chess_board.make_move = self.make_move

    def update(self):
        fields = itertools.chain.from_iterable(self.game.chess_board.matrix)
        figure_names = []
        for field in fields:
            figure = field.figure
            figure_name = (figure.color + " " + figure.name).lower() \
                if figure else figure
            figure_names.append(figure_name)
        self.chess_board.update(figure_names)

    def make_move(self, string):
        self.label_game_info["text"] = "your move: \"{}\"".format(string)
        try:
            self.game.commit_game_move(string)
        except ValueError as msg:
            self.label_game_info["text"] = msg
        self.game.update()
        self.update()
        if self.game.winer:
            self.label_game_info["text"] = self.game.winer + " won!"


class ChessBoard(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = []
        self.last_field = None
        # клетка шахматной доски последней затронутой фигуры
        # self.make_move    # функция для отправки хода в игру
        font = ("fixed", 30, "normal")
        font_for_coords = 15
        background_coords = "#999999"
        anchor = tkinter.CENTER
        sticky = "nesw"
        white_black_switcher = 0
        for ir, row in enumerate(" 87654321 "):
            for ic, column in enumerate(" abcdefgh "):
                if row == " ":
                    ttk.Label(self, text=column, font=font_for_coords,
                        anchor=anchor, background=background_coords).grid(
                            row=ir, column=ic, sticky=sticky)
                    continue
                elif column == " ":
                    ttk.Label(self, text=row, font=font_for_coords,
                        anchor=anchor, background=background_coords).grid(
                            row=ir, column=ic, sticky=sticky)
                    continue
                elif row == column == " ":
                    ttk.Label(self, text="\u2003",
                        anchor=anchor, background=background_coords).grid(
                            row=ir, column=ic, sticky=sticky)
                    continue
                color = ["white", "black"][white_black_switcher]
                if color == "black":
                    background = "grey"
                else:
                    background = "white"
                field = ChessField(root, font=font, background=background,
                    anchor=anchor)
                field.bind("<ButtonRelease>", self.touch_figure)
                field.grid(in_=self, row=ir, column=ic, sticky=sticky)
                self.fields.append(field)
                white_black_switcher ^= 1
            white_black_switcher ^= 1


    def touch_figure(self, event):
        field = event.widget
        # предыдущая клетка не выбранна, а текущая пуста
        if None == self.last_field == field.figure:
            return
        if field.was_touched:
            field["foreground"] = "black"
            field.was_touched = False
            self.last_field = None
            return
        # Разные цвета подсветки, для лучшей видимости
        # Замечание. Опция "background" у "обычных" виджетов (доступных
        # через модуль tkinter) является строкой (str)
        # у виджетов из ttk - <border object>, название цвета
        # в поле string этого объекта
        if field["background"].string == "grey":
            field["foreground"] = "green3"
        elif field["background"].string == "white":
            field["foreground"] = "green"
        field.was_touched = True
        # предыдущая клетка была выбранна и не равна текущей
        if self.last_field and self.last_field != field:
            # находим строковые координаты по индексам
            # индексы - 1 (так как обозначения координат шахматной доски
            # упакованны в одном виджете с клетками шахматной доски 
            # при помощи (.grid()))
            grid_info_1 = self.last_field.grid_info()
            coords_1 = "".join((get_cordinats(
                    grid_info_1["row"] - 1,
                    grid_info_1["column"] - 1)))
            grid_info_2 = field.grid_info()
            coords_2 = "".join((get_cordinats(
                    grid_info_2["row"] - 1,
                    grid_info_2["column"] - 1)))
            self.last_field["foreground"] = field["foreground"] = "black"
            self.last_field.was_touched = field.was_touched = False
            self.last_field = None
            try:
                self.make_move(coords_1 + " " + coords_2)
            except AttributeError:
                raise
        else:
            self.last_field = field

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
    game_frame = GameFrame(root)
    game_frame.pack()