def check_line(line):
    set_numbers = set(line)
    if len(set_numbers) != 9 or '0' in set_numbers:
        return False
    else:
        return True
def checker(sudoku_solution):
    squares = True
    for i in range(0, 55, 27):
        sq1 = sudoku_solution[i: i + 9][0:3] + sudoku_solution[i+9: i + 18][0:3] + sudoku_solution[i+18: i + 27][0:3]
        sq2 = sudoku_solution[i: i + 9][3:6] + sudoku_solution[i + 9: i + 18][3:6] + sudoku_solution[i + 18: i + 27][3:6]
        sq3 = sudoku_solution[i: i + 9][6:9] + sudoku_solution[i + 9: i + 18][6:9] + sudoku_solution[i + 18: i + 27][6:9]
        squares = squares and check_line(sq1) and check_line(sq2) and check_line(sq3)
    for i in range(0, 73, 9):
        transponed_sudoku = ''
        for j in range(9):
            transponed_sudoku += sudoku_solution[j * 9 + i // 9]
        return check_line(sudoku_solution[i: i + 9]) and check_line(transponed_sudoku) and squares

