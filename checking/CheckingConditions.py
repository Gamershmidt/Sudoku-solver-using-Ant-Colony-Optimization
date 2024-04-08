SQUARE_SIZE = 3


def check_line(line):
    set_numbers = set(line)
    if len(set_numbers) != 9 or '0' in set_numbers:
        return False
    else:
        return True


def check_horizontal(grid, row):
    if check_line(grid[row]):
        return True
    return False


def check_vertical(grid, column):
    column_values = []
    for i in range(9):
        column_values.append(grid[i][column])
    if check_line(column_values):
        return True
    return False


def check_square(grid, square_i, square_j):
    square_values = []
    for i in range(3):
        for j in range(3):
            square_values.append(grid[i + square_i * SQUARE_SIZE][j + square_j * SQUARE_SIZE])
    if check_line(square_values):
        return True
    return False