# libraries
import numpy as np
execfile("C:/gitrepo/moss/source/MOSS.py")

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
gb9_sol = solve_board(gentle_board_9, max_solve_time=600000)
print(gb9_sol['solution'])

# 9x9 medium difficulty
medium_board_9 = np.array([
    [0, 9, 0, 5, 0, 0, 0, 0, 8],
    [0, 0, 3, 0, 0, 7, 0, 2, 0],
    [8, 0, 1, 0, 0, 0, 6, 0, 0],
    [0, 6, 0, 0, 0, 8, 3, 9, 2],
    [0, 0, 0, 0, 2, 0, 0, 0, 0],
    [1, 2, 8, 6, 0, 0, 0, 4, 0],
    [0, 0, 9, 0, 0, 0, 7, 0, 5],
    [0, 1, 0, 2, 0, 0, 4, 0, 0],
    [3, 0, 0, 0, 0, 5, 0, 1, 0]
])
mb9_sol = solve_board(medium_board_9, max_solve_time=10800000)  # unfortunately, COIN CBC cannot solve this problem
print(mb9_sol['solution'])
with open("mb9.lp", "w") as text_file:  # therefore, export to lp, and solve with CPLEX
    print(mb9_sol['lp_file'], file=text_file)

# 9x9 difficult board
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
db9_sol = solve_board(difficult_board_9, max_solve_time=1200000)
print(db9_sol['solution'])
with open("./lp_files/db9.lp", "w") as text_file:
    print(db9_sol['lp_file'], file=text_file)

# Evil board
evil_board_9 = np.array([
    [1, 0, 6, 0, 0, 7, 0, 0, 3],
    [9, 2, 0, 0, 3, 0, 0, 0, 0],
    [0, 5, 0, 0, 8, 0, 0, 6, 0],
    [0, 0, 0, 8, 0, 0, 0, 0, 6],
    [0, 1, 0, 0, 0, 0, 0, 5, 0],
    [5, 0, 0, 0, 0, 4, 0, 0, 0],
    [0, 8, 0, 0, 9, 0, 0, 2, 0],
    [0, 0, 0, 0, 2, 0, 0, 9, 4],
    [6, 0, 0, 3, 0, 0, 7, 0, 8]
])
eb9_sol = solve_board(evil_board_9)  # unfortunately, COIN CBC cannot solve this problem
print(eb9_sol['solution'])
with open("./lp_files/eb9.lp", "w") as text_file:  # therefore, export to lp, and solve with CPLEX
    print(eb9_sol['lp_file'], file=text_file)