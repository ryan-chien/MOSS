# libraries
import MOSS as MOSS
import numpy as np

# Define initial Sudoku board (solver input)
# 5x5 Sudoku
gentle_board_5 = np.array([
    [1, 0, 0, 0, 0],
    [2, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 2, 0, 0, 0],
    [0, 5, 0, 0, 0]])
gb5_sol = MOSS.solve_board(gentle_board_5)

# 7x7 Sudoku
gentle_board_7 = np.array([
    [1, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0],
    [0, 5, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 2]])
gb7_sol = MOSS.solve_board(gentle_board_7)

# 8x8 Sudoku
gentle_board_8 = np.array([
    [0, 1, 0, 0, 0, 0, 0, 2],
    [0, 7, 0, 6, 4, 0, 0, 0],
    [1, 0, 0, 0, 5, 0, 0, 8],
    [5, 0, 0, 0, 0, 0, 4, 0]
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 0, 4, 0, 0, 6, 0],
    [6, 4, 0, 0, 0, 0, 3, 0],
    [2, 0, 0, 0, 6, 7, 5, 0]])
gb8_sol = MOSS.solve_board(gentle_board_8)

# board from <https://www.sudokuwiki.org/sudoku.htm>, "Gentle"
gentle_board_9 = np.array([
    [0, 0, 0, 0, 0, 4, 0, 2, 8],
    [4, 0, 6, 0, 0, 0, 0, 0, 5],
    [1, 0, 0, 0, 3, 0, 6, 0, 0],
    [0, 0, 0, 3, 0, 1, 0, 0, 0],
    [0, 8, 7, 0, 0, 0, 1, 4, 0],
    [0, 0, 0, 7, 0, 9, 0, 0, 0],
    [0, 0, 2, 0, 1, 0, 0, 0, 3],
    [9, 0, 0, 0, 0, 0, 5, 0, 7],
    [6, 7, 0, 4, 0, 0, 0, 0, 0]])
gb9_solved = MOSS.solve_board(gentle_board_9, max_solve_time=600000)