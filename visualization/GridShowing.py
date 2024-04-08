import sys
import time
import pygame
from CreatingCheckTable import create_check_table
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
SQUARE_SIZE = 3

# Initialize pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 540, 540
WINDOW_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Sudoku Visualizer")


# Function to draw the grid
def draw_grid():
    for i in range(9):
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (60 * i, 0), (60 * i, HEIGHT), 4)
            pygame.draw.line(screen, BLACK, (0, 60 * i), (WIDTH, 60 * i), 4)
        else:
            pygame.draw.line(screen, GRAY, (60 * i, 0), (60 * i, HEIGHT), 2)
            pygame.draw.line(screen, GRAY, (0, 60 * i), (WIDTH, 60 * i), 2)


def draw_numbers(grid):
    font = pygame.font.Font(None, 40)
    table_for_color = create_check_table(grid)
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                if table_for_color[i][j] == 3:
                    text_color = (34, 139, 34)
                elif table_for_color[i][j] == 2:
                    text_color = (50, 205, 50)
                elif table_for_color[i][j] == 1:
                    text_color = (0, 255, 0)
                else:
                    text_color = BLACK
                text = font.render(str(grid[i][j]), True, text_color)
                screen.blit(text, (j * 60 + 20, i * 60 + 15))


# Example to show how visualization will look like
grids = [
    [[2, 1, 3, 8, 7, 9, 4, 6, 5],
     [6, 5, 7, 3, 5, 1, 8, 8, 8],
     [4, 9, 8, 8, 6, 4, 9, 4, 2],
     [3, 5, 1, 9, 4, 1, 6, 6, 6],
     [5, 4, 4, 1, 8, 8, 4, 2, 9],
     [1, 3, 4, 2, 6, 6, 8, 6, 8],
     [8, 5, 2, 2, 6, 6, 1, 5, 6],
     [7, 4, 4, 6, 5, 1, 3, 2, 8],
     [9, 9, 3, 9, 3, 2, 7, 4, 9]],
    [[1, 8, 4, 7, 4, 1, 9, 9, 6],
     [3, 8, 9, 5, 7, 2, 6, 1, 4],
     [5, 6, 9, 3, 1, 5, 9, 8, 4],
     [9, 6, 8, 6, 1, 4, 9, 5, 3],
     [6, 5, 8, 5, 6, 5, 7, 4, 6],
     [3, 9, 7, 8, 1, 2, 5, 4, 6],
     [5, 2, 8, 4, 7, 4, 3, 9, 8],
     [1, 3, 4, 2, 5, 3, 4, 7, 6],
     [2, 8, 9, 3, 2, 8, 5, 4, 8]],
    [[6, 5, 9, 4, 2, 1, 1, 6, 1],
     [3, 5, 2, 7, 2, 5, 9, 3, 7],
     [2, 8, 5, 9, 1, 4, 6, 3, 7],
     [9, 1, 6, 6, 7, 9, 4, 9, 2],
     [8, 3, 7, 2, 4, 1, 8, 3, 4],
     [6, 8, 9, 2, 5, 1, 6, 7, 3],
     [6, 5, 2, 4, 3, 6, 9, 5, 6],
     [2, 7, 8, 6, 1, 5, 5, 5, 5],
     [2, 7, 9, 6, 4, 1, 9, 2, 2]],
    [[1, 9, 7, 2, 1, 4, 9, 5, 7],
     [7, 8, 7, 4, 5, 4, 7, 2, 1],
     [9, 9, 5, 2, 1, 4, 2, 2, 6],
     [7, 4, 9, 8, 9, 4, 6, 1, 2],
     [4, 9, 4, 5, 1, 3, 7, 7, 3],
     [6, 5, 5, 3, 1, 4, 8, 1, 5],
     [7, 1, 8, 5, 8, 8, 2, 8, 7],
     [9, 1, 9, 6, 6, 4, 9, 1, 6],
     [7, 1, 9, 6, 9, 5, 2, 3, 5]],
    [[3, 9, 3, 6, 6, 9, 5, 5, 1],
     [9, 4, 3, 9, 4, 2, 2, 8, 9],
     [4, 8, 6, 7, 8, 6, 1, 1, 1],
     [1, 8, 6, 4, 6, 3, 1, 5, 1],
     [5, 2, 6, 5, 7, 9, 7, 5, 3],
     [3, 1, 3, 8, 6, 8, 4, 9, 8],
     [5, 9, 1, 3, 4, 1, 9, 2, 2],
     [6, 3, 1, 4, 1, 7, 3, 5, 1],
     [6, 1, 1, 1, 8, 4, 8, 7, 1]]
]

# Main loop
grid_index = 0
while True:
    screen.fill(WHITE)
    current_grid = grids[grid_index]
    draw_grid()
    draw_numbers(current_grid)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()

    # Increment grid index
    grid_index = (grid_index + 1) % len(grids)

    # Pause for 1 second
    time.sleep(1)
