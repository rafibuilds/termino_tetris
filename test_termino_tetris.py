import pytest
from termino_tetris import *

def test_make_board_list():
    """
    Test the creation of the tetris board data structure.
    """
    # Small board
    small_board = make_board_list(5, 5, BOARD_CHAR)
    assert len(small_board) == 5
    assert all(len(row) == 5 for row in small_board)

    # Medium board
    medium_board = make_board_list(10, 10, BOARD_CHAR)
    assert len(medium_board) == 10
    assert all(len(row) == 10 for row in medium_board)

    # Tetris board
    board = make_board_list(20, 10, BOARD_CHAR)
    assert len(board) == 20
    assert all(len(row) == 10 for row in board)

    char = "$"
    custom_board = make_board_list(10, 10, char)
    assert all(all(cell[0] == char for cell in row) for row in custom_board)

def test_rotate_block():
    """
    Test the rotation of a tetris block.
    Ensure that the rotate_block function correctly rotates a tetris block counter-clockwise.
    """
    shape = [
        [1, 0],
        [1, 1]
    ]
    rotated_shape = rotate_block(shape)
    assert rotated_shape == [
        [0, 1],
        [1, 1]
    ]

    rotated_shape = rotate_block(rotated_shape)
    assert rotated_shape == [
        [1, 1],
        [0, 1]
    ]

def test_colliding():
    """
    Test collision detection between a tetris block and the board.
    """
    # No collision test
    block_no_collison = [
         [1, 0],
         [1, 0],
         [1, 1]]
    board_no_collision = make_board_list(10, 10, BOARD_CHAR)
    assert not colliding(board_no_collision, block_no_collison, 0, 0)

    board_collision = make_board_list(5, 5, BOARD_CHAR)
    block_collision = [[1, 1, 1, 1]]
    board_collision[0][0] = (BLOCK_CHAR, None)
    assert colliding(board_collision, block_collision, 0, 0)

def test_drop_block():
    """
    Test dropping a tetris block to the lowest possible position.
    """
     # Test dropping a block when the board is empty
    empty_board = make_board_list(10, 10, BOARD_CHAR)
    block_empty = [[1]]
    new_y_empty = drop_block(empty_board, block_empty, 0, 0, 10 - len(block_empty))
    assert new_y_empty == 9

    # Test dropping a block when there are blocks already present on the board
    board_with_blocks = make_board_list(10, 10, BOARD_CHAR)
    block_with_blocks = [[1]]
    # Add some blocks to the bottom rows of the board
    for row in range(8, 10):
        for col in range(10):
            board_with_blocks[row][col] = (BLOCK_CHAR, None)
    new_y_with_blocks = drop_block(board_with_blocks, block_with_blocks, 0, 0, 10 - len(block_empty))
    assert new_y_with_blocks == 8

def test_score_and_clear():
    """
    Test scoring and clearing filled rows on the tetris board.
    """
    board1 = make_board_list(20, 10, BLOCK_CHAR)
    score1 = 0
    score1, board1 = score_and_clear(board1, score1)
    assert score1 == 20
    assert len(board1) == 20

    board2 = make_board_list(20, 10, BLOCK_CHAR)
    board2.pop()
    board2.insert(-1, [(BOARD_CHAR, None)] * 10)
    score2 = 0
    score2, board2 = score_and_clear(board2, score2)
    assert score2 == 19
    assert len(board2) == 20

    board3 = make_board_list(20, 10, BOARD_CHAR)
    board3.pop()
    board3.pop()
    board3.insert(-1, [(BLOCK_CHAR, None)] * 10)
    board3.insert(-1, [(BLOCK_CHAR, None)] * 10)
    score3 = 0
    score3, board3 = score_and_clear(board3, score3)
    assert score3 == 2
    assert len(board3) == 20

    board4 = make_board_list(20, 10, BOARD_CHAR)
    board4[-1] = [(BLOCK_CHAR, None)] * 10
    board4[18] = [(BLOCK_CHAR, None)] * 10
    board4[17] = [(BLOCK_CHAR, None)] * 10
    score4 = 0
    score4, board4 = score_and_clear(board4, score4)
    assert score4 == 3
    assert len(board4) == 20

def test_is_board_full():
    """
    Test determining if the tetris board is full.
    """
    board = make_board_list(10, 10, BLOCK_CHAR)
    block = [[1]]
    assert is_board_full(board, block, 0, 0, 1)

if __name__ == "__main__":
    pytest.main()
