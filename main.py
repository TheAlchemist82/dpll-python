#DPLL solves CNF-SAT problems.
#The algorithm takes in an input of clauses represented by a set of, sets of letters, and returns true if the sentence is satisfiable and false if it is not.

#The input [["a", "~b", "c"],["~a"],["c", "b"],["a", "c"]] represents the sentence (A OR notB OR C) AND (notA) AND (C OR B) AND (A OR C)

#UNIT PROPOGATION: If a literal appears alone in a clause, it must be set to true for the sentence to be satisfiable. Automatically set it to true, and accordingly any other instance of the literal can be set either to true or false given wheter it appears with a negation or not.

import copy


def falseRemover(sentence):
    return [[item for item in sublist if item != 0] for sublist in sentence]

def trueRemover(sentence):
    return [i for i in sentence if 1 not in i]

def unitPropogation(sentence, assignment):
    counting_unit_clauses = {i[0] for i in sentence if len(i) == 1}

    #The unit_clause dictionary comprehension code was generated partly by Gemini
    for lit in counting_unit_clauses:
        if not lit.startswith("~") and f"~{lit}" in counting_unit_clauses:
            return None
        
    unit_clause = {}
    for lit in counting_unit_clauses:
        negated = lit.startswith("~")
        base = lit.lstrip("~")
        assignment[base] = not negated #recording the truth value
        unit_clause[lit] = 1
        unit_clause[base if negated else f"~{lit}"] = 0
        
    sentence = [[unit_clause.get(l,l ) for l in clause] for clause in sentence]
    #More efficient way to rebuild the sentence found using Claude.
    
    #looks through the nested sub-lists and finds whether the literal is unit or not. If it is, it will make it equal to whatever value it needs to be assigned (0 or 1 depending on whether it appears with a negation or not.)


    return falseRemover(trueRemover(sentence))


#PURE LITERALS: If a literal occurs with only one sign (only with negation or purely on its own), assign it true and its negation false.

def pureLiteral(sentence, assignment):
    flatlist = [item for sublist in sentence for item in sublist]
    pure = {}
    for lit in flatlist:
        negated = lit.startswith("~")
        base = lit.lstrip("~")
        opposite = base if negated else f"~{base}"
        if opposite not in flatlist:
            pure[lit] = 1
            assignment[base] = not negated #recording the truth value

    #for i in sentence:
    #    for j in i:
    #        if j in pure:
    #            i[i.index(j)] = pure[j]

    sentence = [[pure.get(l,l ) for l in clause] for clause in sentence]


    return falseRemover(trueRemover(sentence))


#MOM Heuristic: Maximum occurences on minimum sized clauses is a way to choose which variable to branch on rather than just choosing one at random. It checks the length of each clause and 

def MOM(sentence):

    length = [len(c) for c in sentence if len(c) > 0]

    if not length: return None
    min_len = min(length)

    min_clause = [c for c in sentence if len(c) == min_len]
    flat_min = [item for sublist in min_clause for item in sublist if isinstance(item, str)]

    #score computed by mom heuristic to find which variable to branch on.
    def score(x):
        base = x.lstrip("~")
        count_x = flat_min.count(base)
        count_notx = flat_min.count(f"~{base}")
        return (count_x + count_notx)*10 + (count_x * count_notx)

    return max(flat_min, key=score, default=None)

def apply_assignment(sentence, literal, value, assignment):
    base = literal.lstrip("~")
    negated = literal.startswith("~")
    assignment[base] = not value if negated else value #recording the truth value of the base literal
    var_assignments = {}

    if literal.startswith("~"):
        if value:
            var_assignments[base] = 0
            var_assignments[literal] = 1
        else:
            var_assignments[base] = 1
            var_assignments[literal] = 0
    else:
        if value:
            var_assignments[base] = 1
            var_assignments[f"~{literal}"] = 0
        else:
            var_assignments[base] = 0
            var_assignments[f"~{literal}"] = 1

#    for i in new_sentence:
#        for j in i:
#            if j in var_assignments:
#                i[i.index(j)] = var_assignments[j]
#
    new_sentence = [[var_assignments.get(l,l ) for l in clause] for clause in sentence]

    return falseRemover(trueRemover(new_sentence))


def isSat(sentence):

    if len(sentence) == 0:
        return True

    if [] in sentence:
        return False

    return sentence


def dpll(sentence, assignment=None):
    assignment = dict(assignment) if assignment else {}
    
    status = isSat(sentence)
    if isinstance(status, bool): return (True, assignment) if status else (False, None)

    while True:
        old_sentence = copy.deepcopy(sentence)

        sentence = unitPropogation(sentence, assignment)
        if sentence is None: return (False, None) #Check for contradictions after unit propogation
        sentence = pureLiteral(sentence, assignment)

        status = isSat(sentence)
        if isinstance(status, bool): return (True, assignment) if status else (False, None)

        if sentence == old_sentence: break

    literal = MOM(sentence)
    if literal is None: return False, None

    #Backtracking
   # sentence_true = apply_assignment(sentence, literal, True)
   # if dpll(sentence_true): return True

   # sentence_false = apply_assignment(sentence, literal, False)
   # return dpll(sentence_false)

   #New implementation of backtracking
    for value in (True, False):
        branch = dict(assignment)  # Create a copy of the current assignment for each branch
        new_sentence = apply_assignment(sentence, literal, value, branch)
        result, final_assignment = dpll(new_sentence, branch)
        if result:
            return (True, final_assignment)

    return False, None

def solve(sentence):
    all_vars = {l.strip("~") for clause in sentence for l in clause}
    sat, model = dpll(copy.deepcopy(sentence))
    if not sat:
        return False, None 
    for v in all_vars:
        model.setdefault(v, False) #all variables that have no bearing on satisfiability are set to false
    return True, model


#print(trueRemover(falseRemover(pureLiteral(unitPropogation(([["~b", "c"],["~c"],["a","~b","e"],["d", "b"], ["e","a","~c"]]))))))
#print(trueRemover(falseRemover(pureLiteral(unitPropogation(([["~b", "c", "a"],["~c", "a"],["a","~b","~e"],["d", "b"], ["~d", "e","a","~c"]]))))))
#print((((unitPropogation(([["b", "a", "~a"], ["~b", "~c", "d"], ["c", "b"]]))))))
#print((((pureLiteral(([["b", "d", "~a"], ["~b", "~c", "d"], ["c", "b"]]))))))
#print(isSat(unitPropogation([["a"], ["~a"]])))

#print(dpll([["a", "~b", "c"],["~a"],["c", "~a"],["a", "c"]]))
#print((((dpll(([["a", "~b", "c"],["~c", "d", "~e"],["~a", "~b", "e"],["d", "b"],["e", "a", "~c"]]))))))
#print(dpll([["a"], ["~a"]]))
#print(dpll([["a", "~b"], ["b", "~a"]]))



#print(isSatYet(pureLiteral(unitPropogation(([["a", "~b", "c"],["~a"],["c", "~a"],["a", "c"]])))))
#print(unitPropogation([["a", "~b", "c"],["c", "b"],["a", "c"]]))
