import random

from SudokuGrid import Grid

initial_grid = [
    [0, 6, 0, 0, 0, 0, 5, 0, 2],
    [0, 3, 0, 0, 7, 0, 0, 0, 0],
    [0, 2, 0, 3, 6, 0, 0, 0, 7],
    [8, 7, 3, 0, 2, 1, 4, 5, 0],
    [9, 4, 0, 5, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 9, 5, 0, 0, 4],
    [3, 9, 4, 8, 1, 0, 0, 7, 5],
    [0, 5, 1, 0, 6, 3, 0, 9, 8],
]


class AntColony:
    def __init__(self, num_of_ants, num_of_iterations, alpha, beta, evaporation_rate, initial_grid, dim):
        self.num_of_ants = num_of_ants
        self.num_of_iterations = num_of_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.initial_grid = initial_grid
        dimension = dim
        self.current_grid = Grid(dimension)
        self.grid_size = dim**2
        board_size = dim**2
        num_of_cells = board_size ** 2
        default_pheromone = 1 / num_of_cells
        self.pheromone_matrix = [[[default_pheromone for i in range(board_size)] for j in range(board_size)] for k
                                       in range(board_size)]


        # filling current sudoku grid
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.initial_grid[i][j] != 0:
                    #self.current_grid.sudoku[i][j].fixed = True
                    self.current_grid.set_cell(i, j, self.initial_grid[i][j])
                    # propagate constraints
                    self.current_grid.update_cell_values(i, j)

    def solve_sudoku(self):
            for i in range(num_of_ants):
                current_ant = self.ants[i]
                # TO DO: check including or not
                current_ant.row = random.randint(0, self.grid_size)
                current_ant.column = random.randint(0, self.grid_size)
            sudoku_solved = False
            num_of_cells = self.grid_size**2
            while not sudoku_solved:
                for i in range(num_of_cells):

                    for j in range(self.num_of_ants):
                        current_ant = self.ants[i]
                        current_ant.perform_move()
                self.ants.sort(key= lambda x: x.fitness)
                best_ant = self.ants[0]
                # global pheromone update
               # update_global_pheromones()
                # best value evaporation
                #evaporate_best_value()
        def update_global_pheromones():
            pass
        def evaporate_best_value():
            pass





num_of_ants = 6
num_of_iterations = 100
alpha = 1
beta = 1
dim=3
evaporation_rate = 0.01
ant_colony = AntColony(num_of_ants, num_of_iterations, alpha, beta, evaporation_rate, initial_grid, dim)
ant_colony.current_grid.print_grid()
print(ant_colony.current_grid.sudoku[0][1].set_values)
