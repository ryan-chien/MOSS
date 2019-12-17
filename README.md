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
 > (a) Minimize SUM(x_i_j)

With the following constraints:

> (b) SUM(x_i_j)==45 across j for all i
>
> (c) SUM(x_i_j)==45 across i for all j
>
> (d) SUM(x_i_j)==45 for x_i_j within each nonet
>
> (e) ABS(x_i_j - x_i_notj)>=1 for all i, j
>
> (f) ABS(x_i_j - x_noti_j)>=1 for all i, j


## Current Status
As of current (12/16/2019), MOSS satisfies the all-different constraints within each row (e).
Constraints (b) and (c) are also satisfied. However, the all-different constraints within each 
column (f) are not satisfied, and neither are the summation constraints within each nonet (e).
Thus, satisfaction of constraints (e) and (f) are the subject of ongoing study. See below for an example input board,
and MOSS solution (i.e. output).

    Here is the input Sudoku board:
     [  [0, 0, 0, 0, 0, 4, 0, 2, 8],
        [4, 0, 6, 0, 0, 0, 0, 0, 5],
        [1, 0, 0, 0, 3, 0, 6, 0, 0],
        [0, 0, 0, 3, 0, 1, 0, 0, 0],
        [0, 8, 7, 0, 0, 0, 1, 4, 0],
        [0, 0, 0, 7, 0, 9, 0, 0, 0],
        [0, 0, 2, 0, 1, 0, 0, 0, 3],
        [9, 0, 0, 0, 0, 0, 5, 0, 7],
        [6, 7, 0, 4, 0, 0, 0, 0, 0]  ]
    
    MOSS must fill in the zeros...
    
    And the output provided by MOSS:
     [  [6. 3. 5. 7. 1. 4. 9. 2. 8.]
        [4. 1. 6. 2. 8. 9. 3. 7. 5.]
        [1. 2. 7. 8. 3. 4. 6. 9. 5.]
        [2. 6. 8. 3. 7. 1. 5. 9. 4.]
        [9. 8. 7. 6. 5. 3. 1. 4. 2.]
        [4. 2. 8. 7. 5. 9. 1. 3. 6.]
        [4. 8. 2. 6. 1. 9. 7. 5. 3.]
        [9. 8. 1. 2. 6. 4. 5. 3. 7.]
        [6. 7. 1. 4. 9. 2. 8. 3. 5.]  ]

## Acknowledgements
Thanks to Seth W for the inspiration for this toy problem, the COIN CBC developers for making a great open-source
ILP solver, and the google-ortools team for the mathematical modeling interface.

## Dependencies
MOSS is dependent on 'ortools' and 'numpy'.