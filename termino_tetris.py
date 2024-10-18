import curses # The main module needed for this game to work
import time # Time related functions for the smooth animation of the game
import random # To randomize the blocks in the game
import sys # Sytem handling
from typing import List, Tuple # For type hinting and debugging purposes

# Game Constants
BOARD_WIDTH, BOARD_HEIGHT = 10, 20 # The tetris board width and height
BLOCK_CHAR = "X" # This is the character that will make the block or the tetromino
BOARD_CHAR = "O" # This is the chacter that will make the board
LEVEL = 0.27 # Game lvl

# Shapes of the blocks
SHAPES = [
    [[1, 1, 1, 1]], # Straight-line block
    [[1, 1], # Squre block
     [1, 1]],
    [[1, 1, 1], # T-block
     [0, 1, 0]],
    [[1, 1, 0], # Z-block
     [0, 1, 1]],
    [[0, 1, 1], # S-block
     [1, 1, 0]],
    [[1, 0], # L-block
     [1, 0],
     [1, 1]],
    [[0, 1], # Reverse L-block
     [0, 1],
     [1, 1]],
]

def create_new_block(shapes: List[List[List[int]]]) -> Tuple[List[List[int]], int]:
    '''Generates a shape and color for the block RANDOMLY.
       --------------------------------------------------- 
       curses.COLOR_BLACK == 0
       curses.COLOR_BLUE == 1
       curses.COLOR_GREEN == 2
       curses.COLOR_CYAN == 3
       curses.COLOR_RED == 4
       curses.COLOR_MAGENTA == 5
       curses.COLOR_YELLOW == 6
       curses.COLOR_WHITE == 7
       '''
    # Retrurn a random shape and the color    
    return random.choice(shapes), random.randint(1, 6)

def draw_board(window: curses.window, board: List[List[Tuple[str, int | None]]]) -> None:
    '''
    Draws the board on the screen
    -----------------------------
    board[y][x][0] is the char
    board[y][x][1] is the color
    '''
    for y, row in enumerate(board):
        for x, (char, color) in enumerate(row):
            if char == BLOCK_CHAR and color is not None:
                window.addch(y, x, char, color)
            else:
                window.addch(y, x, char)

def draw_score(window: curses.window, score: int) -> None:
    '''Draws the score board for the game'''
    height, width = window.getmaxyx() # Get the height, width of the window
    scr_text = f"Score: {score}" # Create the score text
    window.addstr(height // 2, (width - len(scr_text)) // 2, scr_text) # Print the scr_text on the window

def draw_instruction(window: curses.window) -> None:
    '''Draws the instructions'''
    # All the instructions in a list of tuples
    instructions = [
        ('Move right:', 'RIGHT Arrow Key ->'),
        ('Move left:', 'LEFT Arrow Key <-'),
        ('Rotate block:', 'UP Arrow Key ^'),
        ('Drop block:', 'Space Bar |__|'),
        ('QUIT', 'Press q'),
    ]

    for i, (title, desc) in enumerate(instructions):
        # Each instruction should have a padding of 3 from each other
        window.addstr(i * 3, 0, title)
        window.addstr(i * 3 + 1, 0, desc) # Increase the y by 1 for the descripition
        # Add dashed horizontal line for asthetics
        if i < len(instructions) - 1:
            window.addstr(y=i * 3 + 2, x=0, str='-' * max(len(title), len(desc)))

def make_board_list(rows: int, cols: int, char: str) -> List[List[Tuple[str, None]]]:
    '''
    Makes the board data structure which is a 2D list
    -------------------------------------------------
    width = cols
    height = rows
    '''
    return [[(char, None) for _ in range(cols)] for _ in range(rows)]

def rotate_block(shape: List[List[int]]) -> List[List[int]]:
    '''Rotates the block counter-clockwise'''
    return [list(row) for row in zip(*shape)][::-1]

def draw_block(board: List[List[Tuple[str, int | None]]], block: List[List[int]], blocky: int, blockx: int, color: int) -> List[List[Tuple[str, int | None]]]:
    '''Draws the block on the board'''
    # Create a copy of the board
    new_board = [row[:] for row in board]
    # Iterate through the block
    for row, part in enumerate(block):
        for col, piece in enumerate(part):
            if piece == 1:
                new_board[blocky + row][blockx + col] = (BLOCK_CHAR, color)
    return new_board

def colliding(board: List[List[Tuple[str, int | None]]], block: List[List[int]], blocky: int, blockx: int) -> bool:
    '''Checks if there is any collision with other blocks'''
    for row, part in enumerate(block):
        for col, piece in enumerate(part):
            if piece == 1:
                board_y, board_x = blocky + row, blockx + col
                if (board_y >= BOARD_HEIGHT or board_x < 0 or board_x >= BOARD_WIDTH or
                    board[board_y][board_x][0] == BLOCK_CHAR):
                    return True
    return False

def drop_block(board: List[List[Tuple[str, int | None]]], block: List[List[int]], blocky: int, blockx: int, max_vertical: int) -> int:
    '''Drops the block when space bar is hit'''
    y = blocky
    while y <= max_vertical and not colliding(board, block, y, blockx):
        y += 1
    return y - 1

def score_and_clear(board: List[List[Tuple[str, int | None]]], score: int) -> Tuple[int, List[List[Tuple[str, int | None]]]]:
    '''Clear the rows that are full and updates the score'''
    # Create an empty row
    empty_row = [(BOARD_CHAR, None) for _ in range(BOARD_WIDTH)]
    # Create a new board with rows that are not filled yet
    new_board = [row for row in board if not all(item[0] == BLOCK_CHAR for item in row)]
    # The score is the difference between the original board height and new board height
    cleared_rows = BOARD_HEIGHT - len(new_board)
    # Update the board with cleared_rows numbered emtpy_rows and add the empty rows in the beginning
    new_board = [empty_row[:] for _ in range(cleared_rows)] + new_board
    return score + cleared_rows, new_board

def is_board_full(board: List[List[Tuple[str, int | None]]],
                  block: List[List[int]], blocky: int, blockx: int) -> bool:
    '''Checks if the board is full or not'''
    return any(item[0] == BLOCK_CHAR for item in board[0]) or colliding(board, block, blocky, blockx)

def main(stdscr):
    '''The preparatory part of the game'''
    curses.curs_set(False) # Make the cursor invisible
    stdscr.nodelay(True) # No delaying in checking for user inputs
    stdscr.clear() # Clear the main window

    # Get the height and width of the screen
    screen_height, screen_width = stdscr.getmaxyx()

    # Tetris board window measurements
    board_win_height, board_win_width = BOARD_HEIGHT + 1, BOARD_WIDTH + 1 # I don't know why giving (20, 10) doesn't work.
    board_win_y, board_win_x = (screen_height - board_win_height) // 2, (screen_width - board_win_width) // 2 # Starting y, x for board_win

    # Score board window measurements
    score_win_height, score_win_width = 2, board_win_width # Width same as board_win_width
    score_win_y, score_win_x = (board_win_y - score_win_height - 1), board_win_x

    # Instruction window measurements
    instr_win_height, instr_win_width = 15, 20
    instr_win_y, instr_win_x = board_win_y, (board_win_x + board_win_width + 5)

    # If the screen is smaller than the board, the program will simply not run
    if (board_win_width + instr_win_width + 5) > screen_width or (board_win_height + score_win_height + 1) > screen_height:
        sys.exit("\nPlease make the terminal full screen or just a bit bigger, buddy")

    # Create all the windows
    board_win = curses.newwin(board_win_height, board_win_width, board_win_y, board_win_x) # Create the board window
    score_brd_win = curses.newwin(score_win_height, score_win_width, score_win_y, score_win_x) # Create the score board window
    instr_win = curses.newwin(instr_win_height, instr_win_width, instr_win_y, instr_win_x) # Create the instruction window

    # Make sure there is no delay in every window
    for win in (board_win, score_brd_win, instr_win):
        win.nodelay(True)

    # Make the board data structure and the copy
    board_list = make_board_list(BOARD_HEIGHT, BOARD_WIDTH, BOARD_CHAR)
    # Score
    score = 0

    # Initialize every color
    for i in range(1, 7):
        curses.init_pair(i, i, curses.COLOR_BLACK)
    
    # Game state
    game_active = True
    while game_active:
        '''Block generating part of the game'''
        # Create the block and color
        block, block_color = create_new_block(SHAPES)
        y, x = 0, (BOARD_WIDTH - len(block[0])) // 2
        # The maximum horizontal and vertical for the block
        maximum_x = BOARD_WIDTH - len(block[0])
        maximum_y = BOARD_HEIGHT - len(block)

        while True:
            # If board is full then, game is voer
            if is_board_full(board_list, block, y, x):
                game_active = False
                score_brd_win.clear() # Clear the score board
                score_brd_win.refresh() # Refresh the score board
                instr_win.clear() # Clear the instruction window
                instr_win.refresh() # Refresh the instruction window
                break

            # Create a new temp_board every time through the loop for drawing the block
            temp_board = draw_block(board_list, block, y, x, curses.color_pair(block_color))

            # Clear the board window and draw the board
            board_win.clear()
            draw_board(board_win, temp_board)
            board_win.refresh()

            # Clear the score board window and draw the score board
            score_brd_win.clear()
            draw_score(score_brd_win, score)
            score_brd_win.refresh()

            # Clear the instruction window and draw the instructions
            instr_win.clear()
            draw_instruction(instr_win)
            instr_win.refresh()

            # Get all the keystrokes
            key = stdscr.getch()
            # Exit if 'q' pressed
            if key == ord('q') or key == ord('Q'):
                game_active = False
                score_brd_win.clear() # Clear the score board
                score_brd_win.refresh() # Refresh the score board
                instr_win.clear() # Clear the instruction window
                instr_win.refresh() # Refresh the instruction window
                break
            elif key == curses.KEY_RIGHT and x < maximum_x and not colliding(board_list, block, y, x + 1):
                x += 1
            elif key == curses.KEY_LEFT and x > 0 and not colliding(board_list, block, y, x - 1):
                x -= 1
            elif key == curses.KEY_UP:
                rotated = rotate_block(block)
                if x <= BOARD_WIDTH - len(rotated[0]) and not colliding(board_list, rotated, y, x):
                    block = rotated
                    maximum_x = BOARD_WIDTH - len(block[0])
                    maximum_y = BOARD_HEIGHT - len(block)
            elif key == ord(' '):
                y = drop_block(board_list, block, y, x, maximum_y)

            # Update the y pos
            y += 1

            if y > maximum_y or colliding(board_list, block, y, x):
                y -= 1
                board_list = draw_block(board_list, block, y, x, curses.color_pair(block_color))
                score, board_list = score_and_clear(board_list, score)
                break
            
            # Sleep for some time to make the game realisitic
            time.sleep(LEVEL)

    # Game over screen
    board_win.clear()
    board_win.addstr(board_win_height // 2, 0, 'GAME OVER!')
    board_win.refresh()
    time.sleep(1)
    board_win.clear()
    draw_score(board_win, score)
    board_win.refresh()
    time.sleep(0.5)

if __name__ == "__main__":
    curses.wrapper(main)
