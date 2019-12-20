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
# board from <https://www.sudokuwiki.org/sudoku.htm>, "Gentle"
gentle_board = np.array([
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

initial_board = gentle_board

def moss(initial_board, max_solve_time=120000):
    # libraries
    from ortools.linear_solver import pywraplp
    import numpy as np
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

    # Set initial board constraints
    print("(3) Setting constraints...")
    constraint_initial = [[]] * 9
    for i in range(0, 9):
        for j in range(0, 9):
            if initial_board[i][j] != 0:
                constraint_initial[i].append(
                    solver.Add(
                        objective_vars[i][j] == initial_board[i][j],
                        'init_x'+str(i)+str(j)+'=='+str(initial_board[i][j])))
            else:
                constraint_initial[i].append(
                    'init_x'+str(i)+str(j)+'==NONE'
                )

    # Set constraint: sum of rows must equal 45
    constraint_rowsum = [[]] * 9
    for i in range(0, 9):
        constraint_rowsum[i] = solver.Add(
            sum(objective_vars[i]) == 45)

    # Set constraint: sum of columns must equal 45
    constraint_colsum = [[]] * 9
    for j in range(0, 9):
        constraint_colsum[j] = solver.Add(
            sum(objective_vars[:, j]) == 45)

    # Set constraint: t equals difference of objective value pairs row-wise (e.g. t0102 - x01 + x02 = 0)
    t_rows = []
    constraint_t_rows = []
    for i in range(0, 9):
        t_i = []
        constraint_t_i = []
        for k in range(0, 8):
            t_j = []
            constraint_t_j = []
            for j in range(0+k, 8):
                # one t for each unique objective variable x pair
                t_j.append(
                    solver.IntVar(
                        -99, 99, 't'+str(i)+str(k)+str(i)+str(j+1)))     # range of -99 to 99
                constraint_t_j.append(
                    solver.Add(     # e.g. t0001=x00-x01 ... t0002=x00-x02
                        t_j[j-k]
                        - objective_vars[i][k]
                        + objective_vars[i][j+1]
                        == 0,
                        't'+str(i)+str(k)+str(i)+str(j+1)))
                #print("Constraint: " + constraint_var_t_j[j-k].name() + ' - ' + objective_vars[i][k].name()
                #        + ' + ' + objective_vars[i][j+1].name() + ' = ' + ' 0 ')
            t_i.append(t_j)
            constraint_t_i.append(constraint_t_j)
        t_rows.append(t_i)
        constraint_t_rows.append(constraint_t_i)

    # Create constraint variables p, n, z, and y
    p_rows = []
    n_rows = []
    z_rows = []
    y_rows = []
    for row in t_rows:
        p_i = []
        n_i = []
        z_i = []
        y_i = []
        for column in row:
            p_j = []
            n_j = []
            z_j = []
            y_j = []
            for variable_t in column:
                p_j.append(
                    solver.IntVar(
                        0, 99, 'p'+variable_t.name()[1:5]))
                n_j.append(
                    solver.IntVar(
                        0, 99, 'n'+variable_t.name()[1:5]))
                z_j.append(
                    solver.IntVar(
                        1, 99, 'z'+variable_t.name()[1:5])) # Note that z must be greater than or equal one
                y_j.append(
                    solver.BoolVar(
                        'y'+variable_t.name()[1:5]))
            p_i.append(p_j)
            n_i.append(n_j)
            z_i.append(z_j)
            y_i.append(y_j)
        p_rows.append(p_i)
        n_rows.append(n_i)
        z_rows.append(z_i)
        y_rows.append(y_i)

    # Set constraints: z equal to the absolute value of objective variable pair differences (Big M formulation)
    constraint_tpn_rows = []     # t-p+n=0
    constraint_zpn_rows = []     # z-p-n=0     e.g. z is the absolute value of objective variable pair differences
    constraint_yp_rows = []      # p-99*y<=0   Big-M formulation, where M=99, to enforce either y=0 or p=0
    constraint_yn_rows = []      # n+99*y<=99  Big-M formulation, where M=99, to enforce either y=0 or p=0
    for i in range(0, t_rows.__len__()):
        constraint_tpn_i = []
        constraint_zpn_i = []
        constraint_yp_i = []
        constraint_yn_i = []
        for j in range(0, t_rows[i].__len__()):
            constraint_tpn_j = []
            constraint_zpn_j = []
            constraint_yp_j = []
            constraint_yn_j = []
            for k in range(0, t_rows[i][j].__len__()):
                constraint_tpn_j.append(
                    solver.Add(     # t-p+n=0
                        t_rows[i][j][k]
                        - p_rows[i][j][k]
                        + n_rows[i][j][k]
                        == 0,
                        'tpn'+t_rows[i][j][k].name()[1:5]))
                constraint_zpn_j.append(
                    solver.Add(     # z-p-n=0
                        z_rows[i][j][k]
                        - p_rows[i][j][k]
                        - n_rows[i][j][k]
                        == 0,
                        'zpn'+z_rows[i][j][k].name()[1:5]))
                constraint_yp_j.append(     # p-99*y<=0
                    solver.Add(
                        p_rows[i][j][k]
                        - 99*y_rows[i][j][k]
                        <= 0,
                        'yp'+p_rows[i][j][k].name()[1:5]))
                constraint_yn_j.append(     # n+99*y<=99
                    solver.Add(
                        n_rows[i][j][k]
                        + 99*y_rows[i][j][k]
                        <= 99,
                        'yn' + n_rows[i][j][k].name()[1:5]))
            constraint_tpn_i.append(constraint_tpn_j)
            constraint_zpn_i.append(constraint_zpn_j)
            constraint_yp_i.append(constraint_yp_j)
            constraint_yn_i.append(constraint_yn_j)
        constraint_tpn_rows.append(constraint_tpn_i)
        constraint_zpn_rows.append(constraint_zpn_i)
        constraint_yp_rows.append(constraint_yp_i)
        constraint_yn_rows.append(constraint_yn_i)

    # Set constraint: t equals difference of objective value pairs row-wise (e.g. t0102 - x01 + x02 = 0)
    t_cols = []
    constraint_t_cols = []
    for i in range(0, 9):
        t_x = []
        constraint_t_x = []
        for k in range(0, 8):
            t_y = []
            constraint_t_y = []
            for j in range(0 + k, 8):
                # one t for each unique objective variable x pair
                t_y.append(
                    solver.IntVar(
                        -99, 99, 't_'+str(k)+str(i)+str(j+1)+str(i)))  # range of -99 to 99
                constraint_t_y.append(
                    solver.Add(  # e.g. t0001=x00-x01 ... t0002=x00-x02
                        t_y[j-k]
                        - objective_vars[k][i]
                        + objective_vars[j+1][i]
                        == 0,
                        't_' + str(k) + str(i) + str(j+1) + str(i)))
                print("Constraint: " + t_y[j-k].name() + ' - ' + objective_vars[k][i].name()
                        + ' + ' + objective_vars[j+1][i].name() + ' = ' + ' 0 ')
            t_x.append(t_y)
            constraint_t_x.append(constraint_t_y)
        t_cols.append(t_x)
        constraint_t_cols.append(constraint_t_x)

    # Create constraint variables p, n, z, and y
    p_cols = []
    n_cols = []
    z_cols = []
    y_cols = []
    for row in t_cols:
        p_x = []
        n_x = []
        z_x = []
        y_x = []
        for column in row:
            p_y = []
            n_y = []
            z_y = []
            y_y = []
            for variable_t in column:
                p_y.append(
                    solver.IntVar(
                        0, 99, 'p_' + variable_t.name()[2:6]))
                n_y.append(
                    solver.IntVar(
                        0, 99, 'n_' + variable_t.name()[2:6]))
                z_y.append(
                    solver.IntVar(
                        1, 99, 'z_' + variable_t.name()[2:6]))  # Note that z must be greater than or equal one
                y_y.append(
                    solver.BoolVar(
                        'y_' + variable_t.name()[2:6]))
            p_x.append(p_y)
            n_x.append(n_y)
            z_x.append(z_y)
            y_x.append(y_y)
        p_cols.append(p_x)
        n_cols.append(n_x)
        z_cols.append(z_x)
        y_cols.append(y_x)

    # Set constraints: z equal to the absolute value of objective variable pair differences (Big M formulation)
    constraint_tpn_cols = []  # t-p+n=0
    constraint_zpn_cols = []  # z-p-n=0     e.g. z is the absolute value of objective variable pair differences
    constraint_yp_cols = []  # p-99*y<=0   Big-M formulation, where M=99, to enforce either y=0 or p=0
    constraint_yn_cols = []  # n+99*y<=99  Big-M formulation, where M=99, to enforce either y=0 or p=0
    for i in range(0, t_cols.__len__()):
        constraint_tpn_x = []
        constraint_zpn_x = []
        constraint_yp_x = []
        constraint_yn_x = []
        for j in range(0, t_cols[i].__len__()):
            constraint_tpn_y = []
            constraint_zpn_y = []
            constraint_yp_y = []
            constraint_yn_y = []
            for k in range(0, t_cols[i][j].__len__()):
                constraint_tpn_y.append(
                    solver.Add(  # t-p+n=0
                        t_cols[i][j][k]
                        - p_cols[i][j][k]
                        + n_cols[i][j][k]
                        == 0,
                        'tpn_' + t_cols[i][j][k].name()[2:6]))
                constraint_zpn_y.append(
                    solver.Add(  # z-p-n=0
                        z_cols[i][j][k]
                        - p_cols[i][j][k]
                        - n_cols[i][j][k]
                        == 0,
                        'zpn_' + z_cols[i][j][k].name()[2:6]))
                constraint_yp_y.append(  # p-99*y<=0
                    solver.Add(
                        p_cols[i][j][k]
                        - 99 * y_cols[i][j][k]
                        <= 0,
                        'yp_' + p_cols[i][j][k].name()[2:6]))
                constraint_yn_y.append(  # n+99*y<=99
                    solver.Add(
                        n_cols[i][j][k]
                        + 99 * y_cols[i][j][k]
                        <= 99,
                        'yn_' + n_cols[i][j][k].name()[2:6]))
            constraint_tpn_x.append(constraint_tpn_y)
            constraint_zpn_x.append(constraint_zpn_y)
            constraint_yp_x.append(constraint_yp_y)
            constraint_yn_x.append(constraint_yn_y)
        constraint_tpn_cols.append(constraint_tpn_x)
        constraint_zpn_cols.append(constraint_zpn_x)
        constraint_yp_cols.append(constraint_yp_x)
        constraint_yn_cols.append(constraint_yn_x)

    # Solution
    solver.SetTimeLimit(max_solve_time)
    status = solver.Solve()
    print(status)
    if status == 0:
        print("Success!")
    if status != 0:
        print("Solve failed, see status for details.")
    solution_values = np.array([
        [objective_vars[i][j].solution_value() for j in range(0, 9)]
        for i in range(0, 9)
    ])
    model_as_string = solver.ExportModelAsLpFormat(False)

    # Output
    return({
        "status": status,
        "solution_values": solution_values,
        "model_lp_file": model_as_string,
        "solver_object": solver
    })