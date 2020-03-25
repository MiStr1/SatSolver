from functools import reduce


def solve_or(clause, values):
    out = []
    for f in clause:
        tmp = abs(f)
        if tmp in values:
            if values[tmp] ^ (f < 0):  # if True whole statement is True remove it
                return []
            # if False don't add it
        else:
            out.append(f)
    return [out]  # if out is empty this means there is no solutions


class KnoFormula:
    """
    has one parameter formula which is a recursive list of depth 2 first depth is an AND clause and second is OR
    variables are numbers and their negations are negative numbers.
    """

    def __init__(self, formula):
        self.formula = formula

    def solve(self, values=None):
        if values is None:
            values = dict()
        return all(map(lambda t:
                       any(map(lambda u: values[abs(u)] ^ (u < 0), t)), self.formula))

    def partial_solve(self, values):
        return KnoFormula(list(reduce(lambda a, b: a + solve_or(b, values), self.formula, [])))

    def to_string(self):
        return " ∧ ".join(map(lambda t: "( " + " ∨ ".join(map(str, t)) + " )", self.formula))
