MOSS: Mathematical Optimization Sudoku Solver

Sudoku can be solved using a 3-index integer linear program (ILP) formulation, (google "ILP Sudoku"
and read the first three hits). So it is pointless to find an alternate 2-index solution. Yet here I am, and
here you are.

MOSS utilizes the absolute value constraint to enforce the all-different rule necesary for a Sudoku solution.
For details of the absolute value constraint, see Gurobi Modeling, "Non Convex Case", page 9:
<https://www.gurobi.com/pdfs/user-events/2017-frankfurt/Modeling-2.pdf>

Thanks to Seth W for the inspiration for this toy problem.