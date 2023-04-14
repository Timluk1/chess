WHITE = 1
BLACK = 2


class Board:
    def __init__(self):
        self.board = [
            ["wR", "wN", "wB", "wK", "wQ", "wB", "wN", "wR"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]
        ]
        self.color = WHITE

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
        s += '    +----+----+----+----+----+----+----+----+\n'
        for row in range(7, -1, -1):
            s += '  {} |'.format(row)
            for col in range(8):
                s += ' {} |'.format(self.board[row][col])
            s += ' \n'.format()
            s += '    +----+----+----+----+----+----+----+----+\n'
        s += '      0    1    2    3    4    5    6    7\n'
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
        if piece.col == col:
            row1, col1 = piece.row, piece.col
            while row1 != row:
                print(board[row1][col1])
                if board[row1][col1] != "  ":
                    return False
                row1 += 1
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


def what_color(color):
    if color == 2:
        return "b"
    return "w"


def what_color_reverse(color):
    if color == "b":
        return 2
    return 1


def is_path_clear(new_row, new_col, board, piece, color):
    flag = False
    if color == "w":
        for i in range(7, -1, -1):
            for j in range(7, -1, -1):
                if piece.can_move(i, j) and board[i][j] != "  ":
                    flag = True
                if flag and i == new_row and j == new_col:
                    return False
        return True
    else:
        for i in range(0, 8):
            for j in range(0, 8):
                if piece.can_move(i, j) and board[i][j] != "  ":
                    flag = True
                if flag and i == new_row and j == new_col:
                    return False
        return True


def game():
    b = Board()
    print(b)
    row, col, row1, col1 = map(int, input().split())
    piece = b.piece(b.board[row][col], row, col, 1)
    print(piece.not_piece(b.board, piece, row1, col1))


if __name__ == "__main__":
    game()
