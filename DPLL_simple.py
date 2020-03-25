from random import sample
from copy import copy


def first_step_DPLL(kno_form):
    """
    :param kno_form: kno formula
    :return: equation with solved pure variables and values of the pure variables
    """
    pure_vars = map(lambda t: (abs(t[0]), t[0] > 0) if (len(t) == 1) else None,
                    kno_form.formula)  # get all pure elements
    pure_vars = dict(list(filter(lambda t: t is not None, pure_vars)))  # remove all Nones returned from the function
    new_formula = kno_form.partial_solve(pure_vars)  # partially solve
    return new_formula, [(k, v) for k, v in pure_vars.items()]


def DPLL(kno_form, vars):
    """
    :param kno_form: kno formula
    :param vars: set of variables used in formula
    :return: list of tuples assigning value to the variables if there is no solution None is returned
    """
    equ = []
    while True:
        kno_form, eq = first_step_DPLL(kno_form)
        if not eq:
            break
        equ += eq
    if [] in kno_form.formula:  # current path doesn't have solutions
        return None
    for e in equ:
        vars.remove(e[0])
    print(repr(kno_form.formula))
    print(len(kno_form.formula))
    print("break")
    if len(kno_form.formula) == 0:  # we have finished the search
        for v in list(vars):
            equ.append((v, False))  # assigning leftover vars
        return equ
    var = sample(vars, 1)[0]  # get random variable from formula and try giving it True or False
    vars.remove(var)
    tru = kno_form.partial_solve({var: True})
    solv = DPLL(tru, vars)
    if solv is not None:
        return equ + solv + [(var, True)]
    fal = kno_form.partial_solve({var: False})
    solv = DPLL(fal, vars)
    if solv is not None:
        return equ + solv + [(var, False)]
    for e in equ:
        vars.add(e[0])
    vars.add(var)
    return None
