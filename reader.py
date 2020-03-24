from BooleanFormula import *
from DPLL_simple import DPLL

input_file = "sudoku_mini.txt"
output_file = "test.txt"


with open(input_file, mode='r') as input_data:
    lines = input_data.readlines()
    clause_list = []

    for line in lines:
        elements = line.split(" ")

        # skip comments at the start of the input file
        if elements[0] != "c":
            if elements[0] == "p":
                # save numbers just in case
                n_vars = elements[2]
                n_clauses = elements[3]
            else:
                # write and save the clause
                clause = []
                for el in elements[:-2]:  # the last two elements are "0", "\n"
                    if "\n" not in elements:
                        print(elements)
                    # check if negated
                    if el[0] == "-":
                        clause.append(NOT(VARIABLE(el[1:])))
                    else:
                        clause.append(VARIABLE(el))
                clause_list.append(OR(clause))

    cnf_formula = AND(clause_list)


#solution = DPLL(cnf_formula)
