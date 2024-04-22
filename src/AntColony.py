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

# initial_grid = [[5,2,3,6,0,8,0,0,4],
# [4,6,0,9,0,0,0,2,0],
# [9,0,8,0,0,0,0,0,0],
# [8,1,0,0,0,4,0,0,9],
# [0,0,0,0,0,5,4,0,7],
# [6,0,0,8,3,0,2,0,5],
# [0,0,0,0,7,3,0,4,6],
# [0,3,0,0,0,0,9,0,0],
# [2,0,0,5,9,6,1,0,3]
# ]

# initial_grid = [
# [0,0,1,5,2,0,0,4,0],
# [6,0,0,1,0,0,0,0,9],
# [0,4,0,8,0,0,0,7,0],
# [0,9,0,0,0,0,0,0,1],
# [0,0,8,0,0,0,4,0,0],
# [4,0,0,0,0,0,0,9,0],
# [0,7,0,0,0,9,0,8,0],
# [5,0,0,0,0,8,0,0,4],
# [0,1,0,0,5,2,6,0,0]
# ]

def load_dataset(filename):
    """
    Load Sudoku puzzles dataset from a CSV file.

    Args:
        filename (str): The filename of the CSV file containing Sudoku puzzles and solutions.

    Returns:
        numpy.ndarray, numpy.ndarray: Arrays containing Sudoku puzzles and their corresponding solutions.
    """
    import numpy as np
    quizzes = np.zeros((1000000, 81), np.int32)
    solutions = np.zeros((1000000, 81), np.int32)
    for i, line in enumerate(open(filename, 'r').read().splitlines()[1:]):
        quiz, solution = line.split(",")
        for j, q_s in enumerate(zip(quiz, solution)):
            q, s = q_s
            quizzes[i, j] = q
            solutions[i, j] = s
    return quizzes, solutions

def load_one_task(filename):
    """
    Load a single Sudoku puzzle from a file.

    Args:
        filename (str): The filename of the file containing the Sudoku puzzle.

    Returns:
        str: A single Sudoku puzzle encoded as a string.
    """
    file = open(filename, 'r')
    task_line = file.readline()
    print(list(task_line))
    return task_line


def create_matrix(input_string):
    """
    Create a Sudoku grid matrix from an input string.

    Args:
        input_string (str): The input string representing the Sudoku puzzle.

    Returns:
        list: A 2D list representing the Sudoku grid.
    """
    rows = []
    for i in range(9):
        row = [int(input_string[j]) for j in range(i * 9, (i + 1) * 9)]
        rows.append(row)
    return rows


def create_array(matrix: Grid):
    """
    Convert a Sudoku grid matrix to a 1D array.

    Args:
        matrix (Grid): The Sudoku grid.

    Returns:
        list: A 1D list representing the Sudoku grid.
    """
    array = []
    for row in matrix.sudoku:
        for val in row:
            array.append(val.value)
    return array


def create_line(matrix: Grid):
    """
    Convert a Sudoku grid matrix to a string.

    Args:
        matrix (Grid): The Sudoku grid.

    Returns:
        str: A string representation of the Sudoku grid.
    """
    line = ""
    for row in matrix.sudoku:
        for val in row:
            line += str(val.value)
    return line


def solve_one_puzzle(filename):
    """
    Solve a single Sudoku puzzle and print the solution.

    Args:
        filename (str): The filename of the file containing the Sudoku puzzle.
    """
    input_puzzle_line = load_one_task(filename)
    initial_grid = create_matrix(input_puzzle_line)
    # print task
    print('Task')
    for row in initial_grid:
        for val in row:
            print(val, end=' ')
        print()
    ant_colony = AntColony(num_of_ants, local_evaporation_rate, global_evaporation_rate, initial_grid, dim)
    found = ant_colony.solve_sudoku()
    if found is not None:
        # solution = create_array(found)
        print('Solved')
        found.print_grid()
        #output_file.write(create_line(found))

    else:
        print('No solution found')

def solve_all_puzzles(num_of_puzzles, filename, output_filename):
    """
    Solve multiple Sudoku puzzles and write the results to an output file.

    Args:
        num_of_puzzles (int): The number of Sudoku puzzles to solve.
        filename (str): The filename of the file containing Sudoku puzzles and solutions.
        output_filename (str): The filename of the output file to write the results to.
    """
    quizzes, solutions = load_dataset(filename)
    # for i in range(10000):
    #     input_line = "".join([str(x) for x in quizzes[i]])
    #     solve_one_puzzle(input_line)
    with open("output.txt", "w") as file:
        for i in range(num_of_puzzles):
            file.write(f"Test {i}\n")
            input_line = "".join([str(x) for x in quizzes[i]])
            solution_line = "".join([str(x) for x in solutions[i]])
            file.write(f"Input task: {input_line}, solution: {solution_line}\n")
            initial_grid = create_matrix(input_line)
            ant_colony = AntColony(num_of_ants, local_evaporation_rate, global_evaporation_rate, initial_grid, dim, output_filename)
            found = ant_colony.solve_sudoku()
            if found is not None:
                solution = create_array(found)
                solved = True
                for j in range(81):
                    if solution[j] != solutions[i][j]:
                        file.write(f"Test {i} failed\n")
                        file.write(f"Incorrect solution: {create_line(found)}\n")
                        solved = False
                        break
                if solved:
                    file.write(f"Test {i} passed\n")
                    file.write(f"Solution: {create_line(found)}\n")
            else:
                file.write(f"No solution found on test{i}\n")


class AntColony:
    '''
    Class representing an Ant Colony Optimization (ACO) algorithm for solving Sudoku puzzles.

    Attributes:
        num_of_ants (int): The number of ants in the colony.
        local_evaporation_rate (float): The rate of local pheromone evaporation.
        global_evaporation_rate (float): The rate of global pheromone evaporation.
        initial_grid (Grid): The initial Sudoku grid.
        current_grid (Grid): The current Sudoku grid being processed.
        grid_size (int): The size of the Sudoku grid.
        num_of_cells (int): The number of cells in the Sudoku grid.
        default_pheromone (float): The default pheromone level on each cell.
        pheromone_matrix (list): Matrix representing pheromone levels on each cell.
        ants (list): List of ants in the colony.
        delta_tau_best (float): Delta tau value for the best solution found.
        best_ant (Ant): The ant with the best solution.
        found_grids_file (file): File to store found grids during solving.
    '''
    def __init__(self, num_of_ants, local_evaporation_rate, global_evaporation_rate,
                 initial_grid, dimension):
        '''
        Initialize an AntColony instance.

        Args:
            num_of_ants (int): The number of ants in the colony.
            local_evaporation_rate (float): The rate of local pheromone evaporation.
            global_evaporation_rate (float): The rate of global pheromone evaporation.
            initial_grid (Grid): The initial Sudoku grid.
            dimension (int): The dimension of the Sudoku grid (e.g., 3 for a 9x9 grid).
        '''
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
        output_file_name = "output.txt"
        #self.output_file_name = open(output_file_name, "w")
        self.found_grids_file = open(output_file_name, "w")
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
                    self.current_grid.propagate(i, j, self.ants[0])
                    # self.current_grid.update_cell_values(i, j)
        self.solved_grid = copy.deepcopy(self.current_grid)
        #print("num of fixed ")

    def solve_sudoku(self):
        """
        Solve the Sudoku puzzle using Ant Colony Optimization.

        Returns:
            Grid: The solved Sudoku grid.
        """
        sudoku_solved = False
        num_of_iterations = 0
        while not sudoku_solved and num_of_iterations < 10000:
            self.ants = [Ant(grid=copy.deepcopy(self.current_grid),
                             pheromone_matrix=self.pheromone_matrix,
                             row=random.randint(0, self.grid_size - 1),
                             column=random.randint(0, self.grid_size - 1),
                             default_pheromone=self.default_pheromone,
                             local_evaporation_rate=self.local_evaporation_rate,
                             ) for i in range(self.num_of_ants)]

            #self.solved_grid.print_grid()
            num_of_iterations += 1

            #print(num_of_iterations, self.delta_tau_best)

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
                #print(ant.num_of_fixed, ant.num_of_incorrect, ant.get_f())
                if ant.get_f() > num_of_fixed:
                    num_of_fixed = ant.get_f()
                    self.best_ant = ant
                    self.solved_grid = self.best_ant.grid
                if num_of_fixed == self.num_of_cells:

                    # print('Solved!!!!!', num_of_fixed, self.best_ant.num_of_incorrect, self.best_ant.num_of_fixed)
                    #self.best_ant.grid.print_grid()
                    self.found_grids_file.write(create_line(self.solved_grid))
                    self.found_grids_file.write("\n")
                    print(num_of_iterations)
                    return self.best_ant.grid
                    # exit()
            self.found_grids_file.write(create_line(self.solved_grid))
            self.found_grids_file.write("\n")
            print(num_of_iterations, num_of_fixed)
            # calculate delta_tau
            delta_tau = self.num_of_cells / (self.num_of_cells - self.best_ant.get_f())
            if delta_tau > self.delta_tau_best:
                self.delta_tau_best = delta_tau

            # global pheromone update
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    #cur_cell = self.best_ant.grid.sudoku[i][j]
                    cur_cell = self.solved_grid.sudoku[i][j]
                    if not cur_cell.is_cell_incorrect():
                        self.pheromone_matrix[i][j][cur_cell.value - 1] = (
                                (1 - self.global_evaporation_rate) * self.pheromone_matrix[i][j][cur_cell.value - 1] +
                                self.global_evaporation_rate * self.delta_tau_best)

            self.delta_tau_best = self.delta_tau_best * self.delta_tau_best_evaporation


num_of_ants = 20
dim = 3
local_evaporation_rate = 0.1
global_evaporation_rate = 0.9

solve_one_puzzle('one_sudoku.csv')
#solve_all_puzzles(10000, 'sudoku_big.csv')
