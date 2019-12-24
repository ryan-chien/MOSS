# MOSS: Mathematical Optimization Sudoku Solver

## Background
Sudoku can be solved using a 3-index integer linear program (ILP) formulation using only binary variables,
(google "ILP Sudoku" and read the first three hits). 

***But can it be solved with a two-index formulation using
integer values [1,9]? (Yes.)***

## Modeling Approach
MOSS is based on finding a feasible solution to the following system of equations:
```
(a) Minimize SUM(x_ij)
```

With the following constraints:
```
(b) SUM(x_ij)==45 across j for all i
(c) SUM(x_ij)==45 across i for all j
(d) SUM(x_ij)==45 for x_i_j within each nonet
(e) ABS(x_ij - x_i_notj)>=1 for all i, j
(f) ABS(x_ij - x_noti_j)>=1 for all i, j
```
Where x is the Sudoku board, and, x_ij are cell-values within the board.

MOSS solves Sudoku entirely using an ILP solver (e.g. COIN-OR CBC, CPLEX, and Gurobi). Heuristics
are restricted to use only within the solver, (i.e. only those heuristics integrated into
COIN-OR CBC are used). Heuristics designed specifically for Sudoku are *not* used.

MOSS utilizes the absolute value constraint to enforce the all-different rule necesary for a Sudoku solution.
For details of the absolute value constraint, see Gurobi Modeling, "Non Convex Case", page 9:
<https://www.gurobi.com/pdfs/user-events/2017-frankfurt/Modeling-2.pdf>.

For details of the formulation, see Appendix A: Mathematical Formulation.

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

## Appendix A: Mathematical Formulation
As noted above, MOSS solves Sudoku by finding a feasible solution to the following system of equations:
With the following constraints:
```
(b) SUM(x_ij)==45 across j for all i
(c) SUM(x_ij)==45 across i for all j
(d) SUM(x_ij)==45 for x_i_j within each nonet
(e) ABS(x_ij - x_i_notj)>=1 for all i, j
(f) ABS(x_ij - x_noti_j)>=1 for all i, j
```
Where x is the Sudoku board, and, x_ij are cell-values within the board.

While constraints [b, c, d] are relatively simple, constraints [e, f] are quite tricky to implement. Absolute value
variables are non-linear, and therefore cannot be directly programmed into an ILP. The following approach is used
to implement constraints [e, f]:

First, set variable 't' equal to the difference of each objective value pair. Set 't' bounds to
 [-10, 10]. For example:
```
 (g) t_01_02 = x01 - x02
```

Second, initiate variables 'p' and 'n' with bounds [0, 10]. For example:
```
 (h) 0 <= p_01_02 <= 10
 (i) 0 <= n_01_02 <= 10
```

Third, initiate variable 'z' with bounds [1, 10]. For example:
```
 (j) 1 <= z_01_02 <= 10
```

Fourth, initiate binary variable 'y'. For example:
```
 (k) 0 <= y_01_02 <= 1
```

Fifth, set 't' equal to the difference of 'p' and 'n'. For example:
```
 (l) t_01_02 = p_01_02 - n_01_02
```

Sixth, constraint that the difference of p and 10*y must be less than or equal to zero. For example:
```
 (m) p_01_02 - 10*y_01-02 <= 0
```

Seventh, constraint that the sum of n and 10*y must be less than or equal to ten. For example:
```
 (n) n_01_02 + 10*y_01_02 <= 10
```

Given steps 1-7, then 'z' will be the absolute value of the objective value pair. I.e.:
```
  z_01_02 = abs(x01 - x02)   iff    constraints [g, h, i, j, k, l, m, n] are TRUE
```

Therefore, we apply [g - n] for each objective value pair and thereby constrain z to be greater than 
or equal to one. Thus, the all-different constraint is satisfied. (Assumes x_ij in [1, 9].)