# SatSolver

Sat solver for project in logika v računalništvu

# Usage

## main

Run sat solver: `python main.py {path/to/input} {path/to/output}`

Example CNF formula is of 28-queens problem stored in n-queens/n-queens-n28.txt

## Compare solutions

Run script to compare solutions: `python compare_solutions.py {path/to/file1} {path/to/file2}`
Returns `True` if solutions are the same and `False` if they are not

## KnoFormula

`from KnoFormula import KnoFormula`

`a = KnoFormula([[-1],[1,2],[-2,3]])`

`a.to_string()`

`( -1 ) ∧ ( 1 ∨ 2 ) ∧ ( -2 ∨ 3 )`

`a.solve({1:False, 2: True, 3:True}) -> True`

`a.partial_solve({1: False}).to_string() `

`( 2 ) ∧ ( -2 ∨ 3 )`


## DPLL_simple

`from DPLL_simple import DPLL`

`DPLL(a,{1,2,3})`

`[(1, False), (2, True), (3, True)]`
