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
BUTTON_COLOR = (255, 0, 0)
BUTTON_TEXT_COLOR = (0, 0, 0)

# Initialize pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 370, 590
WINDOW_SIZE = (WIDTH, HEIGHT)
#screen = pygame.display.set_mode(WINDOW_SIZE)
#pygame.display.set_caption("Sudoku Visualizer")


# Function to draw the grid
def draw_grid(screen):
    for i in range(GRID_SIZE+1):
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (CELL_SIZE * i, 0), (CELL_SIZE * i, GRID_HEIGHT), 2)
            pygame.draw.line(screen, BLACK, (0, CELL_SIZE * i), (GRID_WIDTH, CELL_SIZE * i), 2)
        else:
            pygame.draw.line(screen, BLACK, (CELL_SIZE * i, 0), (CELL_SIZE * i, GRID_HEIGHT), 1)
            pygame.draw.line(screen, BLACK, (0, CELL_SIZE * i), (GRID_WIDTH, CELL_SIZE * i), 1)


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
                text_pos = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
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
                grid[col][row] = str(event.unicode)
    return False


# Function to initialize the Sudoku grid
def initialize_grid():
    grid = [["0" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    return grid


# Function to create stop button
def create_stop_button(screen):
    button_font = pygame.font.Font(None, FONT_SIZE)
    button_text = button_font.render("Stop", True, BUTTON_TEXT_COLOR)
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
    stop_button_rect = create_stop_button(screen)

    while True:
        draw_grid(screen)
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
    time.sleep(2)
    # 001520040600100009040800070090000001008000400400000090070009080500008004010052600
    # 001520040600100009040800070090000001008000400400000090070009080500008004010052600

    AntColony.solve_one_puzzle('input.txt')
    grids = []
    with open("output.txt", 'r') as output_file:
        for line in output_file:
            temp = []
            for i in range(9):
                temp.append(line[i*9:(i+1)*9])
            grids.append(temp)
                #grids[-1].append(list(line)[:81][i: i + 9])

    #print("Sudoku grid:", input_sudoku)
    # grids = [
    #     [[2, 1, 3, 8, 7, 9, 4, 6, 5],
    #      [6, 5, 7, 3, 5, 1, 8, 8, 8],
    #      [4, 9, 8, 8, 6, 4, 9, 4, 2],
    #      [3, 5, 1, 9, 4, 1, 6, 6, 6],
    #      [5, 4, 4, 1, 8, 8, 4, 2, 9],
    #      [1, 3, 4, 2, 6, 6, 8, 6, 8],
    #      [8, 5, 2, 2, 6, 6, 1, 5, 6],
    #      [7, 4, 4, 6, 5, 1, 3, 2, 8],
    #      [9, 9, 3, 9, 3, 2, 7, 4, 9]],
    #     [[1, 8, 4, 7, 4, 1, 9, 9, 6],
    #      [3, 8, 9, 5, 7, 2, 6, 1, 4],
    #      [5, 6, 9, 3, 1, 5, 9, 8, 4],
    #      [9, 6, 8, 6, 1, 4, 9, 5, 3],
    #      [6, 5, 8, 5, 6, 5, 7, 4, 6],
    #      [3, 9, 7, 8, 1, 2, 5, 4, 6],
    #      [5, 2, 8, 4, 7, 4, 3, 9, 8],
    #      [1, 3, 4, 2, 5, 3, 4, 7, 6],
    #      [2, 8, 9, 3, 2, 8, 5, 4, 8]],
    #     [[6, 5, 9, 4, 2, 1, 1, 6, 1],
    #      [3, 5, 2, 7, 2, 5, 9, 3, 7],
    #      [2, 8, 5, 9, 1, 4, 6, 3, 7],
    #      [9, 1, 6, 6, 7, 9, 4, 9, 2],
    #      [8, 3, 7, 2, 4, 1, 8, 3, 4],
    #      [6, 8, 9, 2, 5, 1, 6, 7, 3],
    #      [6, 5, 2, 4, 3, 6, 9, 5, 6],
    #      [2, 7, 8, 6, 1, 5, 5, 5, 5],
    #      [2, 7, 9, 6, 4, 1, 9, 2, 2]],
    #     [[1, 9, 7, 2, 1, 4, 9, 5, 7],
    #      [7, 8, 7, 4, 5, 4, 7, 2, 1],
    #      [9, 9, 5, 2, 1, 4, 2, 2, 6],
    #      [7, 4, 9, 8, 9, 4, 6, 1, 2],
    #      [4, 9, 4, 5, 1, 3, 7, 7, 3],
    #      [6, 5, 5, 3, 1, 4, 8, 1, 5],
    #      [7, 1, 8, 5, 8, 8, 2, 8, 7],
    #      [9, 1, 9, 6, 6, 4, 9, 1, 6],
    #      [7, 1, 9, 6, 9, 5, 2, 3, 5]],
    #     [[3, 9, 3, 6, 6, 9, 5, 5, 1],
    #      [9, 4, 3, 9, 4, 2, 2, 8, 9],
    #      [4, 8, 6, 7, 8, 6, 1, 1, 1],
    #      [1, 8, 6, 4, 6, 3, 1, 5, 1],
    #      [5, 2, 6, 5, 7, 9, 7, 5, 3],
    #      [3, 1, 3, 8, 6, 8, 4, 9, 8],
    #      [5, 9, 1, 3, 4, 1, 9, 2, 2],
    #      [6, 3, 1, 4, 1, 7, 3, 5, 1],
    #      [6, 1, 1, 1, 8, 4, 8, 7, 1]]
    # ]
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
        time.sleep(0.5)
        if grid_index == len(grids):
            break
    pygame.quit()


if __name__ == "__main__":
    main()

