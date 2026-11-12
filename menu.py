from main import solve
from converter import to_clause_list
import os

#LINE_UP = '\033[1A'
#LINE_CLEAR = '\x1b[2K'
#
#def clear_lines(n):
#    for _ in range(n):
#        print(LINE_UP, end=LINE_CLEAR)

def print_start():

    print(r'''
    /$$$$$$$  /$$$$$$$  /$$       /$$              /$$$$$$              /$$                               /$$                              
    | $$__  $$| $$__  $$| $$      | $$             /$$__  $$            | $$                              | $$                              
    | $$  \ $$| $$  \ $$| $$      | $$            | $$  \__/  /$$$$$$  /$$$$$$          /$$$$$$$  /$$$$$$ | $$ /$$    /$$ /$$$$$$   /$$$$$$ 
    | $$  | $$| $$$$$$$/| $$      | $$            |  $$$$$$  |____  $$|_  $$_/         /$$_____/ /$$__  $$| $$|  $$  /$$//$$__  $$ /$$__  $$
    | $$  | $$| $$____/ | $$      | $$             \____  $$  /$$$$$$$  | $$          |  $$$$$$ | $$  \ $$| $$ \  $$/$$/| $$$$$$$$| $$  \__/
    | $$  | $$| $$      | $$      | $$             /$$  \ $$ /$$__  $$  | $$ /$$       \____  $$| $$  | $$| $$  \  $$$/ | $$_____/| $$      
    | $$$$$$$/| $$      | $$$$$$$$| $$$$$$$$      |  $$$$$$/|  $$$$$$$  |  $$$$/       /$$$$$$$/|  $$$$$$/| $$   \  $/  |  $$$$$$$| $$      
    |_______/ |__/      |________/|________/       \______/  \_______/   \___/        |_______/  \______/ |__/    \_/    \_______/|__/      
    ''') 
    print("\n\n")
    print("\t\t\t\t\t\t\t\t Angad Bisen\n\t\t\t\t\t\t\t\t BSMA1250031\n\t\t\t\t\t\t\t\tFinal Project\n\n")

    print("1. Enter a logical expression in the following format:\n")
    print("A & B will be written as A AND B\nA | B will be written as A OR B\n~A will be written as NEG(A)\nA -> B will be written as A IMP B\nA <-> B will be written as A EQUIV TO B\n")
    print("2. Each letter in the alphabet represents a variable. You can use any number of variables in your expression.\n")
    print("3. Each subexpression must be enclosed in parentheses. For example, '(A AND B) OR (C IMP NEG(D))' is a valid expression, '(A AND B) OR B IMP C' is not\n")
    print("4. All literals must be represented by capitals letters A through B. Therefore, the solver can solve for 26 literals.\n")


print_start()
while True:
    expression = input("Enter a logical expression to check for satisfiability (or type 'exit' to quit): ")

    if expression.lower() == "exit":
        break

    elif any(c.islower() for word in [i for i in expression] for c in word):
             print("Please enter capital letters for literals!")
    else:
        try:
            clause_list = to_clause_list(expression)
            print(f"Clause List: {clause_list}")
            result, assignment = solve(clause_list)
            if result:
                print("The expression is satisfiable and the following assignment of truth values satisfies the expression:")
                for i, j in assignment.items():
                    print(f"{i} = {j}")
            else:
                print("The expression is unsatisfiable.")
            
            user_input = input("Press enter to try another! ")
            os.system("cls")
            print_start()

        except Exception as e:
            print(f"Error: {e}. Please enter a valid logical expression.")
