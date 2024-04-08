import random

import numpy as np
from SudokuGrid import Grid

class Ant:
    def __init__(self, grid= None, pheromone_matrix = None, row = 0, column = 0, default_pheromone = 1/81, local_evaporation_rate = 0.01):
        if not grid:
            self.board_size = 81
        else:
            self.board_size = grid.size
        self.grid = grid
        self.num_of_fixed = 0
        self.num_of_incorrect = 0
        self.pheromone_matrix = pheromone_matrix
        self.row = row
        self.column = column
        self.default_pheromone = default_pheromone
        self.local_evaporation_rate = local_evaporation_rate
        self.num_of_visited = 0

    def perform_move(self):
        self.move_one_cell()
        self.num_of_visited += 1
        cur_cell_possible_values = self.grid.get_possible_values(self.row, self.column)

        if self.grid.check_fixed_cell(self.row, self.column):
            self.num_of_fixed += 1
        elif len(cur_cell_possible_values) == 0:
            self.num_of_incorrect += 1
        else:
            # choose value from current cell’s value set;
            pheromones_sum = 0
            for val in cur_cell_possible_values:
                pheromones_sum += self.pheromone_matrix[self.row][self.column][val-1]
            probabilities = [self.pheromone_matrix[self.row][self.column][cur_cell_possible_values[i] - 1] / pheromones_sum for i in range(len(cur_cell_possible_values))]
            chosen_value = np.random.choice(cur_cell_possible_values, p=probabilities)

            # fix value
            self.grid.sudoku[self.row][self.column].fix_cell(chosen_value)
            self.num_of_fixed += 1

            # propagate constraints
            self.grid.update_cell_values(self.row, self.column)

            # local pheromone update
            self.pheromone_matrix[self.row][self.column][chosen_value - 1] = (
                    (1 - self.local_evaporation_rate) * self.pheromone_matrix[self.row][self.column][
                chosen_value - 1] + self.local_evaporation_rate * self.default_pheromone)

    def move_one_cell(self):
        if self.column+1 < self.board_size:
            self.column += 1
        elif self.row + 1 < self.board_size:
            self.row += 1
            self.column = 0
        elif self.row == 8 and self.column == 8 and self.num_of_visited < 81:
            self.row = 0
            self.column = 0

    def get_f(self):
        return self.num_of_fixed - self.num_of_incorrect