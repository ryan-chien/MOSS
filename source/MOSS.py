# MOSS: Mathematical Optimization Sudoku Solver
# Ryan Chien
# 12/16/2019
# The objective of this code is to use an two-index integer linear program to solve Sudoku
# The more common ILP method of solving Sudoku is with three indicies:
### Example 1: <https://towardsdatascience.com/using-integer-linear-programming-to-solve-sudoku-puzzles-15e9d2a70baa>
### Example 2: <https://www.mathworks.com/help/optim/examples/solve-sudoku-puzzles-via-integer-programming.html>

#libraries
from ortools.linear_solver import pywraplp
import numpy as np

# Define initial Sudoku board (solver input)
## board from <https://www.sudokuwiki.org/sudoku.htm>, "Gentle"
initial_board = np.array([
    [0, 0, 0, 0, 0, 4, 0, 2, 8],
    [4, 0, 6, 0, 0, 0, 0, 0, 5],
    [1, 0, 0, 0, 3, 0, 6, 0, 0],
    [0, 0, 0, 3, 0, 1, 0, 0, 0],
    [0, 8, 7, 0, 0, 0, 1, 4, 0],
    [0, 0, 0, 7, 0, 9, 0, 0, 0],
    [0, 0, 2, 0, 1, 0, 0, 0, 3],
    [9, 0, 0, 0, 0, 0, 5, 0, 7],
    [6, 7, 0, 4, 0, 0, 0, 0, 0]
])

# Create solver
print("(1) Initializing optimization model...")
solver = pywraplp.Solver(
    "Sudoku",
    pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
objective = solver.Objective()
objective.SetMinimization

# Create objective variable array
print("(2) Creating objective variables...")
objective_vars = np.array([
    [solver.IntVar(1, 9, 'x' + str(j) + str(i)) for i in range(0, 9)]
    for j in range(0, 9)])

# Set constraints
print("(3) Setting constraints...")
## Initial board
initial_board_constraints = [[]] * 9
for i in range(0, 9):
    for j in range(0, 9):
        if initial_board[i][j] != 0:
            initial_board_constraints[i].append(
                solver.Add(
                    objective_vars[i][j] == initial_board[i][j],
                    'init_x'+str(i)+str(j)+'=='+str(initial_board[i][j])))
        else:
            initial_board_constraints[i].append(
                'init_x'+str(i)+str(j)+'==NONE'
            )

## Sum of Rows Must Equal 45
constraint_a = [[]] * 9
for i in range(0, 9):
    # set addition
    constraint_a[i] = solver.Add(
        sum(objective_vars[i]) == 45)

## Sum of Columns Must Equal 45
constraint_b = [[]] * 9
for j in range(0, 9):
    constraint_b[j] = solver.Add(
        sum(objective_vars[:, j]) == 45)

## Absolute Value Constraints, i for all j
### absolute value constraints, part 1
constraint_var_t_iforallj = []
constraint_t_iforallj = []
for i in range(0, 9):
    constraint_var_t_i = []
    constraint_t_i = []
    for k in range(0, 8):
        constraint_var_t_j = []
        constraint_t_j = []
        for j in range(0+k, 8):
            #### define variable t, integer, range of -99 to 99
            #### one t for each unique objective variable x pair
            constraint_var_t_j.append(
                solver.IntVar(
                    -99, 99, 't'+str(i)+str(k)+str(i)+str(j+1)))
            #### constraint, e.g. t0001 = x00 - x01 ... t0002 = x00 - x02
            constraint_t_j.append(
                solver.Add(
                    constraint_var_t_j[j-k]
                    - objective_vars[i][k]
                    + objective_vars[i][j+1]
                    == 0,
                    't'+str(i)+str(k)+str(i)+str(j+1)))
            #print("Constraint: " + constraint_var_t_j[j-k].name() + ' - ' + objective_vars[i][k].name()
            #        + ' + ' + objective_vars[i][j+1].name() + ' = ' + ' 0 ')
        constraint_var_t_i.append(constraint_var_t_j)
        constraint_t_i.append(constraint_t_j)
    constraint_var_t_iforallj.append(constraint_var_t_i)
    constraint_t_iforallj.append(constraint_t_i)

### absolute value constraints, part 2
constraint_var_p_iforallj = []
constraint_var_n_iforallj = []
constraint_var_z_iforallj = []
constraint_var_y_iforallj = []
for row in constraint_var_t_iforallj:
    constraint_var_p_i = []
    constraint_var_n_i = []
    constraint_var_z_i = []
    constraint_var_y_i = []
    for column in row:
        constraint_var_p_j = []
        constraint_var_n_j = []
        constraint_var_z_j = []
        constraint_var_y_j = []
        for variable_t in column:
            constraint_var_p_j.append(
                solver.IntVar(
                    0, 99, 'p'+variable_t.name()[1:5]))
            constraint_var_n_j.append(
                solver.IntVar(
                    0, 99, 'n'+variable_t.name()[1:5]))
            constraint_var_z_j.append(
                solver.IntVar(
                    1, 99, 'z'+variable_t.name()[1:5])) # Note that z must be greater than or equal one
            constraint_var_y_j.append(
                solver.BoolVar(
                    'y'+variable_t.name()[1:5]))
        constraint_var_p_i.append(constraint_var_p_j)
        constraint_var_n_i.append(constraint_var_n_j)
        constraint_var_z_i.append(constraint_var_z_j)
        constraint_var_y_i.append(constraint_var_y_j)
    constraint_var_p_iforallj.append(constraint_var_p_i)
    constraint_var_n_iforallj.append(constraint_var_n_i)
    constraint_var_z_iforallj.append(constraint_var_z_i)
    constraint_var_y_iforallj.append(constraint_var_y_i)

### absolute value constraints, part 3
constraint_tpn_iforallj = []
constraint_zpn_iforallj = []
constraint_yp_iforallj = []
constraint_yn_iforallj = []
for i in range(0, constraint_var_t_iforallj.__len__()):
    constraint_tpn_i = []
    constraint_zpn_i = []
    constraint_yp_i = []
    constraint_yn_i = []
    for j in range(0, constraint_var_t_iforallj[i].__len__()):
        constraint_tpn_j = []
        constraint_zpn_j = []
        constraint_yp_j = []
        constraint_yn_j = []
        for k in range(0, constraint_var_t_iforallj[i][j].__len__()):
            constraint_tpn_j.append(
                solver.Add(
                    constraint_var_t_iforallj[i][j][k]
                    - constraint_var_p_iforallj[i][j][k]
                    + constraint_var_n_iforallj[i][j][k]
                    == 0,
                    'tpn'+constraint_var_t_iforallj[i][j][k].name()[1:5]))
            constraint_zpn_j.append(
                solver.Add(
                    constraint_var_z_iforallj[i][j][k]
                    - constraint_var_p_iforallj[i][j][k]
                    - constraint_var_n_iforallj[i][j][k]
                    == 0,
                    'zpn'+constraint_var_z_iforallj[i][j][k].name()[1:5]))
            constraint_yp_j.append(
                solver.Add(
                    constraint_var_p_iforallj[i][j][k]
                    - 99*constraint_var_y_iforallj[i][j][k]
                    <= 0,
                    'yp'+constraint_var_p_iforallj[i][j][k].name()[1:5]))
            constraint_yn_j.append(
                solver.Add(
                    constraint_var_n_iforallj[i][j][k]
                    + 99*constraint_var_y_iforallj[i][j][k]
                    <= 99,
                    'yn' + constraint_var_n_iforallj[i][j][k].name()[1:5]))
        constraint_tpn_i.append(constraint_tpn_j)
        constraint_zpn_i.append(constraint_zpn_j)
        constraint_yp_i.append(constraint_yp_j)
        constraint_yn_i.append(constraint_yn_j)
    constraint_tpn_iforallj.append(constraint_tpn_i)
    constraint_zpn_iforallj.append(constraint_zpn_i)
    constraint_yp_iforallj.append(constraint_yp_i)
    constraint_yn_iforallj.append(constraint_yn_i)

# Solution
solver.SetTimeLimit(120000)
status = solver.Solve()
print(status)
solution_values = np.array([
    [objective_vars[i][j].solution_value() for j in range(0, 9)]
    for i in range(0, 9)
])
print(solution_values)

options = pywraplp.ModelExportOptions()
model_as_string = solver.ExportModelAsLpFormat(False)