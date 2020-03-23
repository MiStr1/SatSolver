from BooleanFormula import Operation, TAUTOLOGY
from random import choice


def pure_var(bool_form):
    if bool_form.operation == Operation.VARIABLE:
        return bool_form.sub_formulas, True
    elif bool_form.operation == Operation.NOT and bool_form.sub_formulas.operation == Operation.VARIABLE:
        return bool_form.sub_formulas.sub_formulas, False


def first_step_DPLL(bool_form):
    if bool_form.operation == Operation.OR:
        return bool_form, []
    if bool_form.operation == Operation.VARIABLE:
        return TAUTOLOGY(), [(bool_form.sub_formulas, True)]
    if bool_form.operation == Operation.NOT:
        return TAUTOLOGY(), [(bool_form.sub_formulas.sub_formulas, False)]
    if bool_form.operation == Operation.FALSUM or bool_form.operation == Operation.TAUTOLOGY:
        return bool_form, []
    pure_vars = map(pure_var, bool_form.sub_formulas)
    pure_vars = list(filter(lambda t: t is not None, pure_vars))
    new_formula = bool_form.partial_solve(dict(pure_vars))
    new_formula.simplify_kno()
    return new_formula, list(pure_vars)


def DPLL(bool_form):
    bool_form.simplify_kno()
    bool_form, equ = first_step_DPLL(bool_form)
    if bool_form.operation == Operation.TAUTOLOGY:
        return equ
    if bool_form.operation == Operation.FALSUM:
        return None
    var = choice(bool_form.get_variables())
    tru = bool_form.partial_solve({var: True})
    solv = DPLL(tru)
    if solv is not None:
        return equ + solv + [(var, True)]

    fal = bool_form.partial_solve({var: False})
    solv = DPLL(fal)
    if solv is not None:
        return equ + solv + [(var, False)]
    return None

