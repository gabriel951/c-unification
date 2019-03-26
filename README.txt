%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Authors: Gabriel Ferreira Silva (*) 
%          Ana Cristina Rocha-Oliveira (*)
%          Mauricio Ayala-Rincon (*)
%          Daniele Nantes Sobrinho (*)
%          Maribel Fernandez (**)
%          (*)Universidade de Brasilia, (**)King's College London
% 
% In the directory "files" you will find the .pvs and .prf files of the formalisation
% of nominal c-unification. 
% The top subtheory is >> nominalunif.pvs <<
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

The theory Nominal Unification consists of eight pvs files.

  This was specified in PVS 6.0 (available at http://pvs.csl.sri.com) over
  Mac Os and Linux platforms. Also, you will need the PVS NASA libraries
  (available at http://shemesh.larc.nasa.gov/fm/ftp/larc/PVS-library). 
  Running PVS opens an Emacs window. 

  Uncompress and copy the nominal unification directory somewhere in your 
  system. Then run PVS using as context library (change context) that 
  directory.  

  To follow a proof you should place the cursor over the lemma or theorem
  you want to check and use the PVS meta commands x-step-proof (step by
  step) or x-prove.
 
The contents of the nominal unification library are described below.

atoms.pvs with the implementation of atoms as natural numbers, permutations 
          and the difference set (ds).

nominal_term.pvs contains the data structure of terms and auxiliary functions that
                 that deal with terms. Type checking will generate the additional 
                 pvs file: 
term_adt.pvs which contains all inductive proof schematta for this ADT.

fresh.pvs contains the definition of freshness through the boolean recursive 
          function ``fresh" which checks if an atom is fresh for a term with 
          respect to a specific context. The function ``fresh?" does something 
          similar by verifying if an atom is fresh for a term in some context 
          and, simultaneously, it builds such a context, if it exists. Some 
          properties can be reached very easily, like that freshness is closed 
          over permutation action.

alpha_equivalence.pvs concerns alpha-equivalence, that is defined recursively 
          as the function ``alpha". The function alpha tests if two terms are 
          alpha-equivalent in a specific context. It is proved that alpha is 
          an equivalence relation. 

substitution.pvs deals with substitutions (acting over variables only) and some 
          basic properties. There is a function named ``fresh_subs?" which apply 
          a substitution to a freshness context in the sense that, for each pair 
          (atom x variable) in the original context, it verifies if the atom is 
          fresh in the term obtained by applying the substitution to the 
          variable. This verification and the building of a proper new context 
          is made recursively by the function ``fresh?". The function ``fresh_subs?" 
          is used in the unification algorithm in order to update freshness 
          contexts. There are a number of auxiliary lemmas that are used in the
          formalization of the algorithm that were specified in this file. 

nominalunif.pvs It is 
          provided an algorithm through the function "c_unify" to test if two 
          terms are unifiable and generate a correct and complete set of solutions. 
          Termination, soundness and completeness of this algorithm are already proved.

structure_extra.pvs includes auxiliary lemmas related with properties of 
          lists, non straightforwardly related with the nominal unification
          theory.

The hierarchy of this theory is given as below, where "V" means that the 
theory above imports the theory below:

                        nominalunif
                             |
                             V
                        substitution
                             |
                             V
                      alpha_equivalence
                             |
                             V
                         freshness
                             |
                             V
                        nominal_basis
                         /    |     \
                        |     |      |
                        V     |      V
                     atoms    |    terms
                        |     |   
                        V     V   
                       structure_extra

