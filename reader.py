from KnoFormula import *
from DPLL_simple import DPLL

input_file = "sudoku_mini.txt"
output_file = "output_test.txt"

# read input file
with open(input_file, mode='r') as input_data:
    lines = input_data.readlines()
    clause_list = []

    for line in lines:
        elements = line.split(" ")

        # skip comments at the start of the input file
        if elements[0] != "c":
            if elements[0] == "p":
                # save numbers just in case
                n_vars = int(elements[2])
                n_clauses = int(elements[3])
            else:
                # write and save the clause
                clause = []
                # the last two elements are "0", "\n" so we skip them
                for el in elements[:-2]:
                    clause.append(int(el))
                clause_list.append(clause)

    cnf_formula = KnoFormula(clause_list)

vars = set(range(1, n_vars+1))
# vars = tuple(vars)

solution = DPLL(cnf_formula, vars)

# write results in output file
with open(output_file, mode="w") as out:
    for i in range(n_vars):
        if solution[i][1] is True:
            out.write(str(solution[i][0]) + " ")
        else:
            out.write("-" + str(solution[i][0]) + " ")
