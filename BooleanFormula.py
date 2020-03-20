from enum import Enum

class Operation(Enum):
    FALSUM = 0 # always false
    TAUTOLOGY = 1 # always true
    VARIABLE = 2 # variable
    NOT = 3
    AND = 4
    OR = 5
    IMPLICATION = 6


class BooleanFormula():
    def __init__(self, operation, sub_formulas=None):
        self.operation = operation
        self.sub_formulas = sub_formulas

    def solve(self, values):
        #:param values: a dictionary which maps names of variables to their value
        #:returns: true false value of the formula
        if self.operation == Operation.FALSUM: # in this case subformulas is default None
            return False
        elif self.operation == Operation.TAUTOLOGY:
            return True
        elif self.operation == Operation.VARIABLE: # in this case subformulas is a variable name
            return values[self.sub_formulas]
        elif self.operation == Operation.NOT: # in this case subformulas is only one formula
            return not self.sub_formulas.solve(values)
        elif self.operation == Operation.AND: # in this case subformulas is a list (or iterable struct.) of formulas
            return all(map(lambda t: t.solve(values)))
        elif self.operation == Operation.OR:
            return any(map(lambda t: t.solve(values)))
        elif self.operation == Operation.IMPLICATION: # in this case subformulas is a pair of two formulas
            return self.sub_formulas[1].solve(values) or not self.sub_formulas[0].solve(values)


