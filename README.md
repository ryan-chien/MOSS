# MOSS: Mathematical Optimization Sudoku Solver

## Background
Sudoku can be solved using a 3-index integer linear program (ILP) formulation using only binary variables,
(google "ILP Sudoku" and read the first three hits). 

***But can it be solved with a two-index formulation using
integer values [1:9]? (Yes.)***


## Modeling Approach
MOSS is based on finding a feasible solution to the following system of equations:
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
Where x is the Sudoku board, and, x_i_j are cell-values within the board.

Heuristics are completely unused. MOSS solves Sudoku using mathematical optimization only.

MOSS utilizes the absolute value constraint to enforce the all-different rule necesary for a Sudoku solution.
For details of the absolute value constraint, see Gurobi Modeling, "Non Convex Case", page 9:
<https://www.gurobi.com/pdfs/user-events/2017-frankfurt/Modeling-2.pdf>.

## Current Status
As of 12/20/2019 MOSS satisfies all constraints.
Now witness the firepower of this fully armed and operational battle station!

<img src="/other/demo.gif" width="450" height="350">

``` {python}
gentle_board_9 = np.array([
...    [0, 0, 0, 2, 6, 0, 7, 0, 1],
...    [6, 8, 0, 0, 7, 0, 0, 9, 0],
...    [1, 9, 0, 0, 0, 4, 5, 0, 0],
...    [8, 2, 0, 1, 0, 0, 0, 4, 0],
...    [0, 0, 4, 6, 0, 2, 9, 0, 0],
...    [0, 5, 0, 0, 0, 3, 0, 2, 8],
...    [0, 0, 9, 3, 0, 0, 0, 7, 4],
...    [0, 4, 0, 0, 5, 0, 0, 3, 6],
...    [7, 0, 3, 0, 1, 8, 0, 0, 0]
...])
gb9_solved = solve_board(gentle_board_9, max_solve_time=600000)
...
(1) Initializing optimization model...
(2) Creating objective variables...
(3) Setting constraints...
0
Success!
Board of size 9 solved in 0 seconds, using 134 simplex iterations.
print(gb9_solved['solution'])
[[4 3 5 2 6 9 7 8 1]
 [6 8 2 5 7 1 4 9 3]
 [1 9 7 8 3 4 5 6 2]
 [8 2 6 1 9 5 3 4 7]
 [3 7 4 6 8 2 9 1 5]
 [9 5 1 7 4 3 6 2 8]
 [5 1 9 3 2 6 8 7 4]
 [2 4 8 9 5 7 1 3 6]
 [7 6 3 4 1 8 2 5 9]]
```

## Acknowledgements
Thanks to Seth W for the inspiration for this toy problem, the COIN CBC developers for making a great open-source
ILP solver, and the google-ortools team for the mathematical modeling interface.

## Dependencies
MOSS is dependent on 'ortools' and 'numpy'.

## Closing Remarks
It is possible solve Sudoku with a two-index ILP formulation. However, the two-index solution
is slower than commonly available heuristic solvers. It would be interesting to compare solve
times using a commercial ILP solver such as Gurobi or CPLEX, versus the current open-source 
COIN-OR CBC solver.