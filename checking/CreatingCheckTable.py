import checking.CheckingConditions as Check


def create_check_table(grid):
    check_table = [[0] * 9 for _ in range(9)]

    # Horizontal checking
    for i in range(9):
        if Check.check_horizontal(grid, i):
            for j in range(9):
                check_table[i][j] += 1

    # Vertical checking
    for j in range(9):
        if Check.check_horizontal(grid, j):
            for i in range(9):
                check_table[i][j] += 1

    # Square checking
    for i in range(3):
        for j in range(3):
            if Check.check_square(grid, i, j):
                for k in range(9):
                    check_table[k // 3 + i * Check.SQUARE_SIZE][k % 3 + j * Check.SQUARE_SIZE] += 1
    return check_table
