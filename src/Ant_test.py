import random
import numpy as np
from SudokuGrid import Grid

num_of_cells = 9 ** 2
default_pheromone = 1 / num_of_cells
class Ant_test:
    def __init__(self, grid: Grid, pheromone_matrix = None, row, column, board_size, eps):
        self.grid = grid
        num_of_cells = board_size**2
        default_pheromone = 1/num_of_cells
        self.local_pheromone_matrix = pheromone_matrix
        self.row = row
        self.column = column
        self.board_size = board_size
        self.fitness = 0
        self.num_of_incorrect = 0
        self.eps = eps
        self.num_of_fixed_cells = 0

    def perform_move(self):
        self.move_one_cell()
        if self.grid.get_cell(self.row, self.column).check_fixed():
            self.move_one_cell()
        elif self.grid.get_cell(self.row, self.column).impossible():
            self.num_of_incorrect += 1
            pass
        else:

            # choose value from current cell’s value set;
            possible_values = self.grid.get_possible_values(self.row, self.column)
            probabilities = [self.local_pheromone_matrix[self.row][self.column][i]/np.sum(self.local_pheromone_matrix[self.row][self.column]) for i in range(len(possible_values))]

            # choose value from possible
            chosen_value = np.random.choice(possible_values, probabilities)
            chosen_value_idx = -1
            for i in range(len(possible_values)):
                if possible_values[i] == chosen_value:
                    chosen_value_idx = i

            # fix cell value;
            self.grid.set_cell(self.row, self.column, chosen_value)
            # propagate constraints;
            self.grid.update_cell_values(self.row, self.column)
            # update local pheromone;
            self.local_pheromone_matrix[self.row][self.column][chosen_value_idx] = (
                    (1 - self.eps)*self.local_pheromone_matrix[self.row][self.column][chosen_value_idx] + self.eps*default_pheromone)

    def move_one_cell(self):
        if self.column+1 < self.board_size:
            self.column += 1
        elif self.row + 1 < self.board_size:
            self.row += 1
            self.column = 0