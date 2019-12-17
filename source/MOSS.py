# MOSS: Mathematical Optimization Sudoku Solver
# Ryan Chien
# 12/16/2019
# The objective of this code is to use an two-index integer linear program to solve Sudoku
# The more common ILP method of solving Sudoku is with three indicies: https://towardsdatascience.com/using-integer-linear-programming-to-solve-sudoku-puzzles-15e9d2a70baa

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

initial_board = np.array([
    [0, 0, 0, 7, 0, 4, 0, 0, 5],
    [0, 2, 0, 0, 1, 0, 0, 7, 0],
    [0, 0, 0, 0, 8, 0, 0, 0, 2],
    [0, 9, 0, 0, 0, 6, 2, 5, 0],
    [6, 0, 0, 0, 7, 0, 0, 0, 8],
    [0, 5, 3, 2, 0, 0, 0, 1, 0],
    [4, 0, 0, 0, 9, 0, 0, 0, 0],
    [0, 3, 0, 0, 6, 0, 0, 9, 0],
    [2, 0, 0, 4, 0, 7, 0, 0, 0]
])

initial_board = np.array([
    [0, 9, 3, 0, 0, 4, 5, 6, 0],
    [0, 6, 0, 0, 0, 3, 1, 4, 0],
    [0, 0, 4, 6, 0, 8, 3, 0, 9],
    [9, 8, 1, 3, 4, 5, 0, 0, 0],
    [3, 4, 7, 2, 8, 6, 9, 5, 1],
    [6, 5, 2, 0, 7, 0, 4, 8, 3],
    [4, 0, 6, 0, 0, 2, 8, 9, 0],
    [0, 0, 0, 4, 0, 0, 0, 1, 0],
    [0, 2, 9, 8, 0, 0, 0, 3, 4]
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

## Absolute Value Constraints, j for all i
### part 4
constraint_var_u_jforalli = []
constraint_u_jforalli = []
for i in range(0, 9):
    constraint_var_u_i = []
    constraint_u_i = []
    for k in range(0, 8):
        constraint_var_u_j = []
        constraint_u_j = []
        for j in range(0+k, 8):
            #### define variable t, integer, range of -99 to 99
            #### one t for each unique objective variable x pair
            constraint_var_u_j.append(
                solver.IntVar(
                    -99, 99, 'u'+str(j)+str(i)+str(j+1)+str(i)))
            #### constraint, e.g. t0001 = x00 - x01 ... t0002 = x00 - x02
            constraint_u_j.append(
                solver.Add(
                    constraint_var_u_j[j-k]
                    - objective_vars[k][i]
                    + objective_vars[j+1][i]
                    == 0,
                    'u'+str(i)+str(k)+str(i)+str(j+1)))
            print("Constraint: " + constraint_var_u_j[j-k].name() + ' - ' + objective_vars[k][i].name()
                    + ' + ' + objective_vars[j+1][i].name() + ' = ' + ' 0 ')
        constraint_var_u_i.append(constraint_var_u_j)
        constraint_u_i.append(constraint_u_j)
    constraint_var_u_jforalli.append(constraint_var_u_i)
    constraint_u_jforalli.append(constraint_u_i)

### part 5
constraint_var_q_jforalli = []
constraint_var_o_jforalli = []
constraint_var_a_jforalli = []
constraint_var_b_jforalli = []
for row in constraint_var_t_iforallj:
    constraint_var_q_i = []
    constraint_var_o_i = []
    constraint_var_a_i = []
    constraint_var_b_i = []
    for column in row:
        constraint_var_q_j = []
        constraint_var_o_j = []
        constraint_var_a_j = []
        constraint_var_b_j = []
        for variable_t in column:
            constraint_var_q_j.append(
                solver.IntVar(
                    0, 99, 'q'+variable_t.name()[1:5]))
            constraint_var_o_j.append(
                solver.IntVar(
                    0, 99, 'o'+variable_t.name()[1:5]))
            constraint_var_a_j.append(
                solver.IntVar(
                    1, 99, 'a'+variable_t.name()[1:5])) # Note that z must be greater than or equal one
            constraint_var_b_j.append(
                solver.BoolVar(
                    'b'+variable_t.name()[1:5]))
        constraint_var_q_i.append(constraint_var_q_j)
        constraint_var_o_i.append(constraint_var_o_j)
        constraint_var_a_i.append(constraint_var_a_j)
        constraint_var_b_i.append(constraint_var_b_j)
    constraint_var_q_jforalli.append(constraint_var_q_i)
    constraint_var_o_jforalli.append(constraint_var_o_i)
    constraint_var_a_jforalli.append(constraint_var_a_i)
    constraint_var_b_jforalli.append(constraint_var_b_i)

### absolute value constraints, part 6
constraint_upn_iforallj = []
constraint_apn_iforallj = []
constraint_bp_iforallj = []
constraint_bn_iforallj = []
for i in range(0, constraint_var_u_jforalli.__len__()):
    constraint_upn_i = []
    constraint_apn_i = []
    constraint_bp_i = []
    constraint_bn_i = []
    for j in range(0, constraint_var_u_jforalli[i].__len__()):
        constraint_upn_j = []
        constraint_apn_j = []
        constraint_bp_j = []
        constraint_bn_j = []
        for k in range(0, constraint_var_u_jforalli[i][j].__len__()):
            constraint_upn_j.append(
                solver.Add(
                    constraint_var_u_jforalli[i][j][k]
                    - constraint_var_q_jforalli[i][j][k]
                    + constraint_var_o_jforalli[i][j][k]
                    == 0,
                    'upn'+constraint_var_u_jforalli[i][j][k].name()[1:5]))
            constraint_apn_j.append(
                solver.Add(
                    constraint_var_a_jforalli[i][j][k]
                    - constraint_var_q_jforalli[i][j][k]
                    - constraint_var_o_jforalli[i][j][k]
                    == 0,
                    'apn'+constraint_var_a_jforalli[i][j][k].name()[1:5]))
            constraint_bp_j.append(
                solver.Add(
                    constraint_var_b_jforalli[i][j][k]
                    - 99*constraint_var_a_jforalli[i][j][k]
                    <= 0,
                    'bp'+constraint_var_q_jforalli[i][j][k].name()[1:5]))
            constraint_bn_j.append(
                solver.Add(
                    constraint_var_o_jforalli[i][j][k]
                    + 99*constraint_var_b_jforalli[i][j][k]
                    <= 99,
                    'bn' + constraint_var_o_jforalli[i][j][k].name()[1:5]))
        constraint_upn_i.append(constraint_upn_j)
        constraint_apn_i.append(constraint_apn_j)
        constraint_bp_i.append(constraint_bp_j)
        constraint_bn_i.append(constraint_bn_j)
    constraint_upn_iforallj.append(constraint_upn_i)
    constraint_apn_iforallj.append(constraint_apn_i)
    constraint_bp_iforallj.append(constraint_bp_i)
    constraint_bn_iforallj.append(constraint_bn_i)

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