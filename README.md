# Termino Tetris
This is a Python program to play Tetris in the terminal/console. It utilizes the `curses` library for terminal handling.

#### Video demo: [Tetris in the terminal](https://youtu.be/-T2U5NGxXmA)

## How to Run

#### **Windows OS**:
1. First, make sure you have Python installed on your system.

2. Clone the repository containing the Tetris program:
    ```
    git clone https://www.github.com/rafibuilds/termino_tetris.git
    ```
3. Navigate to the directory where the program is cloned.
   ```
   cd termino_tetris
   ```
4. Install the `windows-curses` package using pip:
    ```
    pip install windows-curses
    ```
5. Run the program:
    ```
    python termino_tetris.py
    ```

#### **Unix/MacOS**:
The `curses` module is a standard library for Python in Unix/Mac devices

1. First, make sure you have Python installed on your system.

2. Clone the repository containing the Tetris program:
    ```
    git clone https://www.github.com/rafibuilds/termino_tetris.git
    ```
3. Navigate to the directory where the program is cloned.
   ```
   cd termino_tetris
   ```
4. Run the program:
   ```
   python termino_tetris.py
   ```

## Instructions
- **Move Right:** Use the RIGHT Arrow Key `->`
- **Move Left:** Use the LEFT Arrow Key `<-`
- **Rotate Block:** Use the UP Arrow Key `^`
- **Drop Block:** Press the Space Bar `|__|`
- **Quit:** Press `q`

**W, A, S, D will not work**

## Program Overview
- **Game Constants:** Definitions of various constants such as `BLOCK_CHAR`, `BOARD_CHAR`, `SHAPES`, `LEVEL`.

- **Shapes:** Basically a 2D list under the constant `SHAPES`.
- **Functions:**
    - `create_new_block`: Generates a random block shape and color.
    - `draw_board`: Draws the Tetris board on the screen.
    - `draw_score`: Draws the score board.
    - `draw_instruction`: Draws the instruction window.
    - `make_board_list`: Creates the board data structure.
    - `rotate_block`: Rotates the block counter-clockwise.
    - `draw_block`: Puts the block on the board.
    - `colliding`: Checks if the block collides with another block.
    - `drop_block`: Drops the block until it collides with another block or reaches the bottom.
    - `score_and_clear`: Clears full rows and updates the score.
    - `is_board_full`: Checks if the board is filled with blocks.
    - `main`: Main function to run the game.

## Dependencies
- `curses`: Main module for terminal/console handling.
- `time`: For smooth animation of the game.
- `random`: To randomize the blocks in the game.
- `sys`: System handling.
- `copy`: For effective copying of the 2D list.

## Function Explanations
### 1. **create_new_block(shapes: list[list[list[int]]]) -> tuple[list[list[int]], int]**
Generates a new block and its color randomly. The `shapes` argument value comes from `SHAPES`, which is a list of block shapes represented as nested lists. Each item of `shpaes` is a list and that list contains more lists. This function initializes colors using the `curses.init_pair()` function and assigns each color a specific ID number. Then, it randomly selects a block shape from `shapes` and returns both the block shape and its corresponding color.

### 2. **draw_board(window: "_curses.window", board: list[list[tuple[str, int]]]) -> None**
Draws the Tetris board on the screen. The `board` is a 2D list where each element is a list and each inner list is a list of tuples containing a string representing the character to be drawn and an integer representing the color. This function iterates through each row of the board, and for each character, it uses the `window.addstr()` method to print it on the specified `window`. If the character is `BLOCK_CHAR` then color will be added with the str.

### 3. **draw_score(window: "_curses.window", score: int) -> None**
Draws the score board on the screen. It takes the `window` object and the `score` as parameters. Inside the function, it constructs the score text using the provided score value and uses `window.addstr()` to print it on the `window`.

### 4. **draw_instruction(window: "_curses.window") -> None**
Draws the instruction window on the screen, providing guidance on how to play the game. It uses the `window.addstr()` method to print the instructions on the specified `window`.

### 5. **make_board_list(rows: int, cols: int, char: str) -> list[list[tuple[str, None]]]**
Creates the board data structure as a 2D list. It initializes the board with a specified character (`char`) and returns the constructed board. The `board` is a list of `rows` lists and each row has `cols` tuples and each tuple has str. There is a color int if the str is `BLOCK_CHAR` otherwise it will be `None`.

### 6. **rotate_block(shape: list[list[int]]) -> list[list[int]]**
Rotates the given block `shape` counter-clockwise. It takes a block `shape` represented as a 2D list and returns the rotated shape. It calculates the width and height of the input `shape` array using the lengths of its first row and the number of rows, respectively. It creates a new 2D array `new_block` with dimensions swapped, so the width of `new_block` becomes the height of `shape`, and vice versa. It iterates over each element of the original `shape` array, and for each element, it calculates its new position in the `new_block` array. The new position of an element from `shape` is determined by its column and row indices, which are swapped, and its new row index is calculated as (width - col - 1) and its column index remains the same. Finally, the function returns the `new_block`, which represents the original block rotated counter-clockwise by 90 degrees.

### 7. **draw_block(board: list[list[tuple[str, int]]], block: list[list[int]], blocky: int, blockx: int, color: int) -> list[list[tuple[str, int]]]**
Places the given block on the board at the specified position which is `blocky`, `blockx` with the specified `color`. It modifies the `board` by adding the `block` to it and returns the updated `board`.

### 8. **colliding(board: list[list[tuple[str, int]]], block: list[list[int]], blocky: int, blockx: int) -> bool**
Checks if the given block collides with another block on the board at the specified position. It returns `True` if there is a collision, otherwise `False`.

### 9. **drop_block(board: list[list[tuple[str, int]]], block: list[list[int]], blocky: int, blockx: int, max_vertical: int) -> int**
Drops the given block vertically until it collides with another block or reaches the bottom of the board. It returns the new vertical position of the block after dropping.

### 10. **score_and_clear(board: list[list[tuple[str, int]]], score: int) -> tuple[int, list[list[tuple[str, int]]]]**
Clears full rows on the `board`, updates the score accordingly, and returns the updated `score` and `board`. It iterates through the last row of the board, checks if it is full, clears it if necessary, and updates the score and the process iterates untill the last row is not filled with `BLOCK_CHAR`.

### 11. **is_board_full(board: list[list[tuple[str, int]]], block: list[list[int]], blocky: int, blockx: int) -> bool**
Checks if the board is completely filled with blocks. For this the whole board doesn't need to be checked, only the top row is sufficient. The function first checks if the first row of `board` is filled with `BOARD_CHAR`, if it is then `board` is not full and returns `False`. If it is not, then it will see if putting the `block` at `blocky` position will make the `block` collide with another one. If it doesn't then the `block` will be drawn on the `board` with `draw_block()` function. Then again the first row will be checked. After this continuous process, `True` or `False` will be returned on the basis if the `board` is full or not.

### 12. **main(stdscr: "_curses.window") -> None**
#### Preparatory Setup
- The preparatory setup section initializes the environment for the game, ensuring it is ready for gameplay. Each step is crucial for setting up the game environment:
  - `curses.curs_set(False)`: This function call hides the cursor, preventing it from being displayed on the screen during gameplay. This enhances the player's focus on the game elements rather than distractions like a blinking cursor.
  - `stdscr.nodelay(True)`: By enabling non-blocking input, the game can continuously check for user input without waiting for keypresses. This feature is essential for responsive gameplay, allowing the game to react quickly to player actions.
  - `stdscr.clear()`: Clearing the main window ensures a clean starting point for rendering game elements. It removes any previous content, providing a blank canvas for the Tetris game.

#### Window Setup
- The window setup section calculates the dimensions and positions of various game windows and creates them using the `curses` library:
  - Tetris Board Window (`board_win`):
    - Its dimensions (`board_win_height`, `board_win_width`) are calculated based on the desired size for displaying the Tetris game board. These dimensions ensure that the board fits comfortably within the terminal window.
    - The position (`board_win_y`, `board_win_x`) is determined relative to the screen center, ensuring the board appears centered on the screen.
    - The window is created using `curses.newwin()` with the calculated dimensions and position, providing a dedicated space for rendering the Tetris game board.
  - Score Board Window (`score_brd_win`):
    - Similar to the Tetris board window, its dimensions (`score_win_height`, `score_win_width`) are calculated, ensuring it fits neatly above the Tetris board.
    - The position (`score_win_y`, `score_win_x`) places the score board window just above the Tetris board window.
    - It is also created using `curses.newwin()`, providing a separate space for displaying the game score.
  - Instruction Window (`instr_win`):
    - Its dimensions (`instr_win_height`, `instr_win_width`) are determined to accommodate instructions for gameplay.
    - The position (`instr_win_y`, `instr_win_x`) situates the instruction window adjacent to the Tetris board window, providing guidance without obstructing gameplay.
    - Like the other windows, it is created using `curses.newwin()`, offering a dedicated area for displaying game instructions.

#### Game Loop
- The game loop is the heart of the Tetris game, orchestrating various game elements and interactions. It runs continuously until the game ends, executing the following key tasks:
  - Block Generation, Movement, and Collision Detection:
    - Blocks are randomly generated using the `create_new_block()` function, selecting shapes and colors for each block.
    - The block's position (`y`, `x`) is updated based on user input, allowing for left, right, rotation, and dropping movements. The block automatically moves downward
    - Collision detection ensures that blocks interact correctly with the game board and other blocks, preventing overlap or unintended behavior and it is done with the `colliding()` function.
  - Scoring and Display Updates:
    - Scoring occurs when complete rows are cleared, and the `score_and_clear()` function handles this process.
    - The game continuously updates the display, rendering the Tetris game board, score board, and instruction window to reflect the current game state.
  - User Input Handling:
    - The function listens for user input, interpreting keypresses to control block movement, rotation, and quitting the game. The input is handled by the `stdscr.getch()` method.
  - Smooth Animation:
    - Time delays introduced using `time.sleep()` ensure smooth animation of block movement and game rendering, enhancing the overall gaming experience.

#### Block Generation and Movement
- This section elaborates on the block generation and movement mechanics within the game loop, providing insights into how blocks are created, positioned, and manipulated:
  - Random Block Generation:
    - Blocks are generated randomly using the `create_new_block()` function, which selects shapes and colors from predefined options.
  - Block Movement and Collision Detection:
    - User input determines block movement, allowing players to shift, rotate, or drop blocks within the game board. The block moves downward automatically.
    - Collision detection ensures that blocks interact correctly with existing game elements, preventing overlaps or conflicts and is done with `collding()` function.

#### Scoring
- Scoring mechanisms are essential for tracking player performance and providing feedback on gameplay progress. This section explains how scoring is implemented and updated during gameplay:
  - Row Clearing and Scoring:
    - When complete rows are cleared, the `score_and_clear()` function handles the scoring process, updating the player's score accordingly.
  - Feedback and Progress Tracking:
    - Scoring provides players with feedback on their performance and progress, motivating them to achieve higher scores and improve their gameplay skills.

#### Game Over
- The game over condition marks the end of gameplay and prompts players to review their final performance. This section describes how the game over state is triggered and displayed to players:
  - End of Gameplay:
    - The game ends when the game board is filled with blocks, and there is no space to spawn new blocks.
  - Displaying Final Results:
    - Upon game over, the function displays "GAME OVER!" on the Tetris board window and shows the final score, allowing players to review their performance.

#### Input Handling
- Effective input handling is crucial for providing players with responsive and intuitive controls. This section explains how user input is processed and utilized within the game loop:
  - Control Mapping:
    - User input, such as keypresses, is mapped to specific actions within the game, such as block movement, rotation, or quitting the game. Key inputs are recorded with the `stdscr.getch()` method.
  - Responsiveness and Feedback:
    - Responsive input handling ensures that player actions are promptly reflected in the game, providing immediate feedback and enhancing the overall gaming experience.

#### Cleanup
- Proper cleanup procedures ensure that the game environment is reset and resources are released appropriately. This section outlines the cleanup process after the game ends or the player quits:
  - Clearing Windows:
    - All game windows are cleared to remove any remaining content and prepare for the next game session.
  - Exiting Curses:
    - The function exits curses using `curses.wrapper()`, ensuring that the curses library is unloaded properly and the terminal state is restored.

## Testing the game
### Pytest
[Pytest](https://docs.pytest.org/en/8.2.x/) is a third-party package/library. It is a testing framework that makes it easy to make and execute tests for programs. Tests can be easily run from the command prompt for a single file or a whole directory. To use the script as a python program the `pytest.main()` is necessary.
To run tests from the terminal:
```
pytest test_termino_tetris.py
```
The file name should have a `test_*.py` suffix.

### Test functions
#### `test_make_board_list()`
Tests the creation of the Tetris board data structure using various board sizes and characters.

#### `test_rotate_block()`
Tests the rotation of a Tetris block counter-clockwise.

#### `test_colliding()`
Tests collision detection between a Tetris block and the board.

#### `test_drop_block()`
Tests dropping a Tetris block to the lowest possible position on the board.

#### `test_score_and_clear()`
Tests scoring and clearing filled rows on the Tetris board.

#### `test_is_board_full()`
Tests determining if the Tetris board is full.
