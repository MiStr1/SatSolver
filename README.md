# SatSolver

Sat solver for project in logika v računalništvu

# Usage

## BooleanFormula

#### Creating formula

from BooleanFormula import *

a = TAUTOLOGY()  ⊤

b = FALSUM()  ⊥

c = VARIABLE("x")  x

d = NOT(a)  ¬ ⊤

e = AND([a,b,d])    ⊤ ∧ ⊥  ∧ ¬ ⊤

f = OR([a,b])   ⊤ ∨ ⊥

g = IMPLICATION(a,b)  ⊤ → ⊥

h = AND([a,b,c,d,e,f,g])

#### Printing formula

print(h.to_string())

⊤ ∧ ⊥ ∧ x ∧ ¬⊤ ∧ (⊤ ∧ ⊥ ∧ ¬⊤) ∧ (⊤ ∨ ⊥) ∧ (⊤ → ⊥)

#### Solving formula

a.solve()  -> True

b.solve() -> False

c.solve() -> ValueMissing exception

c.solve(default_true=True) -> True

c.solve({"x": True}) -> True

c.solve({"x": False}) -> False

#### Partial solving

a = AND([VARIABLE("x"), VARIABLE("y")])

b = a.partial_solve({"x": True})

print(b.to_string())

⊤ ∧ y

#### Simplifinig

print(b.to_string())   
⊤ ∧ y

b.simplify()

print(b.to_string())   
y

#### Tseytin kno form

f = OR([AND([TAUTOLOGY(), NOT(VARIABLE("x"))]), FALSUM()])

print(f.get_kno().to_string())

(i2) ∧ (i0 ∨ x) ∧ (¬i0 ∨ ¬x) ∧ (i0 ∨ ¬i1) ∧ (i1 ∨ ¬i0) ∧ (i2 ∨ ¬i1) ∧ (¬i2 ∨ i1)

f.simplify()
print(f.get_kno().to_string())

(i0) ∧ (i0 ∨ x) ∧ (¬i0 ∨ ¬x)

NOTE !!! Tseytin creates variables from 0 -> inf but they are in int type since all old variables
get converted to string there should be no clashing. 

#### Check if formula is kno

f = OR([AND([TAUTOLOGY(), NOT(VARIABLE("x"))]), FALSUM()])

f.is_kno() False

f.get_kno().is_kno() True

## DPLL

from DPLL import DPLL

from BooleanFormula import *

f = OR([AND([TAUTOLOGY(), NOT(VARIABLE("x"))]), FALSUM()])

f.simplify()

k = f.get_kno()

from DPLL import DPLL

solv = DPLL(k)

[(0, True), ('x', False)]

k.solve(dict(solv)) -> True
