# SatSolver

Sat solver for project in logika v računalništvu

## Usage

#### Creating formula

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

c.solve({"x": True}) -> True

c.solve({"x": False}) -> False

#### Simplifinig

from BooleanFormula import *

f = OR([AND([TAUTOLOGY(), NOT(VARIABLE("x"))]), FALSUM()])

print(f.to_string())   
(⊤ ∧ ¬x) ∨ ⊥

f.simplify()

print(f.to_string())   
¬x

#### Tseytin kno form

f = OR([AND([TAUTOLOGY(), NOT(VARIABLE("x"))]), FALSUM()])

print(f.get_kno().to_string())

(i2) ∧ (i0 ∨ x) ∧ (¬i0 ∨ ¬x) ∧ (i0 ∨ ¬i1) ∧ (i1 ∨ ¬i0) ∧ (i2 ∨ ¬i1) ∧ (¬i2 ∨ i1)

f.simplify()
print(f.get_kno().to_string())

(i0) ∧ (i0 ∨ x) ∧ (¬i0 ∨ ¬x)

NOTE !!! Tseytin creates variables from 0 -> inf but they are in int type since all old variables
get converted to string there should be no clashing. 
