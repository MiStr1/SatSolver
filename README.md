# SatSolver

Sat solver for project in logika v računalništvu

## Usage

#### Creating formula

a = BooleanFormula(Operation.TAUTOLOGY)  ⊤

b = BooleanFormula(Operation.FALSUM)  ⊥

c = BooleanFormula(Operation.VARIABLE, "x")  x

d = BooleanFormula(Operation.NOT, a)  not ⊤

e = BooleanFormula(Operation.AND, [a,b,d])    ⊤ ∧ ⊥  ∧ ¬ ⊤

f = BooleanFormula(Operation.OR, [a,b])   ⊤ ∨ ⊥

f = BooleanFormula(Operation.IMPLICATION, [a,b])  ⊤ → ⊥

#### Printing formula

print(f.to_string())

⊤ → ⊥

#### Solving formula

a.solve()  -> True

b.solve() -> False

c.solve({"x": True}) -> True

c.solve({"x": False}) -> False

#### Simplifinig

from BooleanFormula import BooleanFormula as BF

from BooleanFormula import Operation as OP

f = BF(OP.OR, [BF(OP.AND, [BF(OP.TAUTOLOGY), BF(OP.NOT, BF(OP.VARIABLE, "x"))]), BF(OP.FALSUM)])

print(f.to_string())   
(⊤ ∧ ¬x) ∨ ⊥

f.simplify()

print(f.to_string())   
¬x

#### Tseytin kno form

f = BF(OP.OR, [BF(OP.AND, [BF(OP.TAUTOLOGY), BF(OP.NOT, BF(OP.VARIABLE, "x"))]), BF(OP.FALSUM)])

print(f.get_kno().to_string())

(i2) ∧ (i0 ∨ x) ∧ (¬i0 ∨ ¬x) ∧ (i0 ∨ ¬i1) ∧ (i1 ∨ ¬i0) ∧ (i2 ∨ ¬i1) ∧ (¬i2 ∨ i1)

f.simplify()
print(f.get_kno().to_string())

(i0) ∧ (i0 ∨ x) ∧ (¬i0 ∨ ¬x)

NOTE !!! Tseytin creates variables from 0 -> inf but they are in int type since all old variables
get converted to string there should be no clashing. 

