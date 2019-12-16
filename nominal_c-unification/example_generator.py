# generates automatically examples 
from unify import * 
import random
import copy

# indices of atoms, variables, unit, abstraction, pair, application and commutative
# application in the list of probabilities. 
ATOM_IND = 0 
VAR_IND = 1
UNIT_IND = 2
ABS_IND = 3
PAIR_IND = 4
APP_IND = 5


## the way atoms and variables are denoted is used when we are extracting the number
## the atom we are dealing with (in the context of pvsio). Therefore, don't change
## the representation below. 

# atom prefix - atoms will be denoted by a1, a2, ...  
ATOM_PREFIX = "a"
# atom range - how many different atoms we will be working  
ATOM_RANGE = 10

# variable prefix - variables will be denoted by X1, X2, ...  
VAR_PREFIX = "X"
# variable range - how many different variables we will be working  
VAR_RANGE = 10

# application prefix - function applications will be denoted by f1, f2, ...  
APP_PREFIX = "f"
# application range - how many different function applications we will be working  
APP_RANGE = 5

# commutative function application prefix - commutative function applications will be
# denoted by f^C_1, f^C_2 and so on
CAPP_PREFIX = "f^C_1" 
# commutative application range - how many different commutative function
# applications we will be working  
CAPP_RANGE = 5

# an example of a possible list of probabilities
LST_PROB = [0.1,  0.3, 0.4, 0.6, 0.7, 0.9]

# example parameters of copy term with mods
PROB_VAR = 0.05
PROB_MISS_ATOMS = 0.1
PROB_ABS_ATOMS = 0.5
PROB_C_SWAP = 0.5

def generate_random_perm(prob_stop = 0.5): 
    """ 
    receives: the probability of stopping constructing the permutation
    returns: a random permutation, where the probability of stopping is 0.5 at each
    recursive call
    """
    prob = random.random()
    if prob < prob_stop: 
        return [] 
    else: 
        return [(ATOM_PREFIX + str(random.randint(1, ATOM_RANGE)), 
                ATOM_PREFIX + str(random.randint(1, ATOM_RANGE)))] + \
                generate_random_perm(prob_stop)

def generate_random_term(lst_prob):
    """ 
    receives: lst_prob, a list containing the probability of generating atoms,
    suspend variable and so on. 
    returns: a term, generated randomly according to lst_prob
    """
    # get whether term will be atom, variable, unit, ... 
    prob = random.random()
    if prob < lst_prob[ATOM_IND]:
        return Atom(ATOM_PREFIX + str(random.randint(1, ATOM_RANGE)))
    elif prob < lst_prob[VAR_IND]: 
        return Suspended_variable(generate_random_perm(), VAR_PREFIX +
                str(random.randint(1, VAR_RANGE)))
    elif prob < lst_prob[UNIT_IND]: 
        return Unit()
    elif prob < lst_prob[ABS_IND]: 
        return Abstraction(Atom(ATOM_PREFIX + str(random.randint(1, ATOM_RANGE))),
                        generate_random_term(lst_prob))
    elif prob < lst_prob[PAIR_IND]: 
        return Pair(generate_random_term(lst_prob), generate_random_term(lst_prob))
    elif prob < lst_prob[APP_IND]: 
        return Application(APP_PREFIX + str(random.randint(1, APP_RANGE)), 
                        generate_random_term(lst_prob))
    else: 
        return CApplication(CAPP_PREFIX + str(random.randint(1, CAPP_RANGE)), 
                        Pair(generate_random_term(lst_prob),
                            generate_random_term(lst_prob)))

def copy_term_with_mod(t, prob_var, prob_miss_atoms, prob_abs_atoms, prob_c_swap): 
    """ 
    receives: 
        t - the term to be copied, with slight modifications
        prob_var - probability of returning a suspended variable instead of the term
        prob_miss_atoms - probability of confusing atoms and changing their names,
        prob_abs_atoms - probability of changing the atom in an abstraction
                          obtaining a semantically different term. 
        prob_c_swap - probability of swapping the arguments of the term, case it is a
                      commutative function 
    returns: another term, similar to the one studied, but with slight modifications
    """
    # maybe substitute term by a suspended variable, according to the value of prob
    prob = random.random() 
    if prob < prob_var: 
        return Suspended_variable(generate_random_perm(), VAR_PREFIX +
                str(random.randint(1, VAR_RANGE)))
    
    ## copy term with slight modifications

    # if an atom, check whether we will miss the atom and alter the semantics of the
    # term
    elif isinstance(t, Atom): 
        if prob < prob_miss_atoms:  
            return Atom(ATOM_PREFIX + str(random.randint(1, ATOM_RANGE)))
        else:     
            return copy.deepcopy(t)

    # if an abstraction, check whether we will apply a random permutation
    elif isinstance(t, Abstraction): 
        if prob < prob_abs_atoms: 
            return apply_perm(generate_random_perm(), t)
        else: 
            return copy.deepcopy(t)
    
    elif isinstance(t, CApplication): 
        if prob < prob_c_swap: 
            return CApplication(t.symbol, Pair(copy.deepcopy((t.arg).term2),
                copy.deepcopy((t.arg).term1)))
        else: 
            return copy.deepcopy(t)
    else: 
        return copy.deepcopy(t)

#for i in range(10): 
#    t = generate_random_term(LST_PROB)
#    copy_term_with_mod(t, 0.05, 0.1, 0.5, 0.5)
#    print(i)
