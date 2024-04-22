import sys
import time
import pygame
from CreatingCheckTable import create_check_table
import AntColony
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
SQUARE_SIZE = 3
CELL_SIZE = 40
GRID_SIZE = 9
GRID_WIDTH = CELL_SIZE * GRID_SIZE
GRID_HEIGHT = CELL_SIZE * GRID_SIZE
FONT_SIZE = 30
BUTTON_COLOR = (34, 200, 34)
BUTTON_TEXT_COLOR = (0, 0, 0)

# Initialize pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 370, 460
PADDING = 4
WINDOW_SIZE = (WIDTH, HEIGHT)
#screen = pygame.display.set_mode(WINDOW_SIZE)
#pygame.display.set_caption("Sudoku Visualizer")


# Function to draw the grid
def draw_grid(screen):
    for i in range(GRID_SIZE+1):
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (CELL_SIZE * i+PADDING, 0), (CELL_SIZE * i+PADDING, GRID_HEIGHT), 2)
            pygame.draw.line(screen, BLACK, (0+PADDING, CELL_SIZE * i), (GRID_WIDTH+PADDING, CELL_SIZE * i), 2)
        else:
            pygame.draw.line(screen, BLACK, (CELL_SIZE * i+PADDING, 0), (CELL_SIZE * i+PADDING, GRID_HEIGHT), 1)
            pygame.draw.line(screen, BLACK, (0+PADDING, CELL_SIZE * i), (GRID_WIDTH+PADDING, CELL_SIZE * i), 1)


def draw_numbers(grid, screen, user_input=True, input_grid=None):
    font = pygame.font.Font(None, 30)
    table_for_color = create_check_table(grid)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if int(grid[i][j]) != 0:
                text_color = BLACK
                if not user_input:
                    if int(input_grid[i][j]) == 0:
                        if table_for_color[i][j] == 3:
                            text_color = (34, 139, 34)
                        elif table_for_color[i][j] == 2:
                            text_color = (230, 236, 51)
                        elif table_for_color[i][j] == 1:
                            text_color = (230, 236, 51)
                        elif table_for_color[i][j] == 0:
                            text_color = (255, 0, 0)
                text = font.render(grid[i][j], True, text_color)
                text_pos = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2 + PADDING, i * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_pos)


# Function to handle events
def handle_events(grid, stop_button_rect):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if stop_button_rect.collidepoint(mouse_pos):
                return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return True
            elif event.key == pygame.K_BACKSPACE:
                return True
            elif event.unicode.isdigit():
                row, col = pygame.mouse.get_pos()
                row = row // CELL_SIZE
                col = col // CELL_SIZE
                check = True
                for i in range(GRID_SIZE):
                    if grid[i][row] == str(event.unicode):
                        check = False
                for i in range(GRID_SIZE):
                    if grid[col][i] == str(event.unicode):
                        check = False

                start_x = (col // 3) * 3
                start_y = (row // 3) * 3

                for i in range(start_x, start_x + 3):
                    for j in range(start_y, start_y + 3):
                        if grid[i][j] == str(event.unicode):
                            check = False
                if check or str(event.unicode) == '0':
                    grid[col][row] = str(event.unicode)
    return False


# Function to initialize the Sudoku grid
def initialize_grid():
    grid = [["0" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    return grid


# Function to create stop button
def create_stop_button(screen, text):
    button_font = pygame.font.Font(None, FONT_SIZE)
    button_text = button_font.render(text, True, BUTTON_TEXT_COLOR)
    button_rect = button_text.get_rect(center=(WIDTH // 2, GRID_HEIGHT + (HEIGHT - WIDTH) // 2))
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    screen.blit(button_text, button_rect)
    return button_rect


# Main function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku Grid Input")
    clock = pygame.time.Clock()

    screen.fill(WHITE)
    initial_grid = initialize_grid()

    while True:
        screen.fill(WHITE)
        draw_grid(screen)
        stop_button_rect = create_stop_button(screen, "Confirm")
        draw_numbers(initial_grid, screen)
        if handle_events(initial_grid, stop_button_rect):
            break
        pygame.display.flip()
        clock.tick(30)


    #pygame.quit()
    input_sudoku = ""
    for row in initial_grid:
        for elem in row:
            input_sudoku += elem
    input_file = open("input.txt", "w")
    input_file.write(input_sudoku)
    input_file.close()
    time.sleep(1)

    AntColony.solve_one_puzzle('input.txt')
    grids = []
    with open("output.txt", 'r') as output_file:
        for line in output_file:
            temp = []
            for i in range(9):
                temp.append(line[i*9:(i+1)*9])
            grids.append(temp)

    grid_index = 0
    while True:
        screen.fill(WHITE)
        current_grid = grids[grid_index]
        draw_grid(screen)
        draw_numbers(current_grid, screen, user_input=False, input_grid=initial_grid)
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

        # Increment grid index
        grid_index = (grid_index + 1)

        # Pause for 1 second
        time.sleep(0.2)
        if grid_index == len(grids):
            break

    quit_point = False
    while True:
        screen.fill(WHITE)
        draw_grid(screen)
        stop_button_rect = create_stop_button(screen, "Exit")
        draw_numbers(grids[-1], screen, user_input=False, input_grid=initial_grid)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if stop_button_rect.collidepoint(mouse_pos):
                    quit_point = True
                    break
        if quit_point:
            pygame.quit()
            sys.exit()
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()

# 050083017
# 000100400
# 304005608
# 000030009
# 090824500
# 006000070
# 009000050
# 007290086
# 103607204


# 001520040
# 600100009
# 040800070
# 090000001
# 008000400
# 400000090
# 070009080
# 500008004
# 010052600

