import copy
import random

from SudokuGrid import Grid
from Ant import Ant

# initial_grid = [
#     [0, 6, 0, 0, 0, 0, 5, 0, 2],
#     [0, 3, 0, 0, 7, 0, 0, 0, 0],
#     [0, 2, 0, 3, 6, 0, 0, 0, 7],
#     [8, 7, 3, 0, 2, 1, 4, 5, 0],
#     [9, 4, 0, 5, 0, 0, 0, 0, 0],
#     [0, 1, 0, 0, 0, 4, 0, 0, 0],
#     [0, 0, 0, 0, 9, 5, 0, 0, 4],
#     [3, 9, 4, 8, 1, 0, 0, 7, 5],
#     [0, 5, 1, 0, 6, 3, 0, 9, 8],
# ]
initial_grid = [[0,6,0,0,0,0,5,0,2],
[0,3,0,0,7,0,0,0,0],
[0,2,0,3,6,0,0,0,7],
[8,7,3,0,2,1,4,5,0],
[9,4,0,5,0,0,0,0,0],
[0,1,0,0,0,4,0,0,0],
[0,0,0,0,9,5,0,0,4],
[3,9,4,8,1,0,0,7,5],
[0,5,1,0,6,3,0,9,8]
]




class AntColony:
    def __init__(self, num_of_ants, local_evaporation_rate, global_evaporation_rate,
                 initial_grid, dimension):
        self.num_of_ants = num_of_ants
        self.local_evaporation_rate = local_evaporation_rate
        self.global_evaporation_rate = global_evaporation_rate
        self.delta_tau_best_evaporation = 0.995

        self.initial_grid = initial_grid
        self.current_grid = Grid(dimension)
        self.grid_size = dimension ** 2
        self.num_of_cells = self.grid_size ** 2
        self.default_pheromone = 1 / self.num_of_cells
        self.pheromone_matrix = [
            [[self.default_pheromone for i in range(self.grid_size)] for j in range(self.grid_size)] for k
            in range(self.grid_size)]
        self.ants = [Ant() for i in range(num_of_ants)]
        self.default_pheromone = 1 / self.num_of_cells
        self.delta_tau_best = 0
        self.best_ant = None
        fixed_num = 0
        # filling current sudoku grid
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                # if self.initial_grid[i][j] != 0:
                # self.current_grid.sudoku[i][j].fixed = True
                cur_value = self.initial_grid[i][j]
                self.current_grid.set_cell(i, j, cur_value)
                if (self.initial_grid[i][j] != 0):
                    fixed_num += 1
                    # self.current_grid.propagate_new_constraint(i, j)
                    # propagate constraints
                    self.current_grid.update_cell_values(i, j)
        self.solved_grid = copy.deepcopy(self.current_grid)
        print("num of fixed ")

    def solve_sudoku(self):
        sudoku_solved = False
        num_of_iterations = 0
        while not sudoku_solved:
            self.ants = [Ant(grid=copy.deepcopy(self.current_grid),
                             pheromone_matrix=self.pheromone_matrix,
                             row=random.randint(0, self.grid_size - 1),
                             column=random.randint(0, self.grid_size - 1),
                             default_pheromone=self.default_pheromone,
                             local_evaporation_rate=self.local_evaporation_rate
                             ) for i in range(self.num_of_ants)]

            self.solved_grid.print_grid()
            num_of_iterations += 1

            print(num_of_iterations, self.delta_tau_best)

            for i in range(self.num_of_cells):
                for j in range(self.num_of_ants):
                    current_ant = self.ants[j]
                    current_ant.perform_move()
            # for ant in self.ants:
            #     print(ant.num_of_fixed, ant.num_of_incorrect, ant.get_f())
            #     ant.grid.print_grid()

            num_of_fixed = 0
            self.best_ant = None
            for ant in self.ants:
                print(ant.num_of_fixed, ant.num_of_incorrect, ant.get_f())
                if ant.get_f() > num_of_fixed:
                    num_of_fixed = ant.get_f()
                    self.best_ant = ant
                    self.solved_grid = self.best_ant.grid
                if num_of_fixed == self.num_of_cells:
                    print('Solved!!!!!', num_of_fixed, self.best_ant.num_of_incorrect, self.best_ant.num_of_fixed)
                    self.best_ant.grid.print_grid()
                    exit()
             # calculate delta_tau
            delta_tau = self.num_of_cells/(self.num_of_cells - self.best_ant.get_f())
            if delta_tau > self.delta_tau_best:
               self.delta_tau_best = delta_tau

            # global pheromone update
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    cur_cell = self.best_ant.grid.sudoku[i][j]
                    if not cur_cell.is_cell_incorrect:
                        self.pheromone_matrix[i][j][cur_cell.value - 1] = (
                                (1 - self.global_evaporation_rate) * self.pheromone_matrix[i][j][cur_cell.value - 1] +
                                self.global_evaporation_rate * self.default_pheromone)

            self.delta_tau_best = self.delta_tau_best * self.delta_tau_best_evaporation

num_of_ants = 15
dim = 3
local_evaporation_rate = 0.1
global_evaporation_rate = 0.9
ant_colony = AntColony(num_of_ants, local_evaporation_rate, global_evaporation_rate, initial_grid, dim)
ant_colony.current_grid.print_grid()
print(ant_colony.current_grid.sudoku[0][0].set_values)
ant_colony.solve_sudoku()
