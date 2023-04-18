    def castling0(self):
        '''Можно ли сделать рокировку белым,
        вернет True и сделает рокировку, если можно и False, если нельзя'''

        if isinstance(self.field[0][4], King) :
            if isinstance(self.field[0][0], Knight) and self.field[0][4].get_color() == self.field[0][0].get_color():
                if self.field[0][2] is None and self.field[0][3] is None:
                    self.field[0][2] = self.field[0][4]
                    self.field[0][4] = None
                    self.field[0][3] = self.field[0][0]
                    self.field[0][0] = None
                    return True
                elif self.field[0][6] is None and self.field[0][5] is None:
                    self.field[0][6] = self.field[0][4]
                    self.field[0][4] = None
                    self.field[0][5] = self.field[0][7]
                    self.field[0][7] = None
                    return True
                return False
            return False
        return False
