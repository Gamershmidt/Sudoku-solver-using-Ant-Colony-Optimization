from Unit import Unit
class Grid:
    def __init__(self, dimension=3):
        self.dimension = dimension
        self.size = self.dimension**2
        self.sudoku = [[Unit(self.dimension) for _ in range(self.size)] for _ in range(self.size)]

    def finalized(self):
        for i in range(self.size):
            for j in range(self.size):
                if not self.sudoku[i][j].fixed():
                    return False

        return True

    def set_cell(self, i, j, value):
        self.sudoku[i][j].set_values(value)

    def update_cell_values(self, pos_i, pos_j):
        if not self.sudoku[pos_i][pos_j].check_fixed():
            return
        for i in range(self.size):
            if i != pos_i:
                self.sudoku[i][pos_j].drop_possible(self.sudoku[i][pos_j].value)
                if self.sudoku[i][pos_j].check_fixed():
                    self.update_cell_values(i, pos_j)
        for j in range(self.size):
            if j != pos_j:
                self.sudoku[pos_i][j].drop_possible(self.sudoku[pos_i][j].value)
                if self.sudoku[pos_i][j].check_fixed():
                    self.update_cell_values(pos_i, j)
        # add checker for small squares