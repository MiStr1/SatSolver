# SatSolver

Sat solver for project in logika v računalništvu

## Usage

#### Creating formula

a = BooleanFormula(Operation.TAUTOLOGY)  ⊤

b = BooleanFormula(Operation.FALSUM)  ⊥

c = BooleanFormula(Operation.VARIABLE, "x")  x

d = BooleanFormula(Operation.NOT, a)  not ⊤

e = BooleanFormula(Operation.AND, [a,b,d])    ⊤ ∧ ⊥  ∧ not ⊤

f = BooleanFormula(Operation.OR, [a,b])   ⊤ ∨ ⊥

f = BooleanFormula(Operation.IMPLICATION, [a,b])  ⊤ → ⊥

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

(0 ∨ ¬x) ∧ (¬0 ∨ x) ∧ (0 ∨ ¬1) ∧ (1 ∨ ¬0) ∧ (2 ∨ ¬1) ∧ (¬2 ∨ 1)

f.simplify()
print(f.get_kno().to_string())

(0 ∨ ¬x) ∧ (¬0 ∨ x)

NOTE !!! Tseytin creates variables from 0 -> inf do not use your variables with numeric name.

