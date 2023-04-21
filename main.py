WHITE = 1
BLACK = 2


# Удобная функция для вычисления цвета противника
def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def print_board(board):  # Распечатать доску в текстовом виде (см. скриншот)
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(col, end='    ')
    print()


def main():
    # Создаём шахматную доску
    board = Board()
    # Цикл ввода команд игроков
    while True:
        # Выводим положение фигур на доске
        print_board(board)
        # Подсказка по командам
        print('Команды:')
        print('    exit                               -- выход')
        print('    move <row> <col> <row1> <row1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')
        print('    casting                             -- рокировка')
        print('    transformation <row> <col> <row1> <row1> <char>\n'
              '                                        -- превращение пешки')
        print(
            '                                       (char) название фигуры в которую произойдет'
            ' превращение')
        # Выводим приглашение игроку нужного цвета
        if board.current_player_color() == WHITE:
            print('Ход белых:')
        else:
            print('Ход чёрных:')
        if board.mate():
            if board.board_check():
                print("Шах и мат, игра завершена!")
                break
            else:
                print("Шах!")
        command = input()
        if command == 'exit':
            break
        if command.split()[0] == "casting":
            if board.current_player_color() == WHITE:
                if board.castling0():
                    print("Рокировка прошла успешно")
                else:
                    print("Нет возможности сделать рокировку")
            else:
                if board.castling7():
                    print("Рокировка прошла успешно")
                else:
                    print("Нет возможности сделать рокировку")
        if "transformation" in command.split()[0]:
            move_type, row, col, row1, col1, char = command.split()
            row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
            if board.move_and_promote_pawn(row, col, row1, col1, char):
                print("Превращение пешки прошло успешно")
            else:
                print("Некорректные данные")
        else:
            move_type, row, col, row1, col1 = command.split()
            row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
            if board.move_piece(row, col, row1, col1):
                print('Ход успешен')
            else:
                print('Координаты некорректны! Попробуйте другой ход!')


def correct_coords(row, col):
    '''Функция проверяет, что координаты (row, col) лежат
    внутри доски'''
    return 0 <= row < 8 and 0 <= col < 8


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]
        self.moves = []

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        '''Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела.'''
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def move_piece(self, row, col, row1, col1):
        '''Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False'''
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        if isinstance(piece, King) or isinstance(piece, Rook):
            self.moves.append(piece)
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        if self.mate():
            self.field[row][col] = piece  # Снять фигуру.
            self.field[row1][col1] = None
            if isinstance(piece, King) or isinstance(piece, Rook):
                self.moves.pop(-1)
            return False
        self.color = opponent(self.color)
        return True

    def move_and_promote_pawn(self, row, col, row1, col1, char):
        '''Функция проверки может ли пешка превратиться в другую фигуру'''
        piece = self.field[row][col]
        if isinstance(piece, Pawn):
            if self.field[row][col] is None:
                return False
            if char == "P" or char == "K":
                return False
            if abs(col - col1) == abs(row1 - row) == 1 and self.field[row1][col1] is not None:
                if row1 == 0 or row1 == 7:
                    if self.field[row1][col1].get_color() != piece.get_color():
                        if char == "N":
                            self.move_piece(row, col, row1, col1)
                            self.field[row1][col1] = Knight(piece.get_color())
                        elif char == "Q":
                            self.move_piece(row, col, row1, col1)
                            self.field[row1][col1] = Queen(piece.get_color())
                        elif char == "R":
                            self.move_piece(row, col, row1, col1)
                            self.field[row1][col1] = Rook(piece.get_color())
                        elif char == "B":
                            self.move_piece(row, col, row1, col1)
                            self.field[row1][col1] = Bishop(piece.get_color())
                        return True
                    return False
                return False
            elif abs(row - row1) == 1 and col1 == col and self.field[row1][col1] is None:
                if char == "N":
                    self.move_piece(row, col, row1, col1)
                    self.field[row1][col1] = Knight(piece.get_color())
                elif char == "Q":
                    self.move_piece(row, col, row1, col1)
                    self.field[row1][col1] = Queen(piece.get_color())
                elif char == "R":
                    self.move_piece(row, col, row1, col1)
                    self.field[row1][col1] = Rook(piece.get_color())
                elif char == "B":
                    self.move_piece(row, col, row1, col1)
                    self.field[row1][col1] = Bishop(piece.get_color())
                return True
            return False
        return False

    def castling0(self):
        '''Ракировка белых'''
        cor = ((0, 0), (0, 4)) if self.color == WHITE else ((7, 0), (7, 4))
        r, k = cor
        if self.field[k[0]][k[1]] is None or self.field[r[0]][r[1]] is None:
            return False
        fig_k = self.get_piece(k[0], k[1])
        fig_r = self.get_piece(r[0], r[1])
        if fig_k.char() != 'K' or fig_r.char() != 'R':
            return False
        if fig_k in self.moves or fig_r in self.moves:
            return False
        if fig_k.get_color() != fig_r.get_color():
            return False
        if fig_r.can_move(self, r[0], r[1], k[0], k[1]):
            self.field[r[0]][r[1]] = None
            self.field[k[0]][k[1]] = None
            fig_r.rak = False
            fig_k.rak = False
            self.field[r[0]][3] = fig_r
            self.field[k[0]][2] = fig_k
        else:
            return False
        self.color = opponent(self.color)
        return True

    def castling7(self):
        '''Ракировка черных'''
        cor = ((0, 7), (0, 4)) if self.color == WHITE else ((7, 7), (7, 4))
        r, k = cor
        if self.field[k[0]][k[1]] is None or self.field[r[0]][r[1]] is None:
            return False
        fig_k = self.get_piece(k[0], k[1])
        fig_r = self.get_piece(r[0], r[1])
        if fig_k.char() != 'K' or fig_r.char() != 'R':
            return False
        if fig_k in self.moves or fig_r in self.moves:
            return False
        if fig_k.get_color() != fig_r.get_color():
            return False
        if fig_r.can_move(self, r[0], r[1], k[0], k[1]):
            self.field[r[0]][r[1]] = None
            self.field[k[0]][k[1]] = None
            fig_r.rak = False
            fig_k.rak = False
            self.field[r[0]][5] = fig_r
            self.field[k[0]][6] = fig_k
        else:
            return False
        self.color = opponent(self.color)
        return True

    def is_under_attack(self, row, col, color):
        for i in range(8):
            for j in range(8):
                if self.field[i][j] is not None and (not (isinstance(self.field[i][j], King))):
                    piece = self.field[i][j]
                    if piece.get_color() != color:
                        if piece.can_move(self, i, j, row, col):
                            return True
        return False

    def mate(self):
        '''Проверка на мат'''
        row, col = 0, 0
        for i in range(8):
            for j in range(8):
                if isinstance(self.field[i][j], King) and self.field[i][j].get_color() == self.color:
                    row, col = i, j
        if self.is_under_attack(row, col, self.color):
            return True
        return False

    def all_moves(self, piece, i, j):
        '''Получение всех возможных ходов заданной фигурой'''
        moves = []
        for row in range(8):
            for col in range(8):
                if self.move_piece(i, j, row, col):
                    if self.field[row][col] is None:
                        moves.append((row, col))
                    else:
                        if self.field[row][col].get_color() != piece.get_color():
                            moves.append((row, col))

        return moves

    def board_check(self):
        '''Проверка на шах и мат'''
        if self.mate():
            color = self.color
            piece = ""
            row, col = 0, 0
            for i in range(8):
                for j in range(8):
                    if isinstance(self.field[i][j], King) and self.field[i][j].get_color() == self.color:
                        row, col = i, j
                        piece = self.field[i][j]
            if piece != "":
                row2, col2 = 0, 0
                piece = ""
                for i in range(8):
                    for j in range(8):
                        if self.field[i][j] is not None and (not (isinstance(self.field[i][j], King))):
                            piece2 = self.field[i][j]
                            if piece2.get_color() != color:
                                if piece2.can_move(self, i, j, row, col):
                                    row2, col2 = i, j
                                    piece = self.field[i][j]
                for i in range(8):
                    for j in range(8):
                        if self.field[i][j] is not None and (not (isinstance(self.field[i][j], King))):
                            if (row2, col2) in self.all_moves(self.field[i][j], i, j):
                                print(row2, col2)
                                return False
                if len(self.all_moves(piece, row, col)) == 0:
                    return True
                return False
            return False
        return False


class Rook:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            # Если на пути по горизонтали есть фигура
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по вертикали есть фигура
            if not (board.get_piece(row, c) is None):
                return False

        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Pawn:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано
        if col != col1:
            return False

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        # ход на 1 клетку
        if row + direction == row1:
            return True

        # ход на 2 клетки из начального положения
        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True

        return False

    def can_attack(self, board, row, col, row1, col1):
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))


class Knight:
    '''Класс коня. Пока что заглушка, которая может ходить в любую клетку.'''

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'N'  # kNight, буква 'K' уже занята королём

    def can_move(self, board, row, col, row1, col1):
        if not (0 <= row <= 7) or not (0 <= col <= 7):
            return False
        if abs(row - row1) * abs(col - col1) != 2:
            return False
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King:
    '''Класс короля. Пока что заглушка, которая может ходить в любую клетку.'''

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        if not (0 <= row1 <= 7) or not (0 <= col1 <= 7):
            return False
        if abs(row - row1) <= 1 and abs(col - col1) <= 1:
            return True

        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen:
    '''Класс ферзя. Пока что заглушка, которая может ходить в любую клетку.'''

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        piece1 = board.get_piece(row1, col1)
        if not (piece1 is None) and piece1.get_color() == self.color:
            return False
        if row != row1 and col != col1 and abs(row - row1) != abs(col - col1):
            return False
        elif row == row1 and col == col1:
            return False
        if row == row1 or col == col1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                # Если на пути по вертикали есть фигура
                if not (board.get_piece(r, col) is None):
                    return False

            step = 1 if (col1 >= col) else -1
            for c in range(col + step, col1, step):
                # Если на пути по горизонтали есть фигура
                if not (board.get_piece(row, c) is None):
                    return False

        # Дополнительная проверка для случая диагонального движения вправо вниз.
        if abs(row - row1) == abs(col - col1):
            if row1 - row > 0 and col1 - col < 0:
                step_r = 1
                step_c = -1
                row_check = row + step_r
                col_check = col + step_c
                while row_check != row1 and col_check != col1:
                    if board.get_piece(row_check, col_check) is not None:
                        return False
                    row_check += step_r
                    col_check += step_c
            elif row1 - row < 0 and col1 - col > 0:
                step_r = -1
                step_c = 1
                row_check = row + step_r
                col_check = col + step_c
                while row_check != row1 and col_check != col1:
                    if board.get_piece(row_check, col_check) is not None:
                        return False
                    row_check += step_r
                    col_check += step_c
            elif row1 - row < 0 and col1 - col < 0:
                step_r = -1
                step_c = -1
                row_check = row + step_r
                col_check = col + step_c
                while row_check != row1 and col_check != col1:
                    if board.get_piece(row_check, col_check) is not None:
                        return False
                    row_check += step_r
                    col_check += step_c
            elif row1 - row > 0 and col1 - col > 0:
                step_r = 1
                step_c = 1
                row_check = row + step_r
                col_check = col + step_c
                while row_check != row1 and col_check != col1:
                    if board.get_piece(row_check, col_check) is not None:
                        return False
                    row_check += step_r
                    col_check += step_c
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Bishop:
    '''Класс слона. Пока что заглушка, которая может ходить в любую клетку.'''

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        if abs(row - row1) == abs(col - col1):
            row_step = 1 if row1 > row else -1
            col_step = 1 if col1 > col else -1
            row_check, col_check = row + row_step, col + col_step

            while row_check != row1 and col_check != col1:
                if board.get_piece(row_check, col_check) is not None:
                    return False
                row_check += row_step
                col_check += col_step

        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


if __name__ == "__main__":
    main()
