import copy
import random

from src.SudokuGrid import Grid
from src.Ant import Ant


def load_dataset(filename, num_of_lines = 1000):
    """
    Load Sudoku puzzles dataset from a given CSV file.

    Args:
        filename (str): The filename of the CSV file (contains Sudoku puzzles and solutions).

    Returns:
        numpy.ndarray, numpy.ndarray: Arrays containing Sudoku puzzles and their corresponding solutions.
    """
    import numpy as np

    tasks = np.zeros((num_of_lines, 81), np.int32)
    solutions = np.zeros((num_of_lines, 81), np.int32)
    with open(filename, 'r') as file:
        # ignore the first line
        next(file)
        for i, line in enumerate(file):
            if i >= num_of_lines:
                break
            quiz, solution = line.strip().split(",")
            for j, q_s in enumerate(zip(quiz, solution)):
                q, s = q_s
                tasks[i][j] = int(q)
                solutions[i][j] = int(s)
    return tasks, solutions

def load_one_task(filename):
    """
    Load a single Sudoku puzzle from a given file.

    Args:
        filename (str): The filename of the file containing the Sudoku puzzle.

    Returns:
        str: A single Sudoku puzzle as a string.
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
    Solve a single Sudoku puzzle from a given file and print the solution.

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
    ant_colony = AntColony(num_of_ants, local_evaporation_rate, global_evaporation_rate, initial_grid, dim, delta_tau_best_evaporation)
    found = ant_colony.solve_sudoku()
    if found is not None:
        print('Solved')
        found.print_grid()

    else:
        print('No solution found')

def solve_all_puzzles(num_of_puzzles, filename):
    """
    Function for testing the algorithm.
    Solve given number of Sudoku puzzles from the specified file
    and write the results to an output file.

    Args:
        num_of_puzzles (int): The number of Sudoku puzzles to solve.
        filename (str): The filename of the file containing Sudoku puzzles and solutions.
    """
    quizzes, solutions = load_dataset(filename)
    results_filename = "test_results.txt"
    with open(results_filename, "w") as file:
        for i in range(num_of_puzzles):
            file.write(f"Test #{i}\n")
            # prepare data
            input_line = "".join([str(x) for x in quizzes[i]])
            solution_line = "".join([str(x) for x in solutions[i]])
            file.write(f"Given puzzle: {input_line}, given correct solution: {solution_line}\n")
    
            initial_grid = create_matrix(input_line)
            ant_colony = AntColony(num_of_ants, local_evaporation_rate, global_evaporation_rate, initial_grid, dim, delta_tau_best_evaporation)
            found = ant_colony.solve_sudoku()
            
            if found is not None:
                solution = create_array(found)
                solved = True
                for j in range(81):
                    if solution[j] != solutions[i][j]:
                        file.write(f"Test {i} failed, incorrect found solution: {create_line(found)}\n\n")
                        solved = False
                        break
                if solved:
                    file.write(f"Test {i} passed, solution: {create_line(found)}\n")
            else:
                file.write(f"No solution found on test{i}\n")


class AntColony:
    """
    Class representing an Ant Colony for solving Sudoku puzzles.

    Attributes:
        num_of_ants (int): The number of ants in the colony.
        local_evaporation_rate (float): The local pheromone evaporation rate.
        global_evaporation_rate (float): The global pheromone evaporation.
        initial_grid (Grid): The initial Sudoku grid.
        current_grid (Grid): The current Sudoku grid being processed.
        grid_size (int): The size of the Sudoku grid.
        num_of_cells (int): The number of cells in the Sudoku grid.
        default_pheromone (float): The default pheromone value for each possible value.
        pheromone_matrix (list): Matrix representing pheromone levels on each cell for each possible value.
        ants (list): List of all ants in the colony.
        delta_tau_best (float): Delta tau value for the best solution found.
        best_ant (Ant): The ant with the best solution.
        found_grids_file (file): File to store found grids while finding the solution.
    """
    def __init__(self, num_of_ants, local_evaporation_rate, global_evaporation_rate,
                 initial_grid, dimension, delta_tau_best_evaporation):
        """
        Initialize an AntColony instance.

        Args:
            num_of_ants (int): The number of ants in the colony.
            local_evaporation_rate (float): The local pheromone evaporation rate.
            global_evaporation_rate (float): The global pheromone evaporation rate.
            initial_grid (2D array): The initial Sudoku grid.
            dimension (int): The dimension of the Sudoku grid (e.g., 3 for a 9x9 grid).
        """
        self.num_of_ants = num_of_ants
        self.local_evaporation_rate = local_evaporation_rate
        self.global_evaporation_rate = global_evaporation_rate
        self.delta_tau_best_evaporation = delta_tau_best_evaporation

        self.initial_grid = initial_grid
        self.current_grid = Grid(dimension)
        self.grid_size = dimension ** 2
        self.num_of_cells = self.grid_size ** 2
        self.default_pheromone = 1 / self.num_of_cells
        # fill pheromone matrix with default values
        self.pheromone_matrix = [
            [[self.default_pheromone for i in range(self.grid_size)] for j in range(self.grid_size)] for k
            in range(self.grid_size)]
        self.ants = [Ant() for i in range(num_of_ants)]
        self.default_pheromone = 1 / self.num_of_cells
        self.delta_tau_best = 0
        self.best_ant = None
        fixed_num = 0
        # filename for the file to store intermediate grids for visualization
        output_file_name = "../data/output.txt"

        self.found_grids_file = open(output_file_name, "w")
        # filling current sudoku grid
        for i in range(self.grid_size):
            for j in range(self.grid_size):

                cur_value = self.initial_grid[i][j]
                self.current_grid.set_cell(i, j, cur_value)
                if (self.initial_grid[i][j] != 0):
                    fixed_num += 1

                    # propagate constraints
                    self.current_grid.propagate(i, j, self.ants[0])
        self.solved_grid = copy.deepcopy(self.current_grid)


    def solve_sudoku(self):
        """
        Function that implements the Ant Colony Optimization algorithm to solve Sudoku puzzles.

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


            num_of_iterations += 1

            for i in range(self.num_of_cells):
                for j in range(self.num_of_ants):
                    current_ant = self.ants[j]
                    current_ant.perform_move()

            # number of fixed cells of the best ant's grid
            num_of_fixed = 0

            # find the best ant on the current iteration
            self.best_ant = None
            for ant in self.ants:
                if ant.get_f() > num_of_fixed:
                    num_of_fixed = ant.get_f()
                    self.best_ant = ant
                    self.solved_grid = self.best_ant.grid

                # all cells are fixed, the solution is found
                if num_of_fixed == self.num_of_cells:


                    self.found_grids_file.write(create_line(self.solved_grid))
                    self.found_grids_file.write("\n")
                    return self.best_ant.grid

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
                    cur_cell = self.solved_grid.sudoku[i][j]
                    if not cur_cell.is_cell_incorrect():
                        self.pheromone_matrix[i][j][cur_cell.value - 1] = (
                                (1 - self.global_evaporation_rate) * self.pheromone_matrix[i][j][cur_cell.value - 1] +
                                self.global_evaporation_rate * self.delta_tau_best)
            # evaporation of delta_tau_best to avoid getting stuck in a local optimum
            self.delta_tau_best = self.delta_tau_best * self.delta_tau_best_evaporation


num_of_ants = 20
dim = 3
local_evaporation_rate = 0.1
global_evaporation_rate = 0.9
delta_tau_best_evaporation = 0.995

solve_one_puzzle('../data/one_sudoku.csv')
#solve_all_puzzles(1000, 'sudoku_big.csv')
