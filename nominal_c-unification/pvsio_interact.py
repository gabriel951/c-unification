from unify import * 
from example_generator import * 
import pickle

NUM_INTERATIONS = 2000
PVSIO_INPUT_FILE_NAME = 'experiment_' + str(NUM_INTERATIONS) + '/pvsio_input_' + str(NUM_INTERATIONS) + '.txt'
PVSIO_OUTPUT_NOT_CORRECTED = 'experiment_' + str(NUM_INTERATIONS) + '/pvsio_output_not_corrected.txt'
PVSIO_OUTPUT_CORRECTED = 'experiment_' + str(NUM_INTERATIONS) + '/pvsio_output.txt'
PYTHON_OUTPUT_FILE_NAME = 'experiment_' + str(NUM_INTERATIONS) + '/python_output.txt'
PICKLE_FILE = 'experiment_' + str(NUM_INTERATIONS) + '/lst_terms_python'


def correct_empty_list(string): 
    """
    receives: a string, which may correspond to an empty list
    the function corrects a string of the form (:  :) into the string (: :), 
    the correct way PVS represents an empty string
    returns: the original string, if its not an empty string or the string (: :) 
    correctly represented in PVS
    """
    if string == "(:  :)":
        return "(: :)"
    return string

def generate_pvsio_input(lst_terms): 
    """
    receives: a list of terms
    generates random terms and saves them in a .txt input file that will be supplied to
    PVSIO. Also run the python code in those terms, saving the output (converted
    to PVSIO format) in a .txt output file. 
    """
    pvsio_input_file = open(PVSIO_INPUT_FILE_NAME, "w") 

    # write in PVSIO format
    for t, s in lst_terms: 
        pvsio_input_file.write("(:(")
        pvsio_input_file.write(get_term_representation_pvsio(t)) 
        pvsio_input_file.write(",")
        pvsio_input_file.write(get_term_representation_pvsio(s))
        pvsio_input_file.write("):)")
	pvsio_input_file.write("::unif_prb_lst_typ") # necessary for PVS7, optional for PVS6
	pvsio_input_file.write("\n")

    pvsio_input_file.close()

def get_number(t): 
    """
    receives: a term, which must be an atom or a variable
    returns: the string that represents the number in the term
    """ 
    assert(isinstance(t, Atom) or isinstance(t, Suspended_variable))
    if isinstance(t, Atom): 
        return t.name[1:]
    else: 
        return t.var[1:]

def get_term_representation_pvsio(t): 
    """
    receives: a term t 
    returns: the string that represents the term in pvsio 
    """
    if isinstance(t, Atom): 
        return "at(" + get_number(t) + ")"

    elif isinstance(t, Suspended_variable): 
        return  get_perm_representation_pvsio(t.perm) + " * " + \
                get_number(t)

    elif isinstance(t, Unit): 
        return "unit"

    elif isinstance(t, Abstraction): 
        return "abs(" + get_number(t.atom) + ", " + \
                get_term_representation_pvsio(t.body) + ")"

    elif isinstance(t, Pair): 
        return "pair(" + get_term_representation_pvsio(t.term1) + ", "  + \
                get_term_representation_pvsio(t.term2) + ")"

    elif isinstance(t, Application): 
        return "app(" + "\"" + t.symbol + "\"" + ", " + \
                get_term_representation_pvsio(t.arg) + ")"
    
    elif isinstance(t, CApplication): 
        return "c_app(" + "\"" + t.symbol + "\"" + ", " + \
                get_term_representation_pvsio(t.arg) + ")"

    else: 
        exit("the argument passed is not really a term")

def get_perm_representation_pvsio(perm): 
    """
    receives: a permutation (list of swappings) perm  
    returns: the string that represents the permutation in pvsio 
    """
    string_perm = "(: "
    for i in range(len(perm)): 
        swap = perm[i]
        (t, s) = (swap[0][1:], swap[1][1:])
        string_perm += "(" + t + ", " + s + ")"

        if i != len(perm) - 1: 
            string_perm += ", "
    string_perm += " :)"
    string_perm = correct_empty_list(string_perm)
    return string_perm

def get_context_representation_pvsio(context): 
    """ 
    receives: a context 
    returns: the string corresponding to this context in pvsio 
    """
    string_ctxt = "(: "
    for i in range(len(context)): 
        string_ctxt += "(" + context[i][0][1:] + ", " + context[i][1][1:] + ")" 
        if i != len(context) - 1: 
            string_ctxt += ", "
    string_ctxt += " :)" 
    string_ctxt = correct_empty_list(string_ctxt)
    return string_ctxt

def get_subs_representation_pvsio(substitution): 
    """
    receives: a substitution
    returns: the string corresponding to this substitution in PVSIO
    """
    string_subs = "(: "
    for i in range(len(substitution)): 
        subs = substitution[i]
        string_subs += "(" + subs[0][1:] +  ", " + \
            get_term_representation_pvsio(subs[1]) + ")"  
        if i != len(substitution) - 1: 
            string_subs += ", "

    string_subs += " :)"
    string_subs = correct_empty_list(string_subs)
    return string_subs

def get_fix_pnt_eq_representation_pvsio(fix_pnt_eq_lst): 
    """
    receives: a fixpoint equation list
    returns: the string corresponding to this list in PVSIO
    """
    string_fix_pnt_eq_lst = "(: "
    for i in range(len(fix_pnt_eq_lst)): 
        fix_pnt_eq = fix_pnt_eq_lst[i] 
        string_fix_pnt_eq_lst += "(" + get_perm_representation_pvsio(fix_pnt_eq[0]) + \
                                    ", " + fix_pnt_eq[1][1:] + ")"
        if i != len(fix_pnt_eq_lst) - 1: 
            string_fix_pnt_eq_lst += ", "

    string_fix_pnt_eq_lst += " :)"
    string_fix_pnt_eq_lst = correct_empty_list(string_fix_pnt_eq_lst)
    return string_fix_pnt_eq_lst

def generate_lst_terms():
    """
    generates a list of terms to be unified. Saves the list in a pickle object
    returns: the list of terms generated
    """
    # generate the terms
    lst_terms = []
    for i in range(NUM_INTERATIONS): 
        t = generate_random_term(LST_PROB)
        s = copy_term_with_mod(t, PROB_VAR, PROB_MISS_ATOMS, PROB_ABS_ATOMS,
                PROB_C_SWAP)
        lst_terms += [(t, s)]

    # serializes the list
    pickle_file = open(PICKLE_FILE, "ab")
    pickle.dump(lst_terms, pickle_file)
    pickle_file.close()

    return lst_terms

def load_lst_terms(): 
    """
    load a lst of terms saved in PICKLE_FILE
    returns: a list of terms
    """
    pickle_file = open(PICKLE_FILE, 'rb') 
    lst_terms = pickle.load(pickle_file)
    pickle_file.close()
    return lst_terms

def run_python_code(lst_terms):
    """
    receives: a list of terms, 
    run the python code in those terms saving the output (converted to PVSIO format)
    in a .txt file
    """
    python_output_file = open(PYTHON_OUTPUT_FILE_NAME, "w")

    # run python algorithm 
    for t, s in lst_terms: 
        # run python algorithm in the terms and write output to a file
        # the if-else separation is necessary!
        solution_lst = unify([], [], [(t, s)], [])
        if len(solution_lst) == 0: 
            python_output_file.write("(: :)\n")
        else: 
            python_output_file.write("(: ")
            for j in range(len(solution_lst)): 
                sol = solution_lst[j]
                python_output_file.write("(")
                python_output_file.write(get_context_representation_pvsio(sol[0]))
                python_output_file.write(", ")
                python_output_file.write(get_subs_representation_pvsio(sol[1]))
                python_output_file.write(", ")
                python_output_file.write(get_fix_pnt_eq_representation_pvsio(sol[2]))
                python_output_file.write(")")

                # check if it's not the last solution
                if j != len(solution_lst) - 1: 
                    python_output_file.write(", ")

            python_output_file.write(" :)\n")
        
    python_output_file.close()

def treat_pvsio_output(): 
    """
    open the PVSIO output .txt file, reads it and write every solution in one line.
    this is done by putting in only one line the lines that end in commas. 
    """
    input_file = open(PVSIO_OUTPUT_NOT_CORRECTED, "r") 
    output_file = open(PVSIO_OUTPUT_CORRECTED, "w")

    first_line = True
    for line in input_file: 
	# a line starts with parenteses or space
        assert(line[0] == "(" or line[0] == " ")
	
	# decide whether we should skip a line after printing the previous line
        if not first_line and line[0] == "(":
	    output_file.write("\n")
	first_line = False

	# remove spaces in the beggining and in the end of current line
        line = line.lstrip()
        line = line.rstrip('\n')

	# special case, if the line starts with an infix operator, add space
	if line[0] == "*": 
	    output_file.write(" ")

	# write line
        output_file.write(line)

	# decide whether we write a space or write nothing, according to the last character
	if line[-1] == "," or line[-1] == "*":
	    output_file.write(" ")

    input_file.close() 
    output_file.close()


## 
#compare_pvsio_python_output()
treat_pvsio_output()

#lst_terms = generate_lst_terms()
#lst_terms = load_lst_terms()
#run_python_code(copy.deepcopy(lst_terms))
#generate_pvsio_input(lst_terms)

# debug code
#counter = 1
#for t, s in lst_terms:
#	if counter == 848:
#		unify([], [], [(t,s)], [], True, "  ")
#	counter += 1
