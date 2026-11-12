My project tries to implement the DPLL sat solving algorithm to python and outputs whether a sentence written in propositional logic is satisfiable or not.

The project has three files.
1) **main.py** - The actual DPLL algorithm that takes sentences in CNF and returns the whether they are satisfiable or not along with a the assignment that makes the satisfiable (if it is satisfiable)
2) **converter.py** - The converter function that takes sentences written using regular keywords (AND, OR, IMP, NEG, EQUV) and forms the CNF clause list, by first tokenizing the sentence and then using sympy to convert it into the clause list.
3) **menu.py** - The file that runs both the previous files in tandem

Due to syntactical constraints, I had to be a bit pedantic when it came to usage of parenthesis and the letters that were allowed as literals and those that were not. 


## AI USAGE DISCLAIMER

AI was used in parts for all files to enhance, understand or debug certain aspects of the code. Nothing has been directly taken from any chatbot. Anywhere where a substantial portion was taken from a chatbot, a comment has been left.
I did have to use AI to understand parts of the algorithm so I could implement without making any mistakes, and at points I did take code that it wrote, screenshots for those instances have been attached in the progress reports.

## How to run
Please run the menu.py file in your python env. *sympy* is required as an additional package and can be installed via the following command in the terminal

```pip install sympy```

