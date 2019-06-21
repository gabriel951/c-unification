# tests for the functions defined in unify 
from unify import *

def test_is_var_in_term(): 
    a = Atom("a") 
    b = Atom("b") 
    pi_X = Suspended_variable([], "X")
    unit = Unit()
    pair_term = Pair(a, pi_X)
    abs_term = Abstraction(a, a) 
    app_term = Application("f", pi_X)
    capp_term = CApplication("f", pair_term)

    print(is_var_in_term("a", a)) 
    print(is_var_in_term("X", pi_X))
    print(is_var_in_term("Y", pi_X))
    print(is_var_in_term("Y", unit))
    print(is_var_in_term("Z", pair_term))
    print(is_var_in_term("X", pair_term))
    print(is_var_in_term("X", abs_term))
    print(is_var_in_term("X", app_term))
    print(is_var_in_term("X", capp_term))

def test_perm(): 
    a = Atom("a") 
    b = Atom("b") 
    c = Atom("c") 
    print(apply_perm_atom([("a", "b")], "a"))
    print(apply_perm_atom([("a", "b")], "b"))
    print(apply_perm_atom([("a", "b")], "c"))
    print(apply_perm_atom([("a", "b"), ("b", "c")], "c"))

    pi_X = Suspended_variable([], "X")
    unit = Unit()
    pair_term = Pair(a, pi_X)
    abs_term = Abstraction(a, a) 
    app_term = Application("f", pi_X)
    capp_term = CApplication("f", pair_term)
    perm = [("a", "b"), ("c", "d")]
    print(inverse_perm(perm))

    print(apply_perm(perm, a))
    print(apply_perm(perm, pi_X)) 
    print(apply_perm(perm, unit)) 
    print(apply_perm(perm, pair_term)) 
    print(apply_perm(perm, abs_term))
    print(apply_perm(perm, app_term))
    print(apply_perm(perm, capp_term))
    print("im done") 


def test_freshness(): 
    a = Atom("a") 
    pi_X = Suspended_variable([], "X")
    unit = Unit()
    pair_term = Pair(a, pi_X)
    abs_term = Abstraction(a, a) 
    app_term = Application("f", pi_X)
    capp_term = CApplication("f", pair_term)

    print(is_fresh("a", a))
    print(is_fresh("a", pi_X)) 
    print(is_fresh("a", unit)) 
    print(is_fresh("a", pair_term)) 
    print(is_fresh("a", abs_term))
    print(is_fresh("a", app_term))
    print(is_fresh("a", capp_term))
    print("im done") 

def test_unify(): 
    a = Atom("a")
    b = Atom("b") 
    a_a = Abstraction(a, a)
    b_b = Abstraction(b, b) 

    #sol = unify([], [], [(a, b)], [])
    #print_sol(sol) 
    #sol = unify([], [], [(a, a)], [])
    #print_sol(sol) 
    #print("im done") 
    sol = unify([], [], [(a, a)], [])
    print_sol(sol) 
    


def run_first_ex_paper(): 
    c = Atom("c")
    pi_X = Suspended_variable([("a", "b")], "X")
    id_X = Suspended_variable([], "X")
    pair_t = Pair(pi_X, c) 
    pair_s = Pair(id_X, c) 

    # the two terms we are trying to unify in the first example
    capp_t = CApplication("f", pair_t)
    capp_s = CApplication("f", pair_s) 

    print("Trying to unify terms: ", end='') 
    print(capp_t, end='') 
    print(" and ", end = '')
    print(capp_s)
    print("\n")
    sol = unify([], [], [(capp_t, capp_s)], [], True, '')
    print("Finished.")

def run_second_ex_paper(): 
    c = Atom("c")
    pi_X = Suspended_variable([("a", "b")], "X")
    id_X = Suspended_variable([], "X")
    pair_t = Pair(pi_X, c) 
    pair_s = Pair(id_X, c) 

    # the two terms we are trying to unify in the first example
    capp_t = CApplication("f", pair_t)
    capp_s = CApplication("f", pair_s) 

    #print_sol(sol) 

    # second example 
    d = Atom("d") 
    h_d = Application("h", d)
    pair_t2 = Pair(h_d, capp_t) 
    pair_s2 = Pair(capp_s, h_d) 
    gapp_t = CApplication("g", pair_t2) 
    gapp_s = CApplication("g", pair_s2) 

    print("Trying to unify terms: ", end='') 
    print(gapp_t, end='') 
    print(" and ", end = '')
    print(gapp_s)
    print("\n")
    sol = unify([], [], [(gapp_s, gapp_s)], [], True, '')
    print("Finished.")

# preliminar test 
#test_is_var_in_term()
#test_perm()
#test_freshness()
#test_unify()

#tests that appear in the paper
run_first_ex_paper()
run_second_ex_paper()

