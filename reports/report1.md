# Report: Introduction to Formal Languages

### Course: Formal Languages & Finite Automata
### Author: Andrei Cernisov

----

## Theory

Here are some relevant definitions:
* **Alphabet:** A set of symbols used to create valid strings within the language
* **Vocabulary:**  Collection of valid words or combinations of symbols
* **Grammar:** The rules that determine how symbols can be combined to form valid expressions in the language

## Objectives:

* To understand the concept of formal languages
* Implement a basic grammar in code
* Generate valid strings from the defined grammar

## Implementation Description

I used Python to implement the given grammar. The code defines a `Grammar` class to represent the grammar's components (non-terminals, terminals, and production rules). It includes a function to generate random valid strings from the grammar by starting with the start symbol and recursively applying production rules until all non-terminals are replaced with terminals.
```python
import random

class Grammar:
    def __init__(self):
        self.VN = ['S', 'D', 'R']
        self.VT = ['a', 'b', 'c', 'd', 'f']
        self.P = {
            'S': ['aS', 'bD', 'fR'],
            'D': ['cD', 'dR', 'd'],
            'R': ['bR', 'f']
        }


def print_strings(number_of_strings):
    grammar = Grammar()
    for i in range(number_of_strings):
        start = grammar.VN[0]
        while start[-1] not in grammar.VT:
            t = start[-1]
            start = start[:-1] + random.choice(grammar.P[t])
        print(start)

print_strings(5)
```

* **Grammar Class:** A `Grammar` class stores the non-terminals (`VN`), terminals (`VT`), and production rules (`P`) which define the language.
* **String Generation:** A function generates random valid strings. It does this:
    1. Starts with the start symbol ('S').
    2. Repeatedly replaces non-terminal symbols with a random production rule.
    3. Continues until all symbols in the string are terminals.

## Conclusions 

I successfully implemented the grammar and a function that generates valid strings.