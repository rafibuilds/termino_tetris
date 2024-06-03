# Termino Tetris

This is a Python program to play Tetris in the terminal/console. It utilizes the `curses` library for terminal handling.

## How to Run

#### **Windows OS**:

1. First, make sure you have Python installed on your system.
2. Clone the repository containing the Tetris program:

    ```
    git clone https://github.com/rafibuilds/termino_tetris
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
The `curses` module is already installed in Unix/Mac devices

1. First, make sure you have Python installed on your system.
2. Clone the repository containing the Tetris program:

    ```
    git clone https://github.com/rafibuilds/termino_tetris
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
- **Quit:** Press `q`.

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

#### 1. `create_new_block(shapes: list[list[list[int]]]) -> tuple[list[list[int]], int]`
Generates a new block and its color randomly. The `shapes` argument value comes from `SHAPES`, which is a list of block shapes represented as nested lists. Each item of `shpaes` is a list and that list contains more lists. This function initializes colors using the `curses.init_pair()` function and assigns each color a specific ID number. Then, it randomly selects a block shape from `shapes` and returns both the block shape and its corresponding color.

#### 2. `draw_board(window: "_curses.window", board: list[list[tuple[str, int]]]) -> None`
Draws the Tetris board on the screen. The `board` is a 2D list where each element is a list and each inner list is a list of tuples containing a string representing the character to be drawn and an integer representing the color. This function iterates through each row of the board, and for each character, it uses the `window.addstr()` method to print it on the specified `window`. If the character is `BLOCK_CHAR` then color will be added with the str.

#### 3. `draw_score(window: "_curses.window", score: int) -> None`
Draws the score board on the screen. It takes the `window` object and the `score` as parameters. Inside the function, it constructs the score text using the provided score value and uses `window.addstr()` to print it on the `window`.

#### 4. `draw_instruction(window: "_curses.window") -> None`
Draws the instruction window on the screen, providing guidance on how to play the game. It uses the `window.addstr()` method to print the instructions on the specified `window`.

#### 5. `make_board_list(rows: int, cols: int, char: str) -> list[list[tuple[str, None]]]`
Creates the board data structure as a 2D list. It initializes the board with a specified character (`char`) and returns the constructed board. The `board` is a list of `rows` lists and each row has `cols` tuples and each tuple has str. There is a color int if the str is `BLOCK_CHAR` otherwise it will be `None`.

#### 6. `rotate_block(shape: list[list[int]]) -> list[list[int]]`
Rotates the given block `shape` counter-clockwise. It takes a block `shape` represented as a 2D list and returns the rotated shape. It calculates the width and height of the input `shape` array using the lengths of its first row and the number of rows, respectively. It creates a new 2D array `new_block` with dimensions swapped, so the width of `new_block` becomes the height of `shape`, and vice versa. It iterates over each element of the original `shape` array, and for each element, it calculates its new position in the `new_block` array. The new position of an element from `shape` is determined by its column and row indices, which are swapped, and its new row index is calculated as (width - col - 1) and its column index remains the same. Finally, the function returns the `new_block`, which represents the original block rotated counter-clockwise by 90 degrees.

#### 7. `draw_block(board: list[list[tuple[str, int]]], block: list[list[int]], blocky: int, blockx: int, color: int) -> list[list[tuple[str, int]]]`
Places the given block on the board at the specified position which is `blocky`, `blockx` with the specified `color`. It modifies the `board` by adding the `block` to it and returns the updated `board`.

#### 8. `colliding(board: list[list[tuple[str, int]]], block: list[list[int]], blocky: int, blockx: int) -> bool`
Checks if the given block collides with another block on the board at the specified position. It returns `True` if there is a collision, otherwise `False`.

#### 9. `drop_block(board: list[list[tuple[str, int]]], block: list[list[int]], blocky: int, blockx: int, max_vertical: int) -> int`
Drops the given block vertically until it collides with another block or reaches the bottom of the board. It returns the new vertical position of the block after dropping.

#### 10. `score_and_clear(board: list[list[tuple[str, int]]], score: int) -> tuple[int, list[list[tuple[str, int]]]]`
Clears full rows on the `board`, updates the score accordingly, and returns the updated `score` and `board`. It iterates through the last row of the board, checks if it is full, clears it if necessary, and updates the score and the process iterates untill the last row is not filled with `BLOCK_CHAR`.

#### 11. `is_board_full(board: list[list[tuple[str, int]]], block: list[list[int]], blocky: int, blockx: int, color: int) -> bool`
Checks if the board is completely filled with blocks. For this the whole board doesn't need to be checked, only the top row is sufficient. The function first checks if the first row of `board` is filled with `BOARD_CHAR`, if it is then `board` is not full and returns `False`. If it is not, then it will see if putting the `block` at `blocky` position will make the `block` collide with another one. If it doesn't then the `block` will be drawn on the `board` with `draw_block()` function. Then again the first row will be checked. After this continuous process, `True` or `False` will be returned of the basis if the `board` is full or not.

#### 12. `main(stdscr: "_curses.window") -> None` 
The main function of the game.

### Dependencies:
- `curses`: Main module for terminal/console handling.
- `time`: For smooth animation of the game.
- `random`: To randomize the blocks in the game.
- `sys`: System handling.
- `copy`: For effective copying of the 2D list.
