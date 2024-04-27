# Importing module for checking conditions
import CheckingConditions as Check


def create_check_table(grid):
    """
    Create a check table based on the given Sudoku grid.

    Args:
    grid (list): 2D matrix of Sudoku puzzle with numbers.

    Returns:
    list: 2D list representing the check table, where each cell represents
    how many conditions are met by the number at this position.
    """
    check_table = [[0] * 9 for _ in range(9)]

    # Horizontal checkingGrid
    for i in range(9):
        if Check.check_horizontal(grid, i):
            for j in range(9):
                check_table[i][j] += 1

    # Vertical checkingGrid
    for j in range(9):
        if Check.check_horizontal(grid, j):
            for i in range(9):
                check_table[i][j] += 1

    # Square checkingGrid
    for i in range(3):
        for j in range(3):
            if Check.check_square(grid, i, j):
                for k in range(9):
                    check_table[k // 3 + i * Check.SQUARE_SIZE][k % 3 + j * Check.SQUARE_SIZE] += 1
    return check_table
