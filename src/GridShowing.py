import sys
import time
import pygame
from CreatingCheckTable import create_check_table
import AntColony

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (230, 236, 51)
GREEN = (34, 139, 34)

# Size of each single square in the Sudoku grid
SQUARE_SIZE = 3

# Size of text
FONT_SIZE = 30

# Setting for button
BUTTON_COLOR = (34, 200, 34)
BUTTON_TEXT_COLOR = (0, 0, 0)

# Initialize pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 370, 460
WINDOW_SIZE = (WIDTH, HEIGHT)

# Set up the grid in the screen
CELL_SIZE = 40
GRID_SIZE = 9
GRID_WIDTH = CELL_SIZE * GRID_SIZE
GRID_HEIGHT = CELL_SIZE * GRID_SIZE
PADDING = 4


# Function to draw the grid
def draw_grid(screen):
    """
    Draw the grid lines on the screen.

    Args:
    screen (pygame.Surface): Surface to draw the grid on.
    """
    for i in range(GRID_SIZE+1):
        # A condition that helps to highlight squares of size SQUARE_SIZE
        if i % SQUARE_SIZE == 0:
            pygame.draw.line(screen, BLACK, (CELL_SIZE * i+PADDING, 0), (CELL_SIZE * i+PADDING, GRID_HEIGHT), 2)
            pygame.draw.line(screen, BLACK, (0+PADDING, CELL_SIZE * i), (GRID_WIDTH+PADDING, CELL_SIZE * i), 2)
        else:
            pygame.draw.line(screen, BLACK, (CELL_SIZE * i+PADDING, 0), (CELL_SIZE * i+PADDING, GRID_HEIGHT), 1)
            pygame.draw.line(screen, BLACK, (0+PADDING, CELL_SIZE * i), (GRID_WIDTH+PADDING, CELL_SIZE * i), 1)


def draw_numbers(grid, screen, user_input=True, input_grid=None):
    """
    Draw numbers (from 1 to 9) on the Sudoku grid.

    Args:
    grid (list): 2D matrix of Sudoku puzzle with numbers.
    screen (pygame.Surface): Surface to draw the numbers on.
    user_input (bool): Flag indicating whether the numbers are typed by user.
    input_grid (list): 2D list representing the initial input Sudoku grid.
    """
    font = pygame.font.Font(None, FONT_SIZE)

    # Create checking table for putting different colors to numbers
    table_for_color = create_check_table(grid)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if int(grid[i][j]) != 0:
                text_color = BLACK

                # If this is not user mode, then numbers will have different colors
                # to show how many conditions they fulfill
                if not user_input:
                    if int(input_grid[i][j]) == 0:
                        if table_for_color[i][j] == 3:
                            text_color = GREEN  # Color for numbers that fulfill all 3 conditions
                        elif table_for_color[i][j] == 2:
                            text_color = YELLOW  # Color for numbers that fulfill 2 conditions
                        elif table_for_color[i][j] == 1:
                            text_color = YELLOW  # Color for numbers that fulfill 1 condition
                        elif table_for_color[i][j] == 0:
                            text_color = RED  # Color for numbers that do not fulfill any conditions
                text = font.render(grid[i][j], True, text_color)
                text_pos = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2 + PADDING,
                                                 i * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_pos)


# Function to handle events
def handle_events(grid, stop_button_rect):
    """
    Handle pygame events.

    Args:
    grid (list): 2D matrix of Sudoku puzzle with numbers.
    stop_button_rect (pygame.Rect): Rectangle representing the stop button.

    Returns:
    bool: True if the event is to stop user interaction, False otherwise.
    """
    for event in pygame.event.get():

        # Quit event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # If it is mouse button down event, then get mouse position and
        # check if the mouse is clicked on the stop button
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if stop_button_rect.collidepoint(mouse_pos):
                return True

        # The condition for key down event
        # If key is backspace or return, then stop interaction.
        # If key is digit, then get mouse position in the grid, check conditions for Sudoku puzzle, and
        # write this number to specific cell in grid.
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
                start_x = (col // SQUARE_SIZE) * SQUARE_SIZE
                start_y = (row // SQUARE_SIZE) * SQUARE_SIZE
                for i in range(start_x, start_x + SQUARE_SIZE):
                    for j in range(start_y, start_y + SQUARE_SIZE):
                        if grid[i][j] == str(event.unicode):
                            check = False
                if check or str(event.unicode) == '0':
                    grid[col][row] = str(event.unicode)
    return False


def initialize_grid():
    """
    Initialize the Sudoku grid with zeros.

    Returns:
    list: 2D list representing the Sudoku grid.
    """
    grid = [["0" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    return grid


def create_stop_button(screen, text):
    """
    Create a stop button on the screen.

    Args:
    screen (pygame.Surface): Surface to draw the button on.
    text (str): Text to display on the button.

    Returns:
    pygame.Rect: Rectangle representing the button.
    """
    button_font = pygame.font.Font(None, FONT_SIZE)
    button_text = button_font.render(text, True, BUTTON_TEXT_COLOR)
    button_rect = button_text.get_rect(center=(WIDTH // 2, GRID_HEIGHT + (HEIGHT - WIDTH) // 2))
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    screen.blit(button_text, button_rect)
    return button_rect


# Main function
def main():
    """
    Main function to run the Sudoku solver GUI.

    This function initializes the pygame window, handles user input, displays the Sudoku grid,
    solves the puzzle using Ant Colony Optimization, displays the solved grids, and allows the user to exit.

    """
    # Initialize window for user interaction
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku Grid Input")
    clock = pygame.time.Clock()
    screen.fill(WHITE)

    # Initialize Sudoku grid with zeros
    initial_grid = initialize_grid()

    # Input phase: User fills in the Sudoku grid
    while True:
        screen.fill(WHITE)
        draw_grid(screen)
        stop_button_rect = create_stop_button(screen, "Confirm")
        draw_numbers(initial_grid, screen)

        # Handle user event
        if handle_events(initial_grid, stop_button_rect):
            break
        pygame.display.flip()
        clock.tick(30)

    # Write user initial grid to input file
    input_sudoku = ""
    for row in initial_grid:
        for elem in row:
            input_sudoku += elem
    input_file = open("input.txt", "w")
    input_file.write(input_sudoku)
    input_file.close()
    time.sleep(1)

    # Perform Ant Colony Optimization to solve user's Sudoku puzzle
    AntColony.solve_one_puzzle('input.txt')

    # Obtain solutions from output file
    grids = []
    with open("output.txt", 'r') as output_file:
        for line in output_file:
            temp = []
            for i in range(9):
                temp.append(line[i*9:(i+1)*9])
            grids.append(temp)
    grid_index = 0

    # Display solved grids one by one with a delay
    while True:
        screen.fill(WHITE)
        current_grid = grids[grid_index]
        draw_grid(screen)
        draw_numbers(current_grid, screen, user_input=False, input_grid=initial_grid)

        # Event handling for exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()

        # Increment grid index
        grid_index = (grid_index + 1)

        time.sleep(0.2)
        if grid_index == len(grids):
            break

    quit_point = False

    # Display final grid and exit button
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


# Call the main function
if __name__ == "__main__":
    main()

