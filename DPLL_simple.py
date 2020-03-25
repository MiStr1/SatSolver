from random import choice
from collections import defaultdict
from functools import reduce


def default_d():
    # default value used for dictionary in second step
    return [False, False]

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


def second_step_aux(a,b):
    if b > 0:
        a[b][0] = True
    else:
        a[-1*b][1] = True
    return a


def second_step_DPLL(kno_form):
    # ddict saves if certain variable is found in negation or in positive form [found in +, found in -] bool
    ddict = reduce(second_step_aux, reduce(lambda a,b : a+b, kno_form.formula, []), defaultdict(default_d))
    pure_vars = reduce(lambda a,b: a+[(b[0],b[1][0])] if (b[1][0] ^ b[1][1]) else a, ddict.items(), [])
    new_formula = kno_form.partial_solve(dict(pure_vars))
    return new_formula, pure_vars


def DPLL(kno_form):
    """
    :param kno_form: kno formula
    :return: list of tuples assigning value to the variables if there is no solution None is returned
    """
    equ = []
    while True:
        kno_form, eq = first_step_DPLL(kno_form)
        if not eq:
            break
        equ += eq
    # kno_form, eq = second_step_DPLL(kno_form) doesn't help and only duplicates runtime
    # equ += eq
    if [] in kno_form.formula:  # current path doesn't have solutions
        return None
    if len(kno_form.formula) == 0:  # we have finished the search
        return equ
    var = choice(kno_form.get_vars())  # get random variable from formula and try giving it True or False
    tru = kno_form.partial_solve({var: True})
    solv = DPLL(tru)
    if solv is not None:
        return equ + solv + [(var, True)]
    fal = kno_form.partial_solve({var: False})
    solv = DPLL(fal)
    if solv is not None:
        return equ + solv + [(var, False)]
    return None
