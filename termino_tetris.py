'''
A game to play tetris in the terminal/console.

**For playing in windows**
pip install windows-curses

Playing instruction:
(For simplicity, the arrow keys are used. W, A, S, D will not work)

    Right arrow key ->
    for going right

    Left arrow key <-
    for going left

    Up arrow key ^ (not the carret char)
    for rotating the block

    Space bar |__|
    for droping the block
'''
import curses # The main module needed for this game to work
import time # Time related functions for the smooth animation of the game
import random # To randomize the blocks in the game
import sys # Sytem handling
import copy # To copy the 2d list effectively

# Game Constants
BOARD_WIDTH, BOARD_HEIGHT = (10, 20) # The tetris board width and height
BLOCK_CHAR = "X" # This is the character that will make the block or the tetromino
BOARD_CHAR = "O" # This is the chacter that will make the board

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

# Game level
LEVEL = 0.27

def create_new_block(shapes):
    '''Generates a shape and color for the block RANDOMLY'''
    # Initialize the colors. 0 is reserved for black and white color pair
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    # Retrurn a random shape and the color
    return random.choice(shapes), curses.color_pair(random.randint(1, 6))

def draw_board(window, board):
    '''
    Draws the board on the screen
    -----------------------------
    board[y][x][0] is the char
    board[y][x][1] is the color
    '''
    for y in range(BOARD_HEIGHT): # Go through every row of the board
        for x in range(BOARD_WIDTH): # Go through every column of the row
            if board[y][x][0] == BOARD_CHAR:
                window.addstr(y, x, BOARD_CHAR) # If it is not a block char, then no color
            elif board[y][x][0] == BLOCK_CHAR:
                window.addstr(y, x, BLOCK_CHAR, board[y][x][1]) # If it is a block char, then there will be color

def draw_score(window, score):
    '''Draws the score board for the game'''
    height, width = window.getmaxyx() # Get the height, width of the window
    scr_text = f"Score: {score}" # Create the score text
    y, x = (height // 2), (width // 2 - len(scr_text) // 2) # Calculate the y, x for the scr_text to go on the window
    window.addstr(y, x, scr_text) # Print the scr_text on the window

def draw_instruction(window):
    '''Draws the instructions'''
    window.addstr(0, 0, 'Move right:')
    window.addstr(1, 0, 'RIGHT Arrow Key ->')
    window.addstr(2, 0, '------------------')
    window.addstr(3, 0, 'Move left:')
    window.addstr(4, 0, 'LEFT Arrow Key <-')
    window.addstr(5, 0, '------------------')
    window.addstr(6, 0, 'Rotate block:')
    window.addstr(7, 0, 'UP Arrow Key ^')
    window.addstr(8, 0, '---------------')
    window.addstr(9, 0, 'Drop block:')
    window.addstr(10, 0, 'Space Bar |__|')
    window.addstr(11, 0, '--------------')
    window.addstr(12, 0, 'QUIT')
    window.addstr(13, 0, 'Press q')
    window.addstr(14, 0, '-------')

def make_board_list(rows, cols, char):
    '''
    Makes the board data structure which is a 2D list
    -------------------------------------------------
    width = cols
    height = rows
    '''
    board_data_list = []
    # Create the board data structure
    for _ in range(rows):
        board_data_list.append([(char, None)] * cols) # (char, None); None is replacent for the color
    return board_data_list

def rotate_block(shape):
    '''Rotates the block counter-clockwise'''
    width, height = len(shape[0]), len(shape) # Get the height, width of the original block
    # In one rotation the height will be the width and the width will be the height
    new_block = [[None] * height for _ in range(width)] # Create a new block whose height will be width of the original block and vice versa
    for col in range(width):
        for row in range(height - 1, -1, -1): # Iterate from the last row of the original block
            new_block[width - col - 1][row] = shape[row][col]
    return new_block

def draw_block(board, block, blocky, blockx, color):
    '''Puts the block in the board data structure'''
    # Update the landed blocks on the board
    for row, part in enumerate(block):
        for col, piece in enumerate(part):
            if piece == 1:
                board[blocky + row][blockx + col] = (BLOCK_CHAR, color)
            elif piece == 0: # No need to put that on the board
                continue
    return board

def colliding(board, block, blocky, blockx):
    '''Checks if the block is colliding with another block'''
    for row, part in enumerate(block):
        for col, piece in enumerate(part):
            if piece == 1:
                if board[blocky + row][blockx + col][0] == BOARD_CHAR:
                    continue
                elif board[blocky + row][blockx + col][0] == BLOCK_CHAR:
                    # If there is a block char then there is a collision
                    return True
            elif piece == 0:
                continue
    # If no collision is found, return False
    return False

def drop_block(board, block, blocky, blockx, max_vertical):
    y = blocky
    while not colliding(board, block, y, blockx):
        y += 1
        if y > max_vertical:
            y = max_vertical
            break
    return y

def score_and_clear(board, score):
    '''Clears the rows and scores, if all the chars are BLOCK_CHAR'''
    while True:
        if all(item[0] == BLOCK_CHAR for item in board[-1]): # Checks the last row
            del board[-1]
            board.insert(0, [(BOARD_CHAR, None)] * BOARD_WIDTH) # inserts a new row at the first index
            score += 1
        else:
            break
    return score, board

def is_board_full(board, block, blocky, blockx, color):
    '''Returns a bool whether the board is filled with blocks or not'''
    if all(item[0] == BOARD_CHAR for item in board[0]):
        return False
    else:
        if not colliding(board, block, blocky, blockx):
            board = draw_block(board, block, blocky, blockx, color)
            if all(item[0] == BOARD_CHAR for item in board[0]):
                return False
            else:
                return True
        else:
            return True

def main(stdscr):
    '''The preparatory part of the game'''
    curses.curs_set(False) # Make the cursor invisible
    stdscr.nodelay(True) # No delaying in checking for user inputs
    stdscr.clear() # Clear the main window

    # Get the height and width of the screen, also the center co-ordinates of the screen
    screen_height, screen_width = stdscr.getmaxyx()
    screen_centery, screen_centerx = screen_height // 2, screen_width // 2

    # Tetris board window measurements
    board_win_height, board_win_width = 21, 11 # I don't know why giving (20, 10) doesn't work.
    board_win_y, board_win_x = (screen_centery - board_win_height // 2), (screen_centerx - board_win_width // 2) # Starting y, x for board_win

    # Score board window measurements
    score_win_height, score_win_width = 2, 11 # Width same as board_win_width
    score_win_y, score_win_x = (board_win_y - score_win_height - 1, board_win_x)

    # Instruction window measurements
    instr_win_height, instr_win_width = 15, 20
    instr_win_y, instr_win_x = (board_win_y), (board_win_x + board_win_width + 5)

    # If the screen is smaller than the board, the program will simply not run
    if (board_win_width + instr_win_width + 5) > screen_width or (board_win_height + score_win_height + 1) > screen_height:
        sys.exit("\nPlease make the terminal full screen or just a bit bigger, buddy")

    # Create all the windows
    board_win = curses.newwin(board_win_height, board_win_width, board_win_y, board_win_x) # Create the board window
    board_win.nodelay(True)
    score_brd_win = curses.newwin(score_win_height, score_win_width, score_win_y, score_win_x)
    score_brd_win.nodelay(True)
    instr_win = curses.newwin(instr_win_height, instr_win_width, instr_win_y, instr_win_x)
    instr_win.nodelay(True)

    # Make the board data structure and the copy
    board_list = make_board_list(BOARD_HEIGHT, BOARD_WIDTH, BOARD_CHAR)
    board_list_copy = []
    # Score
    score = 0
    # Game state
    game_active = True

    while game_active:
        '''Block generating part of the game'''
        # Create the block
        block, block_color = create_new_block(SHAPES)
        y, x = (0, BOARD_WIDTH // 2 - len(block[0]) // 2)
        while True:
            '''Main loop of the game'''
            # If there is a copy, copy that shit. If there isn't make a new one
            if board_list_copy:
                board_list = copy.deepcopy(board_list_copy)

            # Check if the block collides with another block and the board is not full
            if not is_board_full(board_list, block, y, x, block_color):
                if not colliding(board_list, block, y, x):
                    # Draw the block on the board_list
                    board_list = draw_block(board_list, block, y, x, block_color)
                elif colliding(board_list, block, y, x):
                    board_list = draw_block(board_list, block, y - 1, x, block_color) # Don't know why but (y - 1) just works
                    board_list_copy = copy.deepcopy(board_list) # If a block is colliding with another block, then it is another round
                    break
            else:
                game_active = False
                score_brd_win.clear()
                score_brd_win.refresh()
                instr_win.clear()
                instr_win.refresh()
                break

            # Update the score
            score, board_list = score_and_clear(board_list, score)

            # Draw the main game window
            board_win.clear() # Clear the window
            draw_board(board_win, board_list) # Draw the board on the window
            board_win.refresh() # Refresh the window
            # Draw the score board window
            score_brd_win.clear()
            draw_score(score_brd_win, score)
            score_brd_win.refresh()
            # Draw the instruction window
            instr_win.clear()
            draw_instruction(instr_win)
            instr_win.refresh()
            # Refresh the stdscr
            stdscr.refresh()

            # The maximum horizontal and vertical for the block
            maximum_x = board_win_width - 1 - len(block[0])
            maximum_y = board_win_height - 1 - len(block)
            # Make the block move downward
            y += 1
            # Vertical calculations
            if y <= maximum_y:
                if board_list_copy:
                    board_list = copy.deepcopy(board_list_copy)
                else:
                    board_list = make_board_list(BOARD_HEIGHT, BOARD_WIDTH, BOARD_CHAR)
            if y > maximum_y:
                board_list_copy = copy.deepcopy(board_list)
                break

            # Get the key inputs
            key = stdscr.getch()
            # Block movements
            # Quit
            if key == ord('q') or key == ord('Q'):
                # Clear the score and instruction window and break out of the loop
                game_active = False
                score_brd_win.clear()
                score_brd_win.refresh()
                instr_win.clear()
                instr_win.refresh()
                break
            # Move the block right -->
            if key == curses.KEY_RIGHT and x <= maximum_x and y <= maximum_y and not colliding(board_list, block, y, x):
                x += 1
                if x > maximum_x:
                    x = maximum_x
                if colliding(board_list, block, y, x): # If increasing the x makes the block collide with another one, decrease it
                    x -= 1
            # Move the block left <--
            if key ==  curses.KEY_LEFT and x >= 0 and y <= maximum_y and not colliding(board_list, block, y, x):
                x -= 1
                if x < 0:
                    x = 0
                if colliding(board_list, block, y, x): # If decreasing the x makes the block collide with another one, increase it
                    x += 1
            # Rotate the block counter-clockwise
            if key == curses.KEY_UP and (0 <= y < maximum_y) and (0 <= x <= maximum_x) and not colliding(board_list, block, y, x):
                # First make a temporary block
                temp_block = rotate_block(block)
                # Get the maximum y and x for the rotated temporary block
                maximum_x = board_win_width - 1 - len(temp_block[0])
                maximum_y = board_win_height - 1 - len(temp_block)
                # If the y, x is greater than the max value give it the max value
                if y > maximum_y:
                     y = maximum_y
                if x > maximum_x:
                    x = maximum_x
                # Check if the temp block is colliding with any block
                if not colliding(board_list, temp_block, y, x):
                    # Copy that shit
                    block = copy.deepcopy(temp_block)
                    del temp_block # Delete the temporary one
                else:
                    del temp_block # Delete the temporary one because the block cannot be rotated
            # Drop the block
            if key == ord(' ') and (y < maximum_y):
                y = drop_block(board_list, block, y, x, maximum_y) # Get the coordiante of where the block will drop

            # Slow the program for smooth animation
            time.sleep(LEVEL)

    # If the game ends, show a text that says "GAME OVER!" and show the score
    board_win.clear()
    board_win.addstr(board_win_height // 2, 0, 'GAME OVER!')
    board_win.refresh()
    time.sleep(1) # Stop the program for a while to display the "GAME OVER!" text
    board_win.clear()
    draw_score(board_win, score) # Draw the score
    board_win.refresh()
    time.sleep(0.5) # Pause for a little to show the score

if __name__ == "__main__":
    curses.wrapper(main)
