# Игра "шахматы"
# Базовая версия, консольная
# Нужные сущности:
#
#	Меню
#		- запуск игры
#		- выход из игры
#		- помощь
#
#	Игра
#		- отрисовка игрового поля
#		- информация о том кто ходит
# 		- передвигает фигуры
#		-
#
#	Шахматная доска
# 		- клетки
# 		-
# 		-
# 		-
# 
# 	Клетка
# 		- координаты
# 		- фигура, если есть
# 		- 
# 
# 	Фигура
# 		- клетка
# 		- название
# 		- координаты
# 		-
#
import itertools

import functions


class ConsoleApp:

	def __init__(self):
		self.menu_commands = {
			"start": self.start,
			"exit": self.exit,
			"help": self.help,
		}

	def __call__(self):
		self.menu()

	def get_menu_command(self):
		menu_command = input("menu command: ")
		try:
			func = self.menu_commands[menu_command]
			func()
		except KeyError:
			self.menu()

	def start(self):
		functions.cls()
		print("start")
		game = ConsoleGame()
		game()
		self.menu()
		pass

	def exit(self):
		print("exit")
		pass

	def help(self):
		functions.cls()
		help_message = "Справка по меню\n"
		help_message += "help - справка по меню\n"
		help_message += "start - начианает новую игру\n"
		help_message += "exit - вызод из игры\n"
		print(help_message)
		input("press Enter")
		self.menu()
		pass

	def menu(self):
		functions.cls()
		text = "CHESS GAME\n\nstart\nhelp\nexit\n"
		print(functions.make_frame(text))
		self.get_menu_command()
		pass


class ConsoleGame:

	def __init__(self):
		self.game = Game()
		self.last_message = ""
		self.game_commands = {
			"exit": self.exit,
			"help": self.help,
		}

	def __call__(self):
		# self.show_game()
		while True:
			# если в игре есть победитель, то напиши в сообщении
			self.game.update()
			if self.game.winer:
				self.last_message = f"{self.game.winer} player won"
			# показываем состояние игры
			self.show_game()
			# принимаем команду
			command = input("game command: ")
			# пытаемся выполнить команду 
			try:
				# если команду удалось найти, то выполняем её
				func = self.game_commands[command]
				func()
				# выходим если была комада для выхода
				if command == "exit":
					break
				# проходим цикл заново
				continue
			# если команда не нашлась, то проходим дальше
			except KeyError:
				pass
			# если есть победитель, то сходить нельзя
			if self.game.winer:
				continue
			# пытаемся сходить ход
			try:
				self.game.commit_game_move(command)
			except Exception as msg:
				self.last_message = msg
			else:
				self.last_message = ""

	def show_game(self):
		functions.cls()
		print("print 'help' if you need help")
		print(f"last_message: {self.last_message}")
		print(self.game)
	
	def exit(self):
		print("exit")

	def help(self):
		functions.cls()
		help_msg = "game commands:\n"
		help_msg += "help - справка по командам\n"
		help_msg += "exit - выход из игры\n"
		help_msg += "'строка' - будет восприниматься как ход\n"
		help_msg += "		например: e2 e4\n"
		print(help_msg)
		input()
		

class Game:

	def __init__(self):
		""" chess_board		- объект шахматной доски
		"""
		self.chess_board = ChessBoard()
		self.players = ["white", "black"]
		self.player_turn = self.players[0]
		self.create_and_set_figures()
		# self.create_test_figures()
		self.winer = None
		self.update()

	def __str__(self):
		res_string = f"player turn: {self.player_turn}\n"
		res_string += str(self.chess_board) + "\n"
		return res_string

	def create_and_set_figures(self):
		""" Создаём и раставляем фигуры разного цвета на шахматной
			доске (chess_board).
		"""
		self.kings = {}
		# создаём чёрные и белые пешки
		for color, row in (("black", "7"), ("white", "2")):
			for column in self.chess_board.columns:
				pawn = Pawn(color=color, chess_board=self.chess_board)
				field = self.chess_board.get_field(column + row)
				pawn.set_at_field(field)
		# создаём ряд фигур для белых и для чёрных
		for color, row in (("black", "8"), ("white", "1")):
			for FigureClass, column in zip(
				(Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook),
				self.chess_board.columns):
				figure = FigureClass(color=color, 
					chess_board=self.chess_board)
				field = self.chess_board.get_field(column + row)
				figure.set_at_field(field)
				# если это король, то добавь его к королям
				if type(figure) == King:
					self.kings[figure.color] = figure
		self.chess_board.update()

	def create_test_figures(self):
		figures_for_test_for_pawn = (
			{"color": "white", "figure": Pawn, "cordinats": "e7",},
			{"color": "black", "figure": King, "cordinats": "e4",},
			# чёрная пешка перед белой, белая на 2 горизонтали
			{"color": "black", "figure": Pawn, "cordinats": "g3",},
			{"color": "white", "figure": Pawn, "cordinats": "g2",},
			# для взятия на проходе
			{"color": "black", "figure": Pawn, "cordinats": "b4",},
			{"color": "white", "figure": Pawn, "cordinats": "a2",},
			# {"color":, "figure":, "cordinats":,},
			# {"color":, "figure":, "cordinats":,},
		)
		figures_for_test_for_castling = (
			# для рокировки белых
			{"color": "white", "figure": Rook, "cordinats": "a1",},
			{"color": "white", "figure": King, "cordinats": "e1",},
			{"color": "white", "figure": Rook, "cordinats": "h1",},
			# для рокировки чёрных
			{"color": "black", "figure": Rook, "cordinats": "a8",},
			{"color": "black", "figure": King, "cordinats": "e8",},
			{"color": "black", "figure": Rook, "cordinats": "h8",},
		)
		figures_for_test_for_checkmate = (
			# для белых
			{"color": "white", "figure": Rook, "cordinats": "c3",},
			{"color": "white", "figure": King, "cordinats": "e1",},
			# для чёрных
			{"color": "black", "figure": Rook, "cordinats": "a1",},
			{"color": "black", "figure": King, "cordinats": "e8",},
			{"color": "black", "figure": Rook, "cordinats": "b2",},
		)
		self.kings = {}
		for data in figures_for_test_for_checkmate:
			figure = data["figure"](color=data["color"], 
				chess_board=self.chess_board)
			figure.set_at_field(
				self.chess_board.get_field(data["cordinats"]))
				# если это король, то добавь его к королям
			if type(figure) == King:
				self.kings[figure.color] = figure
		# 
		self.chess_board.save_current_stage()
		self.chess_board.update()

	def commit_game_move(self, string):
		""" Совершаем один игровой ход.	Меняется очередь хода для игроков.
			Проверяет налчие шаха, мата.
		"""
		# сохраняем состояние шахматного поля на данный момент
		self.chess_board.save_current_stage()
		# словарь для команд для рокировки
		dict_for_castling = {
			("o-o", "о-о", "0-0") : "short",
			("o-o-o", "о-о-о", "0-0-0") : "long",
		}
		# если строка без пробелов и эта строка
		# есть среди вариантов для обозначения рокиорвки
		if len(string.split()) == 1 \
			and string in \
			itertools.chain(*[strings for strings in dict_for_castling]):
			# находим сторону для рокировки и вызываем рокировку
			for strings, castling in dict_for_castling.items():
				if string.lower() in strings:
					self.commit_castling(self.player_turn, castling)
		# если между двумя подстроками есть один пробел, то
		# считаем это за команду для хода
		elif len(string.split()) == 2:
			cordinats_1, cordinats_2 = string.split()
			self.commit_move(self.player_turn, cordinats_1, cordinats_2)
		else:
			raise ValueError(f"{string} is unknown game move")
		# обновляем шахматную доску
		self.chess_board.update()
		# если после хода шах остался
		if self.is_check(self.chess_board, self.player_turn):
			# шахматную доску оставляем такой какой была до хода
			self.chess_board.backup()
			raise ValueError(
				f"{self.player_turn} king is attaked")
		# если ход совершён, и исключений не возникло, то передаём
		# ход другому игроку
		indx = self.players.index(self.player_turn)
		self.player_turn = self.players[indx ^ 1]

	def commit_move(self, color, cordinats_1, cordinats_2):
		""" Соврешаем ход фигурой с поля с кординатами cordinats_1
			на поле с кординатами cordinats_2
		"""
		functions.check_cordinats(cordinats_1)
		functions.check_cordinats(cordinats_2)
		field = self.chess_board.get_field(cordinats_1)
		if not field.figure:
			raise ValueError(f"this field has not figure: {field.cordinats}")
		figure = field.figure
		if figure.color != color:
			raise ValueError("you chose not your figure")
		# ходим выбраной фигурой
		figure.go_to(cordinats_2)

	def commit_castling(self, color, castling):
		""" Функция совершает рокировку если это возможно
			для игрока с цветом color. Длинная или коротка рокировка
			значение castling "long", "short"
		"""
		# print("commit_castling")
		# узнаём горизонталь в зависимости от цвета
		row = "1" if color == "white" else "8"
		# узнаём вертикаль для ладьи в зависимости от стороны рокировки
		if castling == "short":
			rook_column = "h"
		elif castling == "long":
			rook_column = "a"
		else:
			raise ValueError(
				"bad argument - castling. Can be \"short\" or \"long\" ")
		# 
		# выполняем действия связанные с королём
		# 
		# поле на котором должен стоять король
		king_field = self.chess_board.get_field("e" + row)
		# проверяем есть ли на королевском поле фигура
		if not king_field.figure:
			raise ValueError(
				f"field {king_field.cordinats} do not have figure")
		# узнаём что за фигура стоит на поле, если это не король,
		# то вызываем исключение
		king = king_field.figure
		if type(king) != King:
			raise TypeError(
				f"figure on {king_field.cordinats} is not king")
		# если король совершал ход, то вызываем исключение
		if king.was_moved:
			raise ValueError("king was moved.")
		# print(set((color, )), king_field.available_for_colors)
		# если король под шахом
		if not set((color, )) >= king_field.available_for_colors:
			raise ValueError("king was attacked")
		# 
		# выполняем действия связанные с ладьёй
		# 
		# находим поле для ладьи
		rook_field = self.chess_board.get_field(rook_column + row)
		# поле для ладьи должна быть фигура
		if not rook_field.figure:
			raise ValueError(
				f"field {rook_field.cordinats} do not have figure")
		# проверяем, ладья ли это
		rook = rook_field.figure
		if type(rook) != Rook:
			raise TypeError(
				f"figure on {king_field.cordinats} is not king")
		# если ладья двигалась, то рокировка не возможна
		if rook.was_moved:
			raise ValueError("rook was moved.")
		# 
		# проверяем наличие фигур меджу королём и ладьёй
		# 
		# в зависимости от стороны рокировки проверяем разные поля
		if castling == "long":
			columns = ("b", "c", "d")
		if castling == "short":
			columns = ("f", "g")
		# если между королём и ладьёй есть фигура, 
		# значит рокировка невозможна
		for column in columns:
			field = self.chess_board.get_field(column + row)
			if field.figure:
				raise ValueError(f"field {field.cordinats} has figure")
		# 
		# проверяем битые поля, между королём и ладьёй
		# 
		# в зависимости от стороны рокировки проверяем разные поля
		# проверяем только те поля, которые пересекает король.
		# те. поля которые пересекает ладья, могут быть под угрозой
		if castling == "long":
			columns = ("c", "d")
		if castling == "short":
			columns = ("f", "g")
		# проверяем поля, если они под угрозой нападения
		# то рокировку совершать нельзя
		for cloumn in columns:
			field = self.chess_board.get_field(column + row)
			if not set((color, )) >= king_field.available_for_colors:
				raise ValueError(f"field: {field.cordinats} was attacked")
		# 
		# если рокировку можно совершить, то совершаем её
		# 
		if castling == "long":
			new_field_for_king = self.chess_board.get_field("c" + row)
			new_field_for_rook = self.chess_board.get_field("d" + row)
		elif castling == "short":
			new_field_for_king = self.chess_board.get_field("g" + row)
			new_field_for_rook = self.chess_board.get_field("f" + row)
		# устанавливаем фигуры на новые поля
		king.set_at_field(new_field_for_king)
		rook.set_at_field(new_field_for_rook)
		# print("OK! Castling is possible!")

	def is_check(self, chess_board, color):
		""" Проверяет наличие шаха для игрока цвета color
			chess_board - объект шазматной доски
			color - строка цвета игрока ("white"/"black")
		"""
		for field in itertools.chain.from_iterable(chess_board.matrix):
			if field.figure:	# если на поле есть фигура
				figure = field.figure
				# если фигура это король нужного цвета
				if type(figure) == King and figure.color == color:
					# проверяем, может ли фигура другого цвета 
					# атаковать это поле
					if set((color,)) >= field.available_for_colors:
						return False
					else:
						return True
		# print(chess_board)
		# на случай если король не был найден
		raise ValueError(f"chess board do not have {color} king")

	def is_checkmate(self, chess_board, color):
		""" Проверяет наличие мата для игрока цвета color
			chess_board - объект шахматной доски (ChessBoard)
			color - строка цвета игрока ("white"/"black")
		"""
		# если шаха нет, то мата тоже
		if not self.is_check(chess_board, color):
			return False
		# создаём копию шахматной доски чтобы с ней производить
		# ходы фигурами
		new_chess_board = chess_board.copy()
		# print(new_chess_board)
		# для каждого поля из шахматной доски, находим фигуры
		# цвета игрока, и пытаемся сходить этой фигурой,
		# если после хода этой фигуры шах исчез, значит мата нет
		for field in itertools.chain.from_iterable(chess_board.matrix):
			# пропускаем если поле не имеет фигуры или фигура дргуого
			# цвета
			if not field.figure:
				continue
			if not field.figure.color == color:
				continue
			figure = field.figure
			# находим возможные поля на которые может сходить фигура
			available_fields = figure.get_available_fields()
			filtered_fields = \
				figure.filter_available_fields(available_fields)
			# на каждое поле совершаем ход этой фигурой
			for field_for_move in filtered_fields:
				# находим аналогичные :
				# поле, фигуру, поле для хода из копии шахматной доски
				field_ = new_chess_board.get_field(field.cordinats)
				figure_ = field_.figure
				field_for_move_ = new_chess_board.get_field(
									field_for_move.cordinats)
				# сохраняем состояние копии шахматного поля
				new_chess_board.save_current_stage()
				# на случай если фигурой будет король, и им нельзя
				# сходить на битое поле, выкинет исключение
				try:
					# пытаемся сходить фигурой
					figure_.go_to(field_for_move.cordinats)
				except:
					# если сходить не получилось, пропускаем
					continue
				# обновляем копию шахматной доски,
				# для того что бы обновить значения доступности каждого
				# поля для фигур разного цвета
				new_chess_board.update()
				# если после хода шаз исчез, значит мата нет
				if not self.is_check(new_chess_board, color):
					return False
				# возвращаем копию шахматной доски в прежнее состояние
				new_chess_board.backup()
		# если ни один ход фигур не избавил от шаха, то это мат
		return True

	def update(self):
		""" Обновляем состояние игры
			проверяем наличие победителя
		"""
		# если есть мат, то выиграл противоположный игрок
		if self.is_checkmate(self.chess_board, self.player_turn):
			indx = self.players.index(self.player_turn)
			self.winer = self.players[indx ^ 1]

class ChessBoard:

	def __init__(self, rows="87654321", columns="ABCDEFGH"):
		"""Создаёт объект шахматной доски,
			содержит информацию о клетках
		"""
		self.rows = rows
		self.columns = columns
		self.create_matrix()

	def __str__(self):
		""" Возвращает строковое представления шахматной доски
			где "." - строковое представление пустого поля (Field)
			+-------------------------+
			|     A B C D E F G H     |
			|   +-----------------+   |
			| 8 | . . . . . . . . | 8 |
			| 7 | . . . . . . . . | 7 |
			| 6 | . . . . . . . . | 6 |
			| 5 | . . . . . . . . | 5 |
			| 4 | . . . . . . . . | 4 |
			| 3 | . . . . . . . . | 3 |
			| 2 | . . . . . . . . | 2 |
			| 1 | . . . . . . . . | 1 |
			|   +-----------------+   |
			|     A B C D E F G H     |
			+-------------------------+
		"""
		# создаём строки из полей шахматной доски, + рамка
		strings = []
		for row in self.matrix:
			string = " ".join(str(field) for field in row)
			strings.append(string)
		board_string = functions.make_frame("\n".join(strings))
		# добавляем координаты шахмат, + рамка
		strings = []
		# добавляем символы столбцов сверху
		strings.append(" " * 4 + " ".join(self.columns) + " " * 4)
		for line, row in zip(
						board_string.split("\n"),
						" " + self.rows + " "	# пробелы, нужны сохранеия
						):						# рамки
			line = row + " " + line + " " + row
			strings.append(line)
		# добавляем символы столбцов снизу
		strings.append(" " * 4 + " ".join(self.columns) + " " * 4)
		# возвращаем текст с рамкой
		return functions.make_frame("\n".join(strings))

	def create_matrix(self):
		""" Создаёт двумерный список (matrix)
			при self.rows = "21", self.columns = "AB" создаст
			matrix = [
				[Field(0, 0), Field(0, 1)],
				[Field(1, 0), Field(1, 1)]
			]
		"""
		self.matrix = []
		for i_row, row in enumerate(self.rows):
			self.matrix.append([])
			for i_column, column in enumerate(self.columns):
				self.matrix[i_row].append(
					Field(i_row, i_column, cordinats=column+row)
					)

	def save_current_stage(self):
		""" Сохраняет состояние шахматной доски"""
		last_matrix = []
		for i_row, row in enumerate(self.matrix):
			new_row = []
			for field in row:
				new_field = field.copy()
				if field.figure:
					new_figure = field.figure.copy(chess_board=self)
					new_figure.set_at_field(new_field)
				new_row.append(new_field)
			last_matrix.append(new_row)
		self.last_matrix = last_matrix

	def backup(self):
		""" Функция возвращающая последнее состояние шахматного поля"""
		self.matrix = self.last_matrix

	def update(self):
		""" Для каждого поля стираем цвета фигур для которых оно доступно.
			(field.clear_set_of_colors). И заново для каждой фигуры 
			высчитываем поля на которое она	может сходить.
			Нужно для того что бы поля забывали неактуальные значения
			цветов фигур которые могут на них сходить.
		"""
		# для каждого поля стираем старые значения цветов фигур
		# которые могут на него сходить
		for row in self.matrix:
			for field in row:
				field.clear_set_of_colors()
		# для каждой фигуры поля на коорое оно может сходить помечаем
		# что на это поле может сходить данная фигура
		for row in self.matrix:
			for field in row:
				if field.figure:
					field.figure.mark_available_fields()

	def copy(self):
		""" Создаём копию шахматной доски"""
		new_chess_board = ChessBoard()
		# для каждого поля, создаём копию, помещаем эту копию в 
		# матрицу шахматной доски
		for field in itertools.chain.from_iterable(self.matrix):
			new_field = field.copy()
			new_chess_board.matrix\
				[field.i_row][field.i_column] = new_field
			# если старое поле имеет фигуру, то сделай её копию
			# и эту копию установи на новое поле
			if field.figure:
				figure = field.figure
				new_figure = figure.copy(new_chess_board)
				new_figure.set_at_field(new_field)
		return new_chess_board

	def get_field(self, cordinats):
		""" Примает строку кординат шахматного поля, возвращает
			поле (Field) с этими кординатами:
				cb = ChessBoard()
				cd.get_field("A8")	# Field(0, 0)
		"""
		functions.check_cordinats(cordinats)
		i_row, i_column = functions.get_indexes(cordinats[1], cordinats[0])
		return self.matrix[i_row][i_column]

	def get_cordinats(self, field):
		""" Возвращает строку с кординатами поля (field)"""
		i_row, i_column = field.i_row, field.i_column
		return "".join(functions.get_cordinats(i_row, i_column))


class Field:

	def __init__(self, i_row, i_column, cordinats):
		""" Поле, имеет индексы горизонтали и вертикали 
			(i_row, i_column), предназначено для хранения в матрице
			шамхматной доски (ChessBoard.matrix)

			i_row		-	ChessBoard.matrix[i_row][i_column]
			i_column 	- 
			cordinats 	- 	кординаты поля, например "e2"
			figure 		- 	фигура (Figure и его наследники)
			available_for_colors 	- множество для хранения цвета
							фигуры для которой доступно поле
			pawn_long_move	- для хранения пешки сделавшей двойной ход
			delay		- задержка для взятия на проходе
		"""
		self.__dict__["i_row"] = i_row
		self.__dict__["i_column"] = i_column
		self.__dict__["cordinats"] = cordinats.lower()
		self.figure = None
		self.available_for_colors = set()
		self.pawn_long_move = None
		self.delay = 0

	def __setattr__(self, attr, value):
		""" Устанавливаем значения для атрибутов"""
		# атрибуты которые не следует менять
		if attr in ("i_row", "i_column", "cordinats"):
			raise AttributeError("you cannot change attribute: " + attr)
		self.__dict__[attr] = value


	def __str__(self):
		""" Строковое представление поля"""
		# short_name фигуры если она есть, либо точка
		return str(self.figure) if self.figure else "."

	def set_color(self, color):
		""" Сообщаем полю что на него может сходить фигура данного цвета"""
		self.available_for_colors.add(color)

	def clear_set_of_colors(self):
		""" Стираем информацию о том какого цвета фигуры могут сходить
			на это поле
			Дополнительно стирает информацию о прохождении пешки этого
			поля длинным ходом, СПУСТЯ два вызова этой функции
		"""
		self.available_for_colors.clear()
		# если есть пешка которая прошла длинным зодом это поле
		if self.pawn_long_move:
			self.delay += 1
			# спустя два хода (обновления шахматной доски 
			# chess_board.update()) забываем пешку, обнуляем задержку
			if self.delay == 2:
				self.pawn_long_move = None
				self.delay = 0

	def copy(self):
		""" Создаём копию поля"""
		# создаём новое поле
		new_field = Field(self.i_row, self.i_column, self.cordinats)
		# создаём идентичиные атрибуты как у поля оригинала
		for attr, value in self.__dict__.items():
			# пропускаем атрибуты которые нельзя менять
			try:
				new_field.__dict__[attr] = value
			except AttributeError:
				pass
		return new_field


class Figure:
	""" Общий класс для всех фигур"""

	def __init__(self, name, short_name, color, chess_board):
		""" Основные свойства фигуры:
			name - имя
			short_name - сокращённое имя
			color - цвет фигуры
			chess_board - объект шахматной доски (ChessBoard)

			field - поле, на котором находится фигура
			was_moved - фигура ходила? (True/False).
						None - если фигура была создана, но не
						поставленна на поле
		"""
		self.name = name
		self.short_name = short_name
		self.color = color
		self.chess_board = chess_board
		self.field = None
		self.attacked = None
		self.was_moved = None
		pass

	def __str__(self):
		""" Строковое представление фигуры"""
		# выводим сокращённое имя, регистр в зависимости от цвета
		# например: белые верхний регистр
		return self.short_name.upper() if self.color == "white" \
			else self.short_name.lower()

	def __del__(self):
		self.field = None

	def go_to(self, cordinats):
		""" Ходит фигурой на указанные кординаты"""
		# желаемое поле, куда хотим сходить
		desired_field = self.chess_board.get_field(cordinats)
		# находим все поля куда может схоить фигура
		available_fields = self.get_available_fields()
		# фильтруем от полей на которых фигура своего цвета
		filtered_fields = self.filter_available_fields(available_fields)
		# если желаемое поле в числе допустимых
		if desired_field in filtered_fields:
			self.set_at_field(desired_field)
		else:
			raise ValueError(
			f"{self.name} at {self.field.cordinats} to {cordinats}" +
			" impossible move")

	def set_at_field(self, field):
		""" Ставим фигуру на поле (field)"""
		# если фигура уже стояла на каком-то поле, сделай это поле 
		# пустым, будет ошибка, если фигура, была создана, но не 
		# установлена на поле
		if self.field:
			self.field.figure = None
		# ставим, фигуру на поле, а у поля устанавливаем фигуру
		self.field = field
		field.figure = self
		# Если фигура была установлена в первый раз 
		# self.was_moved == None при создании, то значит фигура не двигалась
		# инначе фигура двигалась
		self.was_moved = False if self.was_moved == None else True

	def filter_available_fields(self, available_fields):
		""" Отсеивает доступные поля, например, если на поле стоит фигура
			союзного цвета.
		"""
		filtered_fields = []
		for field in available_fields:
			# если фигура есть, и она цвета противника, то на это поле
			# можно сходить, если фигуры нет, то на поле можно сходить
			if field.figure:
				if field.figure.color != self.color:
					filtered_fields.append(field)
			else:
				filtered_fields.append(field)
		return filtered_fields

	def mark_available_fields(self):
		""" Отмечаем доступные поля цветом этой фигуры"""
		for field in self.get_available_fields():
			field.set_color(self.color)

	def get_available_fields(self):
		""" Метод который должен возвращать список доступных полей.
			(available_fields), список длолжен содержать поля на которые
			может сходить фигура, даже если на поле находится фигура.
			Этот метод должен быть переопределён у классов потомков
		"""
		raise NotImplementedError("you need to create this method")

	def copy(self, chess_board):
		""" Создаём копию фигуры с новым значение шахматной доски"""
		FigureClass = type(self)
		new_figure = FigureClass(color=self.color, chess_board=chess_board)
		return new_figure


class Pawn(Figure):
	""" Класс для фигуры "Пешка" """

	def __init__(self, color, chess_board):
		super().__init__(name="pawn", short_name="p", color=color,
							chess_board=chess_board)
		# словарь ключ строка названия фигуры значение класс 
		# для создания фигуры
		self.choice_answers = {
			"pawn": Pawn,
			"knight": Knight,
			"bishop": Bishop,
			"rook": Rook,
			"queen": Queen,
			}

	def get_available_fields(self):
		"""Возвращает доступные поля для пешки (Pawn)"""
		available_fields = []
		# индексы поля на котором стоит пешка
		i_row, i_column = self.field.i_row, self.field.i_column
		# в зависимости от цвета, пешка идёт либо вверх, либо вниз
		inc = -1 if self.color == "white" else 1
		# находим поле перед пешкой
		next_field = self.chess_board.matrix[i_row + inc][i_column]
		# если поле перед пешкой пустое
		if next_field.figure == None:
			available_fields.append(next_field)	# на это поле можно сходить
			# узнаём горизонталь пешки, например row = "2"
			row = self.field.cordinats[1]
			# если белая или чёрная пешка на стартовой позиции
			if (self.color == "white" and row == "2") \
				or  (self.color == "black" and row == "7"):
				# находим поле для длинного хода
				next_field_2 = \
					self.chess_board.matrix[i_row + inc*2][i_column]
				# если поле пустое, то на него можно сходить
				# заодно отмечаем что одно поле мы пересекли длинным 
				# ходом, нужно для взятия на проходе
				if next_field_2.figure == None:
					available_fields.append(next_field_2)
					# next_field.pawn_long_move = self
					# print(f"next_field: {next_field.cordinats}")
		# ищем поля на которые можно напасть
		row_increment = -1 if self.color == "white" else 1
		right_icnrement, left_increment = 1, -1
		for i_row, i_column in (
				# индексы: 	(ряда перед пешкой, правого столбца)
				# 			(ряда перед пешкой, левого столбца)
				(i_row + row_increment, i_column + right_icnrement),
				(i_row + row_increment, i_column + left_increment),):
			try:
				field = self.chess_board.matrix[abs(i_row)][abs(i_column)]
				# на это поле можно сходить если есть фигура
				# (своя/не своя фигура выяснит filter_available_fields())
				# либо это поле прошла пешка длинным ходом
				if field.figure or field.pawn_long_move:
					available_fields.append(field)
				# print(f"field: {field}, filed.__fict__: {field.__dict__}")
			except IndexError:
				pass
		return available_fields

	def choice_new_figure(self):
		""" Функция выбирает и создаёт новую фигуру.
			Нужно если пешка дойдёт до последней горизонтали
		"""
		choice = input("print new figure: ").lower()
		try:
			FigureClass = self.choice_answers[choice]
		except KeyError:
			raise ValueError("I do not know this figure")
		else:
			new_figure = FigureClass(color=self.color, 
				chess_board=self.chess_board)
			return new_figure

	def set_at_field(self, field):
		""" Устанавливаем фигуру на поле. Если пешка окажется
			на последней горизонтали, то вместо неё ставим другую фигуру
		"""
		# print("set_at_field")
		# если белая или чёрная достигла своей последней горизонтали
		if (field.cordinats[1] == "8" and self.color == "white") \
			or (field.cordinats[1] == "1" and self.color == "black"):
			print("lost horizontal")
			# создаём новую фигуру, устанавливаем её на новое значение
			new_figure = self.choice_new_figure()
			new_figure.set_at_field(field)
			# если ошибок не возникло, то поле на котором была пешка
			# делаем пустым
			if self.field:
				self.field.figure = None
			return 
		# если пешка уже была установлена
		if self.field:
			# если пешка совершает длинный ход
			if ((self.color == "white" and self.field.cordinats[1] == "2") \
				or  \
				(self.color == "black" and self.field.cordinats[1] == "7")) \
				and \
				((self.color == "white" and field.cordinats[1] == "4") \
				or \
				(self.color == "black" and field.cordinats[1] == "5")):
				# print("long move")
				# находим поле которое пересекла пешка \
				inc = -1 if self.color == "white" else 1
				passed_field = \
					self.chess_board.matrix[self.field.i_row + inc] \
						[self.field.i_column]
				# у поля сохраняем что прошла эта пешка
				passed_field.pawn_long_move = self
		# устанавливаем пешку на поле
		super().set_at_field(field)
		# если поле пересекли длинным ходом
		# то совершаем взятие на проходе
		if field.pawn_long_move:
			# print("take on pass")
			pawn = field.pawn_long_move
			if self.color != pawn.color:
				pawn.field.figure = None


class King(Figure):

	def __init__(self, color, chess_board):
		super().__init__(name="king", short_name="k", color=color, 
							chess_board=chess_board)

	def get_available_fields(self):
		""" Возвращает все доступные поля для хода, исключая поля под
			атакой вражеской фигуры
		"""
		available_fields = []
		i_r, i_c = self.field.i_row, self.field.i_column
		for i_r, i_c in (
				# индексы для:
				# i_row		i_column
				(i_r + 1,	i_c - 1), 
				(i_r + 1, 	i_c), 
				(i_r + 1, 	i_c + 1),
				(i_r, 		i_c - 1),
				# (i_r, 		i_c),		# поле на котором стоит король
				(i_r, 		i_c + 1), 
				(i_r - 1, 	i_c - 1), 
				(i_r - 1, 	i_c),
				(i_r - 1, 	i_c + 1),
				):
			try:
				# значения индексов передаём abs(), иначе, король
				# стоя на краю карты ведёт себя некоректно
				field = self.chess_board.matrix[abs(i_r)][abs(i_c)]
			except IndexError:
				continue
			else:
				available_fields.append(field)
		# print([field.cordinats for field in available_fields])
		return available_fields

	def set_at_field(self, field):
		""" Устанваливаем короля на поле field
			проверяет если поле field атаковано, то на него нельзя ставить
			за исключением первая установка на поле 
		"""
		# если фигура не была установлена, то ничего не проверяем
		if self.field:
			# если поле на которое хотим установить, под атакой 
			# другой фигуры, то ставить короля на это поле нельзя
			if not set((self.color, )) >= field.available_for_colors:
				raise ValueError(
				f"king cannot to go to attaked field {field.cordinats}")
		super().set_at_field(field)


class Knight(Figure):

	def __init__(self, color, chess_board):
		super().__init__(name="knight", short_name="n", color=color,
							chess_board=chess_board)

	def get_available_fields(self):
		available_fields = []
		i_r, i_c = self.field.i_row, self.field.i_column
		for i_r, i_c in (
				(i_r + 2,	i_c - 1),
				(i_r + 2,	i_c + 1),
				(i_r - 1,	i_c + 2),
				(i_r + 1,	i_c + 2),
				(i_r - 2,	i_c - 1),
				(i_r - 2,	i_c + 1),
				(i_r - 1,	i_c - 2),
				(i_r + 1,	i_c - 2),
			):
			try:
				# значения индексов передаём abs(), иначе, конь
				# стоя на краю карты ведёт себя некоректно
				field = self.chess_board.matrix[abs(i_r)][abs(i_c)]
			except IndexError:
				continue
			else:
				available_fields.append(field)
		return available_fields


class Bishop(Figure):

	def __init__(self, color, chess_board):
		super().__init__(name="bishop", short_name="b", color=color,
							chess_board=chess_board)

	def get_available_fields(self):
		available_fields = []
		diagonals = []
		for incr_i_r, incr_i_c in (
				(-1, -1),
				(-1, 1),
				(+1, -1),
				(+1, 1),
			):
			diagonal = []
			i_row, i_column = self.field.i_row, self.field.i_column
			while True:
				i_row += incr_i_r
				i_column += incr_i_c
				try:
					field = \
					self.chess_board.matrix[abs(i_row)][abs(i_column)]
				except IndexError:
					break
				else:
					diagonal.append(field)
				# print(f"i_row: {i_row}\ni_column: {i_column}")
				# print(f"field.cordinats: {field.cordinats}")
				if (i_row == 0 or i_column == 0) \
					or (i_row == len(self.chess_board.matrix) - 1 \
					or \
					i_column == len(self.chess_board.matrix[0]) -1):
					diagonals.append(diagonal)
					break
		# print("diagonals")
		# for diagonal in diagonals:
		# 	print([field.cordinats for field in diagonal])
		for diagonal in diagonals:
			for field in diagonal:
				if field.figure:
					available_fields.append(field)
					break				
				else:
					available_fields.append(field)
					continue
		return available_fields


class Rook(Figure):

	def __init__(self, color, chess_board):
		super().__init__(name="rook", short_name="r", color=color,
							chess_board=chess_board)

	def get_available_fields(self):
		available_fields = []
		# индексы поля на котором находится фигура
		i_row, i_column = self.field.i_row, self.field.i_column
		# поля находящиейся слева, справа, сверху, снизу от фигуры
		# без поля на котором фигура!
		left_fields = self.chess_board.matrix[i_row][i_column::-1][1:]
		right_fields = self.chess_board.matrix[i_row][i_column:][1:]
		# вспомогательный список, в котором поля одного столбца
		# на его основе создаём поля сверху и снизу от фигуры
		columns = [row[i_column] for row in self.chess_board.matrix]
		up_fields = columns[i_row::-1][1:]
		down_fields = columns[i_row::][1:]
		# смотрим значения кординат полей справа, слева, сверху и снизу
		# от фигуры
		if 0:
			# print("columns: ", [field.cordinats for field in columns])
			print("left_fields: ", 
				[field.cordinats for field in left_fields])
			print("right_fields: ", 
				[field.cordinats for field in right_fields])
			print("up_fields: ", 
				[field.cordinats for field in up_fields])
			print("down_fields: ", 
				[field.cordinats for field in down_fields])
		for fields in (left_fields, right_fields, up_fields, down_fields):
			for field in fields:
				if field.figure:
					available_fields.append(field)
					break				
				else:
					available_fields.append(field)
					continue
		# print(f"available_fields: {available_fields}")
		return available_fields


class Queen(Figure):

	def __init__(self, color, chess_board):
		super().__init__(name="queen", short_name="q", color=color,
							chess_board=chess_board)

	def get_available_fields(self):
		available_fields = []
		available_fields.extend(Bishop.get_available_fields(self))
		available_fields.extend(Rook.get_available_fields(self))
		# print([field.cordinats for field in available_fields])
		return available_fields


if __name__ == "__main__":
	app = ConsoleApp()
	app()
