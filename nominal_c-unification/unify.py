# unification implementation of the algorithm 
# We tried to make it closer with the pseudocode in the article

# code only because lab does not have python3 
from __future__ import print_function

import copy

class Atom: 
    def __init__(self, name): 
        self.name = name

    def __str__(self): 
        return self.name

class Suspended_variable: 
    def __init__(self, perm, var): 
        self.perm = perm
        self.var = var

    def __str__(self): 
        # build a way to print permutation 
        perm_str = "[" 
        for swap in self.perm: 
            perm_str += "(" + swap[0] + " " +  swap[1] + ") "
        perm_str += "]"
        return perm_str + "*" + self.var

class Unit: 
    def __init__(self): 
        pass 
    
    def __str__(self): 
        return "<>"

class Abstraction: 
    def __init__(self, atom, body): 
        self.atom = atom 
        self.body = body 

    def __str__(self): 
        return "[" + (self.atom).__str__() + "]" + (self.body).__str__() 

class Pair: 
    def __init__(self, term1, term2): 
        self.term1 = term1
        self.term2 = term2

    def __str__(self): 
        return "<" + (self.term1).__str__() + ", " + (self.term2).__str__() + ">"

class Application: 
    def __init__(self, symbol, arg): 
        self.symbol = symbol
        self.arg = arg
    
    def __str__(self): 
        return self.symbol + "(" + (self.arg).__str__() + ")" 

class CApplication: 
    def __init__(self, symbol, arg): 
        assert(isinstance(arg, Pair))
        self.symbol = symbol 
        self.arg = arg

    def __str__(self): 
        return self.symbol + "(" + (self.arg).__str__() + ")" 
        
# check if var X is in t 
def is_var_in_term(X, t): 
    if isinstance(t, Atom):
        return False
    elif isinstance(t, Suspended_variable): 
        return X == t.var 
    elif isinstance(t, Unit): 
        return False
    elif isinstance(t, Abstraction): 
        return is_var_in_term(X, t.body) 
    elif isinstance(t, Pair): 
        return is_var_in_term(X, t.term1) or is_var_in_term(X, t.term2) 
    elif isinstance(t, Application): 
        return is_var_in_term(X, t.arg)
    elif isinstance(t, CApplication): 
        return is_var_in_term(X, t.arg) 

# apply a permutation to an atom name. The permutation is represented as a swap list
def apply_perm_atom(swap_lst, atom_name): 
    if len(swap_lst) == 0: 
        return atom_name
    else: 
        atom_name = apply_perm_atom(swap_lst[1:], atom_name) 
        swap = swap_lst[0]
        if atom_name == swap[0]: 
            return swap[1]
        elif atom_name == swap[1]: 
            return swap[0]
        else: 
            return atom_name

# inverse a permutation 
def inverse_perm(perm): 
    return perm[::-1] 

# apply a permutation, represented as a list of swappings to a term t
def apply_perm(swap_lst, t): 
    if isinstance(t, Atom): 
        new_t_name = apply_perm_atom(swap_lst, t.name) 
        new_t = Atom(new_t_name)
        return new_t
    elif isinstance(t, Suspended_variable): 
        new_t_perm = swap_lst + t.perm
        new_t_var = t.var
        new_t = Suspended_variable(new_t_perm, new_t_var)
        return new_t
    elif isinstance(t, Unit): 
        new_t = Unit()
        return new_t
    elif isinstance(t, Abstraction): 
        new_t_atom = apply_perm(swap_lst, t.atom)
        new_t_body = apply_perm(swap_lst, t.body)  
        new_t = Abstraction(new_t_atom, new_t_body) 
        return new_t
    elif isinstance(t, Pair): 
        new_t_term1 = apply_perm(swap_lst, t.term1) 
        new_t_term2 = apply_perm(swap_lst, t.term2) 
        new_t = Pair(new_t_term1, new_t_term2)
        return new_t
    elif isinstance(t, Application): 
        new_t_symbol = t.symbol
        new_t_arg = apply_perm(swap_lst, t.arg) 
        new_t = Application(new_t_symbol, new_t_arg)
        return new_t 
    elif isinstance(t, CApplication): 
        new_t_symbol = t.symbol
        new_t_arg = apply_perm(swap_lst, t.arg) 
        new_t = CApplication(new_t_symbol, new_t_arg)
        return new_t 
    else: 
        quit("term passed is not really a term") 
            

# returns the minimal context necessary for an atom a to be fresh in t. 
# returns also a boolean, indicating if it is possible
def is_fresh(a, t): 
    if isinstance(t, Atom): 
        return ([], a != t.name) 
    elif isinstance(t, Suspended_variable): 
        return ([(apply_perm_atom(inverse_perm(t.perm), a), t.var)], True)
    elif isinstance(t, Unit): 
        return ([], True)
    elif isinstance(t, Abstraction): 
        if (t.atom).name == a: 
            return ([], True)
        else: 
            return is_fresh(a, t.body)
    elif isinstance(t, Pair): 
        (Delta1, bool1) = is_fresh(a, t.term1) 
        (Delta2, bool2) = is_fresh(a, t.term2) 
        if bool1 and bool2: 
            return (Delta1 + Delta2, True) 
        else: 
            return ([], False) 
    elif isinstance(t, Application): 
        return is_fresh(a, t.arg)
    elif isinstance(t, CApplication): 
        return is_fresh(a, t.arg)
    else: 
        quit("term passed is not really a term") 

# returns the minimal context in which a#Xsigma, for every a#X in Nabla 
# returns a boolean indicating if it is possible
def is_fresh_subs(sigma, Nabla): 
    if len(Nabla) == 0: 
        return ([], True)
    else: 
        (a, X) = (Nabla[0][0], Nabla[0][1]) 
        (Delta1, bool1) = is_fresh(a, apply_sub_term(sigma, Suspended_variable([], X)))     
        (Delta2, bool2) = is_fresh_subs(sigma, Nabla[1:])
        if bool1 and bool2: 
            return (Delta1 + Delta2, True)
        else: 
            return([], False)

# apply a nuclear substitution to a term 
def apply_nuc_sub_term(nuc_sub, t): 
    (X, s) = (nuc_sub[0], nuc_sub[1]) 
    if isinstance(t, Atom): 
        return t
    elif isinstance(t, Suspended_variable): 
        if t.var == X: 
            return apply_perm(t.perm, s) 
        else: 
            return t
    elif isinstance(t, Unit): 
        return t
    elif isinstance(t, Abstraction): 
        t.body = apply_nuc_sub_term(nuc_sub, t.body)  
        return t
    elif isinstance(t, Pair): 
        t.term1 = apply_nuc_sub_term(nuc_sub, t.term1) 
        t.term2 = apply_nuc_sub_term(nuc_sub, t.term2) 
        return t
    elif isinstance(t, Application): 
        t.arg = apply_nuc_sub_term(nuc_sub, t.arg) 
        return t 
    elif isinstance(t, CApplication): 
        t.arg = apply_nuc_sub_term(nuc_sub, t.arg) 
        return t
    else: 
        quit("term passed is not really a term") 

# apply a substitution, represented as a list of nuclear substitutions, to a term 
def apply_sub_term(sigma, t): 
    if len(sigma) == 0: 
        return t
    else: 
        return apply_sub_term(sigma[1:], apply_nuc_sub_term(sigma[0], t))

# apply a substitution sigma to a list of unification problems
def apply_sub(sigma, PrbLst): 
    if len(PrbLst) == 0: 
        return [] 
    else: 
        (t, s) = PrbLst[0] 
        t_sigma = apply_sub_term(sigma, t) 
        s_sigma = apply_sub_term(sigma, s) 
        return [(t_sigma, s_sigma)] + apply_sub(sigma, PrbLst[1:])


# transforma a list of fixpoint equations into a list of unification problems
def fix_pnt2prb_lst(FPEqLst): 
    if len(FPEqLst) == 0: 
        return [] 
    else: 
        fix_pnt_equation = FPEqLst[0] 
        perm = fix_pnt_equation[0] 
        var = fix_pnt_equation[1] 
        t = Suspended_variable(perm, var) 
        s = Suspended_variable([], var) 
        return [(t, s)] + fix_pnt2prb_lst(FPEqLst[1:])

# the function that unifies terms t and s
def unify(Delta, sigma, PrbLst, FPEqLst, verb=False, indent_lvl=""):
    #colocar um deep copy na hora dos branchs... colocar um deepcopy na hora de chamar is_fresh_subs, na hora de chamar is_fresh tb
    #check_param(Delta, sigma, PrbLst, FPEqLst)
    if verb: 
        print_quad(Delta, sigma, PrbLst, FPEqLst, indent_lvl)

    if len(PrbLst) == 0: 
        if verb: 
            print(indent_lvl, end = '') 
            print_sol([(Delta, sigma, FPEqLst)])
            print("\n")
        return [(Delta, sigma, FPEqLst)]
    else: 
        (t, s) = PrbLst[0]
        PrbLst1 = PrbLst[1:]
        if isinstance(s, Suspended_variable) and (not is_var_in_term(s.var, t)):
            sigma1 = [(s.var, apply_perm(inverse_perm(s.perm), t))]
            sigma2 = sigma1 + sigma 
            (Delta1, bool1) = is_fresh_subs(sigma1, copy.deepcopy(Delta))
            Delta2 = Delta1 + Delta
            PrbLst2 = apply_sub(sigma1, PrbLst1) + \
                        apply_sub(sigma1, fix_pnt2prb_lst(FPEqLst)) 
            if bool1: 
                return unify(Delta2, sigma2, PrbLst2, [], verb, indent_lvl) 
            else:
                if verb: 
                    print(indent_lvl + "No solution\n") 
                return []

        else: 
            if isinstance(t, Atom): 
                if isinstance(s, Atom) and s.name == t.name: 
                    return unify(Delta, sigma, PrbLst1, FPEqLst, verb, indent_lvl)
                else: 
                    if verb: 
                        print(indent_lvl + "No solution\n")
                    return []

            elif isinstance(t, Suspended_variable):  
                if not is_var_in_term(t.var, s): 
                    sigma1 = [(t.var, apply_perm(inverse_perm(t.perm), s))]
                    sigma2 = sigma1 + sigma 
                    (Delta1, bool1) = is_fresh_subs(sigma1, copy.deepcopy(Delta))
                    Delta2 = Delta1 + Delta
                    PrbLst2 = apply_sub(sigma1, PrbLst1) + \
                                apply_sub(sigma1, fix_pnt2prb_lst(FPEqLst)) 
                    if bool1: 
                        return unify(Delta2, sigma2, PrbLst2, [], verb, indent_lvl) 
                    else: 
                        if verb: 
                            print(indent_lvl + "No solution\n") 
                        return []

                elif isinstance(s, Suspended_variable) and s.var == t.var:
                    FPEqLst1 = [(inverse_perm(s.perm) + t.perm, t.var)] + \
                                FPEqLst 
                    return unify(Delta, sigma, PrbLst1, FPEqLst1, verb, indent_lvl)
                else: 
                    if verb: 
                        print(indent_lvl + "No solution\n")
                    return []

            elif isinstance(t, Unit):
                if isinstance(s, Unit): 
                    return unify(Delta, sigma, PrbLst1, FPEqLst, verb, indent_lvl)
                else: 
                    if verb: 
                        print(indent_lvl + "No solution\n")
                    return []
             
            elif isinstance(t, Pair): 
                if isinstance(s, Pair): 
                    PrbLst2 = [(t.term1, s.term1)] + [(t.term2, s.term2)] + PrbLst1
                    return unify(Delta, sigma, PrbLst2, FPEqLst, verb, indent_lvl)
                else: 
                    if verb: 
                        print(indent_lvl + "No solution\n")
                    return []

            elif isinstance(t, Abstraction): 
                if isinstance(s, Abstraction) and (t.atom).name == (s.atom).name:  
                    PrbLst2 = [(t.body, s.body)] + PrbLst1
                    return unify(Delta, sigma, PrbLst2, FPEqLst, verb, indent_lvl)
                elif isinstance(s, Abstraction) and (t.atom).name != (s.atom).name: 
                    (Delta1, bool1) = is_fresh(copy.deepcopy((t.atom).name), s.body)
                    Delta2 = Delta1 + Delta 
                    PrbLst2 = [(t.body, apply_perm([((t.atom).name, \
                                (s.atom).name)], s.body))] + PrbLst1
                    if bool1: 
                        return unify(Delta2, sigma, PrbLst2, FPEqLst, verb,
                                indent_lvl)
                    else: 
                        if verb: 
                            print(indent_lvl + "No solution\n") 
                        return [] 
                else: 
                    if verb: 
                        print(indent_lvl + "No solution\n") 
                    return []

            elif isinstance(t, Application): 
                if (not isinstance(s, Application)) or (t.symbol != s.symbol): 
                    if verb: 
                        print(indent_lvl + "No solution\n") 
                    return [] 
                else: 
                    PrbLst2 = [(t.arg, s.arg)] + PrbLst1
                    return unify(Delta, sigma, PrbLst2, FPEqLst, verb, indent_lvl) 

            elif isinstance(t, CApplication): 
                if (not isinstance(s, CApplication)) or (t.symbol != s.symbol): 
                    if verb: 
                        print(indent_lvl + "No solution\n") 
                    return [] 
                else: 
                    new_indent_lvl = indent_lvl + "   "
                    PrbLst_branch1 = [((t.arg).term1, (s.arg).term1)] + \
                                     [((t.arg).term2, (s.arg).term2)] + \
                                     PrbLst1 
                    sol1 = unify(copy.deepcopy(Delta), copy.deepcopy(sigma), copy.deepcopy(PrbLst_branch1), 
				copy.deepcopy(FPEqLst), verb, new_indent_lvl) 
                    PrbLst_branch2 = [((t.arg).term1, (s.arg).term2)] + \
                                     [((t.arg).term2, (s.arg).term1)] + \
                                     PrbLst1 
                    sol2 = unify(Delta, sigma, PrbLst_branch2, FPEqLst, verb, 
                            new_indent_lvl) 
                    return sol1 + sol2
            else: 
                quit("term t is not really a term")

# print a context 
def print_context(Delta): 
    print("[", end = '')
    for fresh_constraint in Delta: 
        print(fresh_constraint[0] + "#" + fresh_constraint[1] + " ", end = '')
    print("]", end = '') 

# print a substitution
def print_sub(sigma): 
    if len(sigma) == 0: 
        print("id", end = '')
    else: 
        print("[", end = '')
        for nuc_sub in sigma: 
            print(nuc_sub[0] + "->", end = '') 
            print(nuc_sub[1], end = ' ')
        print("]", end = '')

# prints a list of unification problems
def print_prb_lst(PrbLst): 
    print("[", end = '') 
    for unif_prb in PrbLst: 
        print("(", end = '') 
        print(unif_prb[0], end = '')
        print(" = ", end = '') 
        print(unif_prb[1], end = '')
        print("), ", end = '') 
    print("]", end = '')

# prints a fix point equation
def print_fix_pnt_eq(FPEqLst): 
    print("[", end = '')
    for fix_pnt_eq in FPEqLst: 
        print(fix_pnt_eq[0], end = '')
        print("*" + fix_pnt_eq[1] + " = " + fix_pnt_eq[1] + " ", end = '')
    print("]", end = '')

# prints the solutions found by the unify function 
def print_sol(sol_lst):
    if len(sol_lst) == 0: 
        print("no solution was found") 
    else: 
        for sol in sol_lst: 
            print("solution: <", end = '')
            print_context(sol[0])
            print(", ", end = '')
            print_sub(sol[1])
            print(", ", end = '')
            print_fix_pnt_eq(sol[2])
            print(">")

# print a quadruple 
def print_quad(Delta, sigma, PrbLst, FPEqLst, indent_lvl): 
    print(indent_lvl + "<", end = '')
    print_context(Delta)
    print(", ", end = '') 
    print_sub(sigma) 
    print(", ", end = '')
    print_prb_lst(PrbLst)
    print(", ", end = '') 
    print_fix_pnt_eq(FPEqLst)
    print(">", end = '')
    print("\n" + indent_lvl + "|") 

