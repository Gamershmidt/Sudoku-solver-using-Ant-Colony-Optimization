# Size of each single square in the Sudoku grid
SQUARE_SIZE = 3


def check_set_of_numbers(line):
    """
    Check if all numbers in a set are unique and from 1 to 9.

    Args:
        line (list): list of numbers.

    Returns:
        bool: True if all numbers in the list are unique and not equal to zero, False otherwise.
    """
    set_numbers = set(line)
    if len(set_numbers) != 9 or '0' in set_numbers:
        return False
    else:
        return True


def check_horizontal(grid, row):
    """
    Check if horizontal line in Sudoku puzzle is correct.

    Args:
        grid (list): 2D matrix of Sudoku puzzle with numbers.
        row (int): number of considering row.

    Returns:
        bool: True if all numbers in the row are unique and not equal to zero, False otherwise.
    """
    if check_set_of_numbers(grid[row]):
        return True
    return False


def check_vertical(grid, column):
    """
    Check if vertical line in Sudoku puzzle is correct.

    Args:
        grid (list): 2D matrix of Sudoku puzzle with numbers.
        column (int): number of considering column.

    Returns:
        bool: True if all numbers in the column are unique and not equal to zero, False otherwise.
    """
    column_values = []
    for i in range(9):
        column_values.append(grid[i][column])
    if check_set_of_numbers(column_values):
        return True
    return False


def check_square(grid, square_i, square_j):
    """
    Check if single square in Sudoku puzzle is correct.

    Args:
        grid (list): 2D matrix of Sudoku puzzle with numbers.
        square_i (int): position of considering square by horizontal line.
        square_j (int): position of considering square by vertical line.

    Returns:
        bool: True if all numbers in the square are unique and not equal to zero, False otherwise.
    """
    square_values = []
    for i in range(3):
        for j in range(3):
            square_values.append(grid[i + square_i * SQUARE_SIZE][j + square_j * SQUARE_SIZE])
    if check_set_of_numbers(square_values):
        return True
    return False
