# libraries
import MOSS
import numpy as np

# Define initial Sudoku board (solver input)
# 5x5 Sudoku
gentle_board_5 = np.array([
    [1, 0, 0, 0, 0],
    [2, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 2, 0, 0, 0],
    [0, 5, 0, 0, 0]])
gb5_sol = solve_board(gentle_board_5)

# 7x7 Sudoku
gentle_board_7 = np.array([
    [1, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0],
    [0, 5, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 2]])
gb7_sol = solve_board(gentle_board_7)

# 8x8 Sudoku
gentle_board_8 = np.array([
    [0, 1, 0, 0, 0, 0, 0, 2],
    [0, 7, 0, 6, 4, 0, 0, 0],
    [1, 0, 0, 0, 5, 0, 0, 8],
    [5, 0, 0, 0, 0, 0, 4, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 0, 4, 0, 0, 6, 0],
    [6, 4, 0, 0, 0, 0, 3, 0],
    [2, 0, 0, 0, 6, 7, 5, 0]])
gb8_sol = solve_board(gentle_board_8)

# 9x9 sudoku from https://dingo.sbs.arizona.edu/~sandiway/sudoku/examples.html
gentle_board_9 = np.array([
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]
])
gb9_solved = solve_board(gentle_board_9, max_solve_time=600000)

# 9x9 sodiku difficult board
difficult_board_9 = np.array([
    [2, 0, 0, 3, 0, 0, 0, 0, 0],
    [8, 0, 4, 0, 6, 2, 0, 0, 3],
    [0, 1, 3, 8, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 2, 0, 3, 9, 0],
    [5, 0, 7, 0, 0, 0, 6, 2, 1],
    [0, 3, 2, 0, 0, 6, 0, 0, 0],
    [0, 2, 0, 0, 0, 9, 1, 4, 0],
    [6, 0, 1, 2, 5, 0, 8, 0, 9],
    [0, 0, 0, 0, 0, 1, 0, 0, 2]
])
db9_solved = solve_board(difficult_board_9, max_solve_time=600000)