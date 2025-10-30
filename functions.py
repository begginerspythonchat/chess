# вспомогательные функции
#
#
#
import os


def make_frame(text):
    """ Возвращает текст с рамкой. Пример:
        -> Привет
        <-
        +--------+
        | Привет |
        +--------+
    """
    new_lines = []
    max_len = max(map(lambda l: len(l), text.split("\n")))
    new_lines.append("+-" + ("-" * max_len) + "-+")
    for line in text.split("\n"):
        new_line = "| " + line.center(max_len) + " |"
        new_lines.append(new_line)
    new_lines.append("+-" + ("-" * max_len) + "-+")
    return "\n".join(new_lines)

def cls():
    """Функция очищает экран консоли"""
    os.system('cls' if os.name=='nt' else 'clear')

def get_cordinats(i_row, i_column, rows="87654321", columns="ABCDEFGH"):
    """ Принимает индексы шахматного поля, возвращает координаты:
        get_cordinats(0, 0)        # ("a", "1")
        get_cordinats(-1, 20)    # ValueError
    """
    try:
        row = rows[i_row]
        column = columns[i_column]
    except IndexError:
        raise ValueError("i_row or i_column is bad value")
    return (column.lower(), row.lower())

def get_indexes(row, column, rows="87654321", columns="ABCDEFGH"):
    """ Принимает координаты шахматного поля, возвращает индексы этих
        координат:
            getget_indexes("1", "a")    # (7, 0)
            getget_indexes("10", "z")    # ValueError
    """
    # переводим все строки в нижний регистр
    row, column = row.lower(), column.lower()
    rows, columns = rows.lower(), columns.lower()
    # находим индексы
    i_row = rows.find(row)
    i_column = columns.find(column)
    if (i_row == -1) or (i_column == -1):
        print(i_row, i_column)
        raise ValueError("row or column is bad value")
    return i_row, i_column

def check_cordinats(cordinats, rows="87654321", columns="ABCDEFGH"):
    """ Вызывает исключение если кординаты не верны"""
    # print(cordinats)
    cordinats = cordinats.lower()
    rows, columns = rows.lower(), columns.lower()
    if (len(cordinats) != 2) or (cordinats[0] not in columns) \
        or (cordinats[1] not in rows):
        raise ValueError(f"cordinats are not invalid : {cordinats}")    


if __name__ == "__main__":
    pass