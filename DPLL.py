from BooleanFormula import Operation, TAUTOLOGY
from random import choice


def pure_var(bool_form):
    """
    :param bool_form: boolean formula element from AND in kno
    :return: if element is a pure variable or its negation it returns the value necceseary exc: ("x", True)
    for the formula to be True otherwise it returns None
    """
    if bool_form.operation == Operation.VARIABLE:
        return bool_form.sub_formulas, True
    elif bool_form.operation == Operation.NOT and bool_form.sub_formulas.operation == Operation.VARIABLE:
        return bool_form.sub_formulas.sub_formulas, False


def first_step_DPLL(bool_form):
    """
    :param bool_form: kno formula
    :return: equation with solved pure variables and values of the pure variables
    """
    if bool_form.operation == Operation.OR: # only one OR in AND
        return bool_form, []
    if bool_form.operation == Operation.VARIABLE: # only one variable in AND
        return TAUTOLOGY(), [(bool_form.sub_formulas, True)]
    if bool_form.operation == Operation.NOT: # only one NOT in AND
        return TAUTOLOGY(), [(bool_form.sub_formulas.sub_formulas, False)]
    if bool_form.operation == Operation.FALSUM or bool_form.operation == Operation.TAUTOLOGY: # only one True or False
        return bool_form, []
    pure_vars = map(pure_var, bool_form.sub_formulas)  # get all pure elements
    pure_vars = list(filter(lambda t: t is not None, pure_vars)) #remove all Nones returned from the function
    new_formula = bool_form.partial_solve(dict(pure_vars)) # partially solve
    new_formula.simplify_kno() # simplify
    return new_formula, list(pure_vars)


def DPLL(bool_form):
    bool_form.simplify_kno() # simplify
    bool_form, equ = first_step_DPLL(bool_form) # solve pure variables
    if bool_form.operation == Operation.TAUTOLOGY: # we have finished the search
        return equ
    if bool_form.operation == Operation.FALSUM: # current path doesn't have solutions
        return None
    var = choice(bool_form.get_variables()) # get random variable from formula and try giving it True or False
    tru = bool_form.partial_solve({var: True})
    solv = DPLL(tru)
    if solv is not None:
        return equ + solv + [(var, True)]

    fal = bool_form.partial_solve({var: False})
    solv = DPLL(fal)
    if solv is not None:
        return equ + solv + [(var, False)]
    return None

