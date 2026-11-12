from sympy import symbols, to_cnf
from sympy import And, Or, Not, Implies, Equivalent

import re

A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z = symbols("A B C D E F G H I J K L M N O P Q R S T U V W X Y Z")

def parse_to_syntax(tokens):
    
    if not tokens:
        raise ValueError("Incorrect Expression.")

    token = tokens.pop(0)

    if token == "(":
        left = parse_to_syntax(tokens)
    
        if len(tokens) == 0:
            raise IndexError("Enter an expression.")

        op = tokens.pop(0)
    

        if op == ")":
            return left 

        right = parse_to_syntax(tokens)
        closing = tokens.pop(0)

        if closing != ")":
            raise ValueError(f"Expected ')', found '{closing}'")

        if op == "AND": return left & right
        if op == "OR": return left | right
        if op == "IMP": return Implies(left, right)
        if op == "EQUIV": return Equivalent(left, right)
        raise ValueError(f"Unknown binary operator: '{op}'")

    elif token == "NEG":
        return ~parse_to_syntax(tokens) 

    else:
        return symbols(token)

def to_clause_list(sentence):

    cleaned_sentence = f"({sentence})"
    tokens = re.findall(r'\(|\)|\b[A-Z0-9_]+\b', cleaned_sentence)

    expr = parse_to_syntax(tokens)

    cnf = to_cnf(expr)

    clauses = cnf.args if isinstance(cnf, And) else [cnf]
    clause_list = []
    for clause in clauses:
        literals = clause.args if isinstance(clause, Or) else [clause]
        clause_list.append([str(l) for l in literals])

    return clause_list

    
    

#sentence1 = "((NEG(A) IMP B) AND (B EQUIV C))"
#sentence2 = "(( NEG (A AND B) OR (B IMP C) ) EQUIV ((B AND C) OR NEG(C)))"
#sentence3 = "A AND NEG(A)" #[["A"], ["~A"]]
#sentence4 = ""
#
#result1 = to_clause_list(sentence1)
#result2 = to_clause_list(sentence2)
#result3 = to_clause_list(sentence3)
#
#print(result1)
#print(result2)
#print(result3)
