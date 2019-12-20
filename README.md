# MOSS: Mathematical Optimization Sudoku Solver

## Background
Sudoku can be solved using a 3-index integer linear program (ILP) formulation, (google "ILP Sudoku"
and read the first three hits). So it is pointless to find an alternate 2-index solution. Yet here I am, and
here you are.

MOSS utilizes the absolute value constraint to enforce the all-different rule necesary for a Sudoku solution.
For details of the absolute value constraint, see Gurobi Modeling, "Non Convex Case", page 9:
<https://www.gurobi.com/pdfs/user-events/2017-frankfurt/Modeling-2.pdf>

## Modeling Approach
MOSS is based on finding a feasible solution to:
```
(a) Minimize SUM(x_i_j)
```

With the following constraints:
```
(b) SUM(x_i_j)==45 across j for all i
(c) SUM(x_i_j)==45 across i for all j
(d) SUM(x_i_j)==45 for x_i_j within each nonet
(e) ABS(x_i_j - x_i_notj)>=1 for all i, j
(f) ABS(x_i_j - x_noti_j)>=1 for all i, j
```

## Current Status
As of current (12/20/2019), MOSS satisfies constraints (b, c, e, f).

``` {python}
>>> import MOSS
>>> import numpy as np

>>> difficult_board_9 = np.array([
...     [2, 0, 0, 3, 0, 0, 0, 0, 0],
...     [8, 0, 4, 0, 6, 2, 0, 0, 3],
...     [0, 1, 3, 8, 0, 0, 2, 0, 0],
...     [0, 0, 0, 0, 2, 0, 3, 9, 0],
...     [5, 0, 7, 0, 0, 0, 6, 2, 1],
...     [0, 3, 2, 0, 0, 6, 0, 0, 0],
...     [0, 2, 0, 0, 0, 9, 1, 4, 0],
...     [6, 0, 1, 2, 5, 0, 8, 0, 9],
...     [0, 0, 0, 0, 0, 1, 0, 0, 2]
... ])

>>> db9_solved = solve_board(difficult_board_9, max_solve_time=600000)
(1) Initializing optimization model...
(2) Creating objective variables...
(3) Setting constraints...
0
Success!

>>> db9_solved['solution_values']
array([[2, 9, 8, 3, 1, 7, 4, 5, 6],
       [8, 5, 4, 1, 6, 2, 9, 7, 3],
       [9, 1, 3, 8, 4, 5, 2, 6, 7],
       [1, 4, 6, 7, 2, 8, 3, 9, 5],
       [5, 8, 7, 4, 9, 3, 6, 2, 1],
       [7, 3, 2, 9, 8, 6, 5, 1, 4],
       [3, 2, 5, 6, 7, 9, 1, 4, 8],
       [6, 7, 1, 2, 5, 4, 8, 3, 9],
       [4, 6, 9, 5, 3, 1, 7, 8, 2]])
```

## Acknowledgements
Thanks to Seth W for the inspiration for this toy problem, the COIN CBC developers for making a great open-source
ILP solver, and the google-ortools team for the mathematical modeling interface.

## Dependencies
MOSS is dependent on 'ortools' and 'numpy'.