WHITE = 1
BLACK = 2


class Board:
    def __init__(self):
        self.board = [
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]
        ]
        self.color = BLACK

    def print_board(self):
        print('     +----+----+----+----+----+----+----+----+')
        for row in range(7, -1, -1):
            print(' ', row, end='  ')
            for col in range(8):
                print('|', self.board[row][col], end=' ')
            print('|')
            print('     +----+----+----+----+----+----+----+----+')
        print(end='        ')
        for col in range(8):
            print(col, end='    ')
        print()

    def __str__(self):
        s = ""
        s += '     +----+----+----+----+----+----+----+----+\n'
        for row in range(7, -1, -1):
            s += '  {}  |'.format(row)
            for col in range(8):
                s += ' {} |'.format(self.board[row][col])
            s += ' \n'.format()
            s += '     +----+----+----+----+----+----+----+----+\n'
        s += '        0    1    2    3    4    5    6    7\n'
        return s

    def piece(self, name, row, col, color):
        if name[1] == 'P':
            return Pawn(row, col, color)
        elif name[1] == 'R':
            return Rook(row, col, color)
        elif name[1] == 'K':
            return King(row, col, color)
        elif name[1] == 'B':
            return Bishop(row, col, color)
        elif name[1] == 'Q':
            return Queen(row, col, color)
        elif name[1] == 'N':
            return Knight(row, col, color)

    def move_piece(self, row, col, row1, col1):
        piece = self.piece(self.board[row][col], row, col, self.color)
        if self.board[row1][col1] != "  ":
            return False
        elif piece.can_move(row1, col1) and piece.not_piece(self.board, piece, row1, col1):
            self.board[row][col] = "  "
            if piece.get_color() == 1:
                color = "b"
            else:
                color = "w"
            self.board[row1][col1] = color + piece.char()
            self.color = opponent(self.color)
            return True
        return False


class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color


class King(Piece):

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def char(self):
        return 'K'

    def get_color(self):
        return self.color

    def can_move(self, row, col):
        if not (0 <= row <= 7) or not (0 <= col <= 7):
            return False
        if abs(self.row - row) <= 1 and abs(self.col - col) <= 1:
            return True

        return False

    def not_piece(self, board, piece, row, col):
        return True


class Pawn(Piece):

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def char(self):
        return 'P'

    def get_color(self):
        return self.color

    def can_move(self, row, col):
        if self.col != col:
            return False
        if self.color == BLACK:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6
        if self.row + direction == row:
            return True
        if self.row == start_row and self.row + 2 * direction == row:
            return True

        return False

    def not_piece(self, board, piece, row, col):
        """Артибут проверки не перешагивате ли ладья через другую фигуру"""
        row1, col1 = piece.row, piece.col
        if board[row1 + 1][col1] == "  ":
            return True
        if board[row1 - 1][col1] == "  ":
            return True
        else:
            return False


class Rook(Piece):

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def char(self):
        return 'R'

    def get_color(self):
        return self.color

    def can_move(self, row, col):
        if self.row != row and self.col != col:
            return False

        return True

    def not_piece(self, board, piece, row, col):

        """Артибут проверки не перешагивате ли ладья через другую фигуру"""
        if piece.col == col:
            if row > piece.row:
                row1, col1 = piece.row, piece.col
                while row1 != row:
                    row1 += 1
                    if board[row1][col1] != "  ":
                        return False
                return True
            else:
                row1, col1 = piece.row, piece.col
                while row1 != row:
                    row1 -= 1
                    if board[row1][col1] != "  ":
                        return False
                return True
        else:
            if col > piece.col:
                row1, col1 = piece.row, piece.col
                while col1 != col:
                    col1 += 1
                    if board[row1][col1] != "  ":
                        return False
                return True
            else:
                row1, col1 = piece.row, piece.col
                while col1 != col:
                    col1 -= 1
                    if board[row1][col1] != "  ":
                        return False
                return True


class Knight(Piece):

    def set_position(self, row1, col1):
        self.row = row1
        self.col = col1

    def get_color(self):
        return self.color

    def char(self):
        return "N"

    def can_move(self, row, col):
        if not (0 <= row <= 7) or not (0 <= col <= 7):
            return False
        if abs(self.row - row) * abs(self.col - col) != 2:
            return False
        return True

    def not_piece(self, board, piece, row, col):
        return True


class Bishop(Piece):

    def set_position(self, row1, col1):
        self.row = row1
        self.col = col1

    def get_color(self):
        return self.color

    def char(self):
        return "B"

    def can_move(self, row, col):
        if not (0 <= row <= 7) or not (0 <= col <= 7):
            return False
        if abs(self.col - col) != abs(self.row - row):
            return False
        return True

    def not_piece(self, board, piece, row, col):

        """Атрибут проверки не перешагивает ли слон через другую фигуру"""
        if abs(piece.row - row) == abs(piece.col - col):
            # Проверяем, движется ли слон по диагонали
            if row > piece.row and col > piece.col:
                # Движение вправо вниз
                row1, col1 = piece.row, piece.col
                while row1 != row and col1 != col:
                    row1 += 1
                    col1 += 1
                    if board[row1][col1] != "  ":
                        return False
                return True
            elif row > piece.row and col < piece.col:
                # Движение влево вниз
                row1, col1 = piece.row, piece.col
                while row1 != row and col1 != col:
                    row1 += 1
                    col1 -= 1
                    if board[row1][col1] != "  ":
                        return False
                return True
            elif row < piece.row and col > piece.col:
                # Движение вправо вверх
                row1, col1 = piece.row, piece.col
                while row1 != row and col1 != col:
                    row1 -= 1
                    col1 += 1
                    if board[row1][col1] != "  ":
                        return False
                return True
            else:
                # Движение влево вверх
                row1, col1 = piece.row, piece.col
                while row1 != row and col1 != col:
                    row1 -= 1
                    col1 -= 1
                    if board[row1][col1] != "  ":
                        return False
                return True
        else:
            return False  # Если слон не движется по диагонали


class Queen(Piece):

    def set_position(self, row1, col1):
        self.row = row1
        self.col = col1

    def get_color(self):
        return self.color

    def char(self):
        return "Q"

    def can_move(self, row, col):
        if not (0 <= row <= 7) or not (0 <= col <= 7):
            return False
        if self.row == row or self.col == col:
            return True
        if abs(self.col - col) == abs(self.row - row):
            return True
        return False

    def not_piece(self, board, row, col):
        if self.row == row or self.col == col:
            # Проверка на наличие других фигур на пути движения по вертикали или горизонтали (аналогично ладье)
            step = 1 if col == self.col else -1
            col1 = self.col + step
            while col1 != col:
                if board[row][col1] != "  ":
                    return False
                col1 += step

            step = 1 if row == self.row else -1
            row1 = self.row + step
            while row1 != row:
                if board[row1][col] != "  ":
                    return False
                row1 += step

            return True

        elif abs(self.row - row) == abs(self.col - col):
            # Проверка на наличие других фигур на пути движения по диагонали (аналогично слону)
            row_step = 1 if row > self.row else -1
            col_step = 1 if col > self.col else -1
            row1, col1 = self.row + row_step, self.col + col_step
            while row1 != row:
                if board[row1][col1] != "  ":
                    return False
                row1 += row_step
                col1 += col_step

            return True

        else:
            # Если королева движется по неправильному направлению, то она не проходит сквозь другие фигуры
            return False


def opponent(color):
    if color == WHITE:
        return BLACK
    return WHITE


def game():
    b = Board()
    while True:
        print(b)
        if b.color == 2:
            print("Ходят белые")
        else:
            print("Ходят черные")
        # Ввежите столбец и строку фигуры, которой хотите сходить, и столбец и строку куда хотите ее поставить
        row, col, row1, col1 = map(int, input().split())
        piece = b.piece(b.board[row][col], row, col, b.color)
        print(piece, piece.can_move(row1, col1), piece.not_piece(b.board, piece, row1, col1))
        if piece.can_move(row1, col1) and piece.not_piece(b.board, piece, row1, col1) and b.board[row1][col1] == "  ":
            b.board[row][col] = "  "
            if piece.get_color() == 1:
                color = "b"
            else:
                color = "w"
            b.board[row1][col1] = color + piece.char()
            print("OK")
            b.color = opponent(b.color)
        else:
            print("NOT OK")


if __name__ == "__main__":
    game()
