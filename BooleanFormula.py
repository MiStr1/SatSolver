from enum import Enum
from functools import reduce

class Operation(Enum):
    FALSUM = 0 # always false
    TAUTOLOGY = 1 # always true
    VARIABLE = 2 # variable
    NOT = 3
    AND = 4
    OR = 5
    IMPLICATION = 6


class ValueMissing(Exception):
    pass


class BooleanFormula:
    """
    Class BooleanFormula represents a formula with bool variables and operations
    operation is an enum which tells the operation
    sub_formulas is data for the operation
    for FALSUM, TAUTOLOGY it is None for VARIABLE it is the name of the variable for not it is a
    single sub_formula, for other three it is a list of sub_formulas
    """
    def __init__(self, operation, sub_formulas=None, keep_int=False):
        self.operation = operation
        self.sub_formulas = sub_formulas
        if self.operation == Operation.VARIABLE and not keep_int:
            self.sub_formulas = str(self.sub_formulas)

    def get_variables(self):
        # returns all variables (there can be doubles)
        if self.operation == Operation.AND or self.operation == Operation.OR or self.operation == Operation.IMPLICATION:
            return reduce(lambda a,b: a+b.get_variables(), self.sub_formulas, [])
        if self.operation == Operation.NOT:
            return self.sub_formulas.get_variables()
        if self.operation == Operation.VARIABLE:
            return [self.sub_formulas]
        return []

    def to_string(self, top=True):
        # returns formula in a string form
        # top means we are at the top layer of formula
        conn = " wrong OP "
        if self.operation == Operation.FALSUM:
            return "⊥"
        elif self.operation == Operation.TAUTOLOGY:
            return "⊤"
        elif self.operation == Operation.VARIABLE:
            if isinstance(self.sub_formulas, int):
                return "i"+str(self.sub_formulas)
            return self.sub_formulas
        elif self.operation == Operation.NOT:
            return "¬" + self.sub_formulas.to_string(False)
        elif self.operation == Operation.AND:
            conn = " ∧ "
        elif self.operation == Operation.OR:
            conn = " ∨ "
        elif self.operation == Operation.IMPLICATION:
            conn = " → "
        out = conn.join(map(lambda t: t.to_string(False), self.sub_formulas))
        if not top:
            out = "(" + out + ")"
        return out

    def solve(self, values=None):
        """
        :param values: a dictionary which maps names of variables to their value
        :returns: True False value of the formula
        """
        if values is None:
            values = {}
        if self.operation == Operation.FALSUM: # in this case subformulas is default None
            return False
        elif self.operation == Operation.TAUTOLOGY:
            return True
        elif self.operation == Operation.VARIABLE: # in this case subformulas is a variable name
            if self.sub_formulas in values:
                return values[self.sub_formulas]
            else:
                raise ValueMissing
        elif self.operation == Operation.NOT: # in this case subformulas is only one formula
            return not self.sub_formulas.solve(values)
        elif self.operation == Operation.AND: # in this case subformulas is a list (or iterable struct.) of formulas
            return all(map(lambda t: t.solve(values), self.sub_formulas))
        elif self.operation == Operation.OR:
            return any(map(lambda t: t.solve(values), self.sub_formulas))
        elif self.operation == Operation.IMPLICATION: # in this case subformulas is a pair of two formulas
            return self.sub_formulas[1].solve(values) or not self.sub_formulas[0].solve(values)

    ####################################################
    # cleaning functions used to simplify the formula  #
    ####################################################
    def remove_empty(self):
        # if Ands or Ors have one or less element remove them (returns true if there were any changes)
        if self.operation == Operation.NOT:
            return self.sub_formulas.remove_empty()
        elif self.operation == Operation.IMPLICATION:
            return self.sub_formulas[0].remove_empty() or self.sub_formulas[1].remove_empty()
        elif self.operation == Operation.OR or self.operation == Operation.AND:
            if len(self.sub_formulas) > 1:
                # recursively call subformulas
                return any(map(lambda t: t.remove_empty(), self.sub_formulas))
            elif len(self.sub_formulas) == 1:
                # remove and or or
                self.operation = self.sub_formulas[0].operation
                self.sub_formulas = self.sub_formulas[0].sub_formulas
                return True
            # and or or to constant
            if self.operation == Operation.AND:
                self.operation = Operation.TAUTOLOGY
            elif self.operation == Operation.OR:
                self.operation = Operation.FALSUM
            self.sub_formulas = None
            return True

        return False

    def remove_constants(self):
        # removes unnecessary TATUTOLOGIES of FALSUMS (returns true if there were any changes)

        if self.operation == Operation.NOT:
            # first call the function recursively and check if there were changes
            change = self.sub_formulas.remove_constants()
            if self.sub_formulas.operation == Operation.FALSUM:
                self.operation = Operation.TAUTOLOGY
                self.sub_formulas = None
                return True
            elif self.sub_formulas.operation == Operation.TAUTOLOGY:
                self.operation = Operation.FALSUM
                self.sub_formulas = None
                return True
            return change

        if self.operation == Operation.AND:
            # first call the function recursively and check if there were changes
            change = any(map(lambda t: t.remove_constants(), self.sub_formulas))
            # if FALSUM exists whole AND is False
            if any(map(lambda t: t.operation == Operation.FALSUM, self.sub_formulas)):
                self.operation = Operation.FALSUM
                self.sub_formulas = None
                return True
            # remove all TAUTOLOGIES since they don't change the operation
            start_len = len(self.sub_formulas)
            self.sub_formulas = list(filter(lambda t: t.operation != Operation.TAUTOLOGY, self.sub_formulas))
            return change or start_len != len(self.sub_formulas)

        if self.operation == Operation.OR:
            # first call the function recursively and check if there were changes
            change = any(map(lambda t: t.remove_constants(), self.sub_formulas))
            # if TAUTOLOGY exists whole OR is TRUE
            if any(map(lambda t: t.operation == Operation.TAUTOLOGY, self.sub_formulas)):
                self.operation = Operation.TAUTOLOGY
                self.sub_formulas = None
                return True
            # remove all FALSUMS since they don't change the operation
            start_len = len(self.sub_formulas)
            self.sub_formulas = list(filter(lambda t: t.operation != Operation.FALSUM, self.sub_formulas))
            return change or start_len != len(self.sub_formulas)

        if self.operation == Operation.IMPLICATION:
            # first call the function recursively and check if there were changes
            change = self.sub_formulas[0].remove_constants or self.sub_formulas[1].remove_constants
            if self.sub_formulas[0].operation == Operation.FALSUM or \
               self.sub_formulas[1].operation == Operation.TAUTOLOGY:
                self.operation = Operation.TAUTOLOGY
                self.sub_formulas = None
                return True
            return change

        return False

    def push_negations(self):
        # pushes negations to the bottom of the Formula (returns true if there were any changes)
        if self.operation in (Operation.AND, Operation.OR, Operation.IMPLICATION):
            return any(map(lambda t: t.push_negations(), self.sub_formulas))

        if self.operation == Operation.NOT:
            if self.sub_formulas.operation == Operation.NOT:
                # double negations remove both negations
                self.operation = self.sub_formulas.sub_formulas.operation
                self.sub_formulas = self.sub_formulas.sub_formulas.sub_formulas
                return self.push_negations()
            elif self.sub_formulas.operation == Operation.AND or self.sub_formulas.operation == Operation.OR:
                # de morgan
                op = self.sub_formulas.operation
                self.sub_formulas = list(map(lambda t: BooleanFormula(Operation.NOT, t), self.sub_formulas.sub_formulas))
                if op == Operation.AND:
                    self.operation = Operation.OR
                else:
                    self.operation = Operation.AND
                return any(map(lambda t: t.push_negations, self.sub_formulas))
            elif self.sub_formulas.operation == Operation.IMPLICATION:
                self.sub_formulas = list(self.sub_formulas.sub_formulas)
                self.sub_formulas[1] = BooleanFormula(Operation.NOT, self.sub_formulas[1])
                self.operation = Operation.AND
                return any(map(lambda t: t.push_negations(), self.sub_formulas))

        return False

    def get_top_level_variable(self):
        # returns Formula if it is a variable or negation of variable
        if self.operation == Operation.VARIABLE:
            tmp = self.sub_formulas
            if isinstance(tmp, int):
                tmp = "i"+str(tmp)
            else:
                tmp = "s" + tmp
            return (tmp, True)
        if self.operation == Operation.NOT and self.sub_formulas.operation == Operation.VARIABLE:
            tmp = self.sub_formulas.sub_formulas
            if isinstance(tmp, int):
                tmp = "i" + str(tmp)
            else:
                tmp = "s" + tmp
            return (tmp, False)
        return ("", True)

    def remove_variables(self):
        # removes unnecessary variables (returns true if there were any changes)
        if self.operation == Operation.NOT:
            return self.sub_formulas.remove_variables()

        if self.operation == Operation.AND or self.operation == Operation.OR:
            # remove same variables that occur in OR or AND
            # first call the function recursively and check if there were changes
            change = any(map(lambda t: t.remove_variables(), self.sub_formulas))
            get_vars = list(enumerate(map(lambda t: t.get_top_level_variable(), self.sub_formulas)))
            get_vars = sorted(get_vars, key= lambda k: k[1])
            new_sub_formulas = [self.sub_formulas[get_vars[0][0]]]
            for var in range(1, len(get_vars)):
                if get_vars[var][1][0] != get_vars[var-1][1][0] or get_vars[var][1][0] == "":
                    # different subformulas
                    new_sub_formulas.append(self.sub_formulas[get_vars[0][0]])
                else:
                    # same variables
                    if get_vars[var][1][1] == get_vars[var-1][1][1]:
                        # same negation -> skip one
                        change = True
                    else:
                        # different negation
                        if self.operation == Operation.OR:
                            self.operation = Operation.TAUTOLOGY
                        else:
                            self.operation = Operation.FALSUM
                        self.sub_formulas = None
                        return False
            if change:
                self.sub_formulas = new_sub_formulas
            return change

        if self.operation == Operation.IMPLICATION:
            # first call the function recursively and check if there were changes
            change = self.sub_formulas[0].remove_variables() or self.sub_formulas[1].remove_variables()
            var1, var2 = list(set(self.sub_formulas[0].get_variables)), list(set(self.sub_formulas[1].get_variables))
            if len(var1) == 1 and len(var2) == 1 and var1[0] == var2[0]: # only one same var in both subformulas
                if self.solve({var1[0]:False}) == self.solve({var1[0]:True}): # outcome is not affected by var
                    if self.solve({var1[0], False}):
                        self.operation = Operation.TAUTOLOGY
                        self.sub_formulas = None
                    else:
                        self.operation = Operation.FALSUM
                        self.sub_formulas = None
                    return True
            return change

        return False

    def simplify(self):
        """
        calls all cleaning functions until there is no more changes
        """
        while True:
            if not any([self.push_negations(), self.remove_empty(), self.remove_variables(), self.remove_constants()]):
                break

    ###########
    # Tseytin #
    ###########

    def tseytin_step_one(self, used_vars=0):
        """
        this method maps sub formulas to new variables so that those equation can be used in creation of kno
        :param used_vars: tracks the number of variables used so that there are no duplicates
        :return: formula with new variables, all equations to new variables, number of used variables
        equations to new variables are in a form of a list with (formula, i) where i is the number of variable
        """
        if self.operation == Operation.NOT:
            sub_form, equ, used_vars = self.sub_formulas.tseytin_step_one(used_vars)
            equ.append((BooleanFormula(Operation.NOT, sub_form), used_vars))
            return BooleanFormula(Operation.VARIABLE, used_vars, keep_int=True), equ, used_vars+1
        elif self.operation in (Operation.IMPLICATION, Operation.AND, Operation.OR):
            new_sub_form = []
            eq = []
            for subf in self.sub_formulas:
                sub_form, equ, used_vars = subf.tseytin_step_one(used_vars)
                new_sub_form.append(sub_form)
                eq += equ
            eq.append((BooleanFormula(self.operation, new_sub_form), used_vars))
            return BooleanFormula(Operation.VARIABLE, used_vars, keep_int=True), eq, used_vars+1
        return self, [], used_vars

    def get_kno(self):
        f, equ, _ = self.tseytin_step_one()
        kno_sub_form = [BooleanFormula(Operation.OR, [f])]
        for formula, var in equ:
            variable = BooleanFormula(Operation.VARIABLE, var, keep_int=True)
            if formula.operation == Operation.NOT:
                kno_sub_form.append(BooleanFormula(Operation.OR, [variable, formula.sub_formulas]))
                kno_sub_form.append(BooleanFormula(Operation.OR, [
                    BooleanFormula(Operation.NOT, variable), formula]))
            elif formula.operation == Operation.AND:
                big_or = [variable]
                neg = BooleanFormula(Operation.NOT, variable)
                for sub_form in formula.sub_formulas:
                    big_or.append(BooleanFormula(Operation.NOT, sub_form))
                    kno_sub_form.append(BooleanFormula(Operation.OR, [sub_form, neg]))
                kno_sub_form.append(BooleanFormula(Operation.OR, big_or))
            elif formula.operation == Operation.OR:
                big_or = [BooleanFormula(Operation.NOT, variable)]
                for sub_form in formula.sub_formulas:
                    big_or.append(sub_form)
                    neg = BooleanFormula(Operation.NOT, sub_form)
                    kno_sub_form.append(BooleanFormula(Operation.OR, [variable, neg]))
                kno_sub_form.append(BooleanFormula(Operation.OR, big_or))
            elif formula.operation == Operation.IMPLICATION:
                formula1, formula2 = formula.sub_formulas
                kno_sub_form.append(BooleanFormula(Operation.OR, [
                    BooleanFormula(Operation.NOT, formula1), formula2, BooleanFormula(Operation.NOT, variable)
                ]))
                kno_sub_form.append(BooleanFormula(Operation.OR, [formula1, variable]))
                kno_sub_form.append(BooleanFormula(Operation.OR,
                    [BooleanFormula(Operation.NOT, formula2), variable]))
        out = BooleanFormula(Operation.AND, kno_sub_form)
        # simplifying
        out.simplify()
        # prefer empty ands and ors to nothing for easier solving
        if out.operation != Operation.AND:
            out = BooleanFormula(Operation.AND, [out])
        for sub_f in range(len(out.sub_formulas)):
            if out.sub_formulas[sub_f].operation != Operation.OR:
                out.sub_formulas[sub_f] = BooleanFormula(Operation.OR, [out.sub_formulas[sub_f]])
        return out


