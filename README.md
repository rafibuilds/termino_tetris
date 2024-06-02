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

### 1. create_new_block(shapes: Any) -> tuple[Any, int]
Generates a new block from `shapes`. `shapes` argument value will come from `SHAPES` constant. The function first initializes all the colors with the `curses.init_pair()` function and each color has a specific id number(0 is exclusively reserved for Black and White). `curses.init_pair()` has three parameters which is the color id number, foreground(the color that is on top) and background. In this game, the fg and bd colors are given by the `curses` module's color constants. After the initialization step, a random block is generated from `shapes` and both block and color is returned.

### 2. draw_board(window: Any, board: Any) -> Any


### 3. draw_score(window: Any, score: int) -> Any


### 4. draw_instruction(window: Any) -> Any


### 5. make_board_list(rows: int, cols: int, char: str) -> Any


### 6. rotate_block(shape: Any) -> Any
