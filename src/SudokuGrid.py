from Unit import Unit
class Grid:
    def __init__(self, dimension=3):
        self.dimension = dimension
        self.size = self.dimension**2
        self.sudoku = [[Unit(self.dimension) for _ in range(self.size)] for _ in range(self.size)]

    def finalized(self):
        for i in range(self.size):
            for j in range(self.size):
                if not self.sudoku[i][j].is_cell_fixed():
                    return False

        return True

    def set_cell(self, i, j, value):
        self.sudoku[i][j].set_cell(value)
    def fix_cell(self, i, j, value):
        if not self.sudoku[i][j].is_cell_incorrect():
            self.sudoku[i][j].fix_cell(value)

    def update_cell_values(self, pos_i, pos_j):
        if not self.sudoku[pos_i][pos_j].is_cell_fixed():
            return
        for i in range(self.size):
            if i != pos_i:
                self.sudoku[i][pos_j].drop_possible(self.sudoku[pos_i][pos_j].value)

        for j in range(self.size):
            if j != pos_j:
                self.sudoku[pos_i][j].drop_possible(self.sudoku[pos_i][pos_j].value)

        row_square = pos_i // self.dimension
        column_square = pos_j // self.dimension
        start_i = row_square * self.dimension
        start_j = column_square * self.dimension

        for i in range(start_i, start_i + self.dimension):
            for j in range(start_j, start_j + self.dimension):
                if (i != pos_i or j != pos_j):
                    self.sudoku[i][j].drop_possible(self.sudoku[pos_i][pos_j].value)

        # add checker for small squares
    def propagate_new_constraint(self, pos_i, pos_j):
        for i in range(self.size):
            if i != pos_i:
                self.sudoku[i][pos_j].drop_possible(self.sudoku[pos_i][pos_j].value)
        for j in range(self.size):
            if j != pos_j:
                self.sudoku[pos_i][j].drop_possible(self.sudoku[pos_i][pos_j].value)
                # add checker for small squares
                row_square = pos_i // self.dimension
                column_square = pos_j // self.dimension
                start_i = row_square * self.dimension
                start_j = column_square * self.dimension
        for i in range(start_i, start_i + self.dimension):
            for j in range(start_j, start_j + self.dimension):
                if (i != pos_i or j != pos_j):
                    self.sudoku[i][j].drop_possible(self.sudoku[pos_i][pos_j].value)

    def print_grid(self):
        print(f"Size: ", len(self.sudoku[0]))
        for i in range(len(self.sudoku[0])):
            for j in range(len(self.sudoku[1])):
                print(self.sudoku[i][j].value, end=' ')
            print()

    def get_cell_from_grid(self, i, j):
        return self.sudoku[i][j]
    def get_possible_values(self, row, column):
        return self.sudoku[row][column].get_possible_values()

    def check_fixed_cell(self, row, column):
        return self.sudoku[row][column].is_cell_fixed()