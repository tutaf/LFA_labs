# Chomsky Normal Form
### Course: Formal Languages & Finite Automata
### Author: Andrei Cernisov
#### Variant 3

----

## Theory

Chomsky Normal Form is a way of representing context-free grammars in a restricted form. It is named after Noam Chomsky, a linguist who introduced this concept in the field of formal language theory. CNF is a useful representation because it simplifies the structure of a grammar, making it easier to work with and analyze.

In a grammar in Chomsky Normal Form, every production rule must be of one of the following two forms:

1. **Non-terminal to Non-terminals**: A non-terminal symbol on the left-hand side can be rewritten as a sequence of two non-terminal symbols or a single terminal symbol.
   - Example: `A -> BC` or `A -> a`

2. **Start Symbol to Terminal**: The start symbol can be rewritten as an empty string (epsilon, ε).
   - Example: `S -> ε`

This restricted form has several advantages:

1. **Simplicity**: By limiting the structure of production rules, CNF grammars become easier to analyze and work with, especially in parsing algorithms and other formal language applications.

2. **Unambiguity**: Grammars in CNF are inherently unambiguous, meaning that for any given string in the language, there is at most one leftmost derivation.

3. **Parsing Efficiency**: Many parsing algorithms, such as the Cocke-Younger-Kasami (CYK) algorithm, operate more efficiently on grammars in CNF.

4. **Theoretical Significance**: CNF plays an important role in the theoretical study of formal languages and automata theory, as it helps establish relationships between different classes of grammars and languages.

While not all context-free grammars can be directly represented in CNF, it is possible to transform any CFG into an equivalent grammar in Chomsky Normal Form through a series of transformations. These transformations involve eliminating certain types of production rules and introducing new non-terminal symbols as needed.

The process of converting a grammar to CNF typically involves the following steps:

1. **Introduce a New Start Symbol**: If the original start symbol has productions that generate terminal symbols directly, introduce a new start symbol with a single production rule that generates the original start symbol.

2. **Eliminate ε-productions**: Remove any production rules that generate the empty string (ε) directly, except for the start symbol.

3. **Eliminate Unit Productions**: Remove any production rules that have a single non-terminal symbol on the right-hand side.

4. **Eliminate Terminals from the Right-Hand Side**: Replace any production rule that has a terminal symbol along with other symbols on the right-hand side with new non-terminal symbols and corresponding productions.

5. **Eliminate Long Productions**: Replace any production rule that has more than two non-terminal symbols on the right-hand side with new non-terminal symbols and corresponding productions, ensuring that each rule has at most two non-terminal symbols on the right-hand side.


By following these steps, any context-free grammar can be transformed into an equivalent grammar in Chomsky Normal Form, which can then be used for various applications in formal language theory and parsing algorithms.

## Objectives

The main objectives of this laboratory work are:

1. Understand the concept of Chomsky Normal Form and its significance in formal language theory.
2. Learn the steps involved in transforming a context-free grammar into an equivalent grammar in Chomsky Normal Form.
3. Implement a Python program that takes a context-free grammar as input and converts it into an equivalent grammar in Chomsky Normal Form.
4. Test the implemented program with various input grammars to ensure its correctness.

## Implementation Description

The implementation of the Chomsky Normal Form transformation is divided into several functions, each responsible for a specific step in the transformation process. The main components are:

1. `Grammar` class
2. `eliminate_start_symbol` function
3. `eliminate_epsilon_rules` function
4. `eliminate_nonsolitary_terminals` function
5. `eliminate_rhs_with_more_than_two_nonterminals` function
6. `eliminate_unit_rules` function

### 1. `Grammar` Class

The `Grammar` class represents a context-free grammar and provides methods for adding productions and converting the grammar to Chomsky Normal Form.

```python
class Grammar:
    def __init__(self, start_symbol, productions=None):
        self.start_symbol = start_symbol
        self.productions = productions if productions is not None else {}
```

The `__init__` method initializes the grammar with a start symbol and an optional dictionary of productions. The `productions` attribute is a dictionary where the keys are non-terminal symbols, and the values are lists of right-hand side productions for that non-terminal.

```python
    def add_production(self, nonterminal, rhs):
        if nonterminal not in self.productions:
            self.productions[nonterminal] = []
        self.productions[nonterminal].append(rhs)
```

The `add_production` method allows adding new production rules to the grammar. It takes a non-terminal symbol (`nonterminal`) and a right-hand side (`rhs`) as input. If the non-terminal does not exist in the `productions` dictionary, a new entry is created with an empty list. The `rhs` is then appended to the list of productions for that non-terminal.

```python
    def to_cnf(self):
        self.eliminate_start_symbol()
        self.eliminate_epsilon_rules()
        self.eliminate_nonsolitary_terminals()
        self.eliminate_rhs_with_more_than_two_nonterminals()
        self.eliminate_unit_rules()
```

The `to_cnf` method orchestrates the transformation process by calling the respective functions in the correct order to convert the grammar to Chomsky Normal Form.

### 2. `eliminate_start_symbol` Function

```python
def eliminate_start_symbol(self):
    new_start_symbol = self.start_symbol + "0"
    self.productions[new_start_symbol] = [[self.start_symbol]]
    self.start_symbol = new_start_symbol
```

This function introduces a new start symbol by creating a new non-terminal symbol (`new_start_symbol`) and adding a production rule that generates the original start symbol. The `new_start_symbol` is created by appending a "0" to the original start symbol to ensure uniqueness.

The function then adds a new entry to the `productions` dictionary with the `new_start_symbol` as the key and a list containing a single production rule `[self.start_symbol]` as the value. Finally, the `start_symbol` attribute is updated to the `new_start_symbol`.

### 3. `eliminate_epsilon_rules` Function

```python
def eliminate_epsilon_rules(self):
    nullable = set()
    for nonterminal, rhs_list in self.productions.items():
        for rhs in rhs_list:
            if rhs == ['ε']:
                nullable.add(nonterminal)
```

The first part of the function identifies nullable non-terminals, which are non-terminals that can directly generate the empty string (epsilon, `ε`). It iterates over all productions in the grammar and adds the non-terminal to the `nullable` set if it has a production rule that generates `['ε']`.

```python
    changes = True
    while changes:
        changes = False
        for nonterminal, rhs_list in self.productions.items():
            for rhs in rhs_list:
                if all(symbol in nullable for symbol in rhs) and nonterminal not in nullable:
                    nullable.add(nonterminal)
                    changes = True
```

The second part expands the `nullable` set to include non-terminals that can indirectly generate epsilon through a sequence of nullable non-terminals. It iterates over all productions again and checks if all symbols on the right-hand side are nullable. If so, and the current non-terminal is not already in the `nullable` set, it is added to the set, and the `changes` flag is set to `True`. This loop continues until no new nullable non-terminals are found.

```python
    for nonterminal in list(self.productions.keys()):
        self.productions[nonterminal] = [rhs for rhs in self.productions[nonterminal] if rhs != ['ε']]

    for nonterminal in self.productions.keys():
        new_rhs_list = []
        for rhs in self.productions[nonterminal]:
            filtered_rhs = [symbol for symbol in rhs if symbol not in nullable]
            if filtered_rhs:
                new_rhs_list.append(filtered_rhs)
            elif nonterminal == self.start_symbol:
                new_rhs_list.append(['ε'])
        self.productions[nonterminal] = new_rhs_list

    self.productions = {nt: rhs_list for nt, rhs_list in self.productions.items() if rhs_list}
```

The third part removes all epsilon productions from the grammar, except for the start symbol. It first removes any production rule that generates `['ε']` directly. Then, it iterates over all productions again and removes any nullable non-terminals from the right-hand side of each production rule. If the resulting right-hand side is empty and the non-terminal is the start symbol, a production rule `['ε']` is added to allow the start symbol to generate epsilon. Finally, any non-terminals that do not produce anything are removed from the `productions` dictionary.

### 4. `eliminate_nonsolitary_terminals` Function

```python
def eliminate_nonsolitary_terminals(self):
    terminal_to_nonterminal = {}
    additional_productions = {}
    new_productions = {nt: [list(rhs) for rhs in rhs_list] for nt, rhs_list in self.productions.items()}
    for nonterminal, rhs_list in new_productions.items():
        for rhs in rhs_list:
            for i, symbol in enumerate(rhs):
                if symbol.islower() and len(rhs) > 1:
                    if symbol not in terminal_to_nonterminal:
                        new_nonterminal = f'N_{symbol}'
                        terminal_to_nonterminal[symbol] = new_nonterminal
                        additional_productions[new_nonterminal] = [[symbol]]
                    rhs[i] = terminal_to_nonterminal[symbol]
```

This function eliminates any terminal symbols that appear alongside non-terminal symbols on the right-hand side of a production rule. It first creates a dictionary `terminal_to_nonterminal` to store mappings between terminal symbols and new non-terminal symbols that will be introduced.

It then creates a new dictionary `new_productions` by cloning the existing `productions` dictionary. This is done to avoid modifying the original dictionary during the transformation process.

The function iterates over all productions in the `new_productions` dictionary. For each production rule, it checks if there are any terminal symbols (`symbol.islower()`) that are not solitary (i.e., appear with other symbols on the right-hand side, `len(rhs) > 1`). If such a terminal symbol is found and it does not have a corresponding non-terminal symbol in the `terminal_to_nonterminal` dictionary, a new non-terminal symbol (`new_nonterminal`) is created and added to the dictionary, along with a new production rule that generates the terminal symbol.

The terminal symbol in the current production rule is then replaced with the corresponding non-terminal symbol from the `terminal_to_nonterminal` dictionary.

```python
    for nonterminal, rules in additional_productions.items():
        if nonterminal in new_productions:
            new_productions[nonterminal].extend(rules)
        else:
            new_productions[nonterminal] = rules
    self.productions = new_productions
```

Finally, the new production rules for the introduced non-terminal symbols are added to the `new_productions` dictionary. If the non-terminal already exists in the dictionary, the new rules are appended to the existing list of productions. Otherwise, a new entry is created with the new rules.

The `productions` attribute of the `Grammar` object is then updated with the `new_productions` dictionary, effectively eliminating all non-solitary terminals from the grammar.

### 5. `eliminate_rhs_with_more_than_two_nonterminals` Function

```python
def eliminate_rhs_with_more_than_two_nonterminals(self):
    new_productions = {nt: [] for nt, _ in self.productions.items()}
    count = 0
    for nonterminal, rhs_list in self.productions.items():
        for rhs in rhs_list:
            if len(rhs) > 2:
                current_nonterminal = nonterminal
                remaining_rhs = rhs[:]
                while len(remaining_rhs) > 2:
                    new_nonterminal = f"{nonterminal}_BIN{count}"
                    count += 1
                    if new_nonterminal not in new_productions:
                        new_productions[new_nonterminal] = []
                    new_productions[current_nonterminal].append([remaining_rhs.pop(0), new_nonterminal])
                    current_nonterminal = new_nonterminal
                new_productions[current_nonterminal].append(remaining_rhs)
            else:
                new_productions[nonterminal].append(rhs)
    self.productions = new_productions
```

This function ensures that no production rule has more than two non-terminal symbols on the right-hand side. It first creates a new dictionary `new_productions` with the same keys as the original `productions` dictionary but with empty lists as values.

The function then iterates over all productions in the original `productions` dictionary. For each production rule with more than two symbols on the right-hand side (`len(rhs) > 2`), it creates new non-terminal symbols (`new_nonterminal`) and corresponding production rules to break down the long production into a series of shorter productions.

The process works as follows:

1. The current non-terminal (`current_nonterminal`) is set to the non-terminal being processed.
2. A copy of the right-hand side (`remaining_rhs`) is created to avoid modifying the original list.
3. While the length of `remaining_rhs` is greater than 2, a new non-terminal symbol (`new_nonterminal`) is created by appending a unique identifier (`_BIN{count}`) to the original non-terminal name.
4. A new production rule is added to the `new_productions` dictionary, with the `current_nonterminal` as the key and a list containing the first symbol from `remaining_rhs` and the `new_nonterminal` as the value.
5. The `current_nonterminal` is updated to the `new_nonterminal`.
6. The first symbol is removed from `remaining_rhs`.

After the loop, the final production rule with at most two symbols is added to the `new_productions` dictionary under the `current_nonterminal` key.

If the original production rule had two or fewer symbols, it is added to the `new_productions` dictionary without any modifications.

Finally, the `productions` attribute of the `Grammar` object is updated with the `new_productions` dictionary, effectively eliminating all production rules with more than two non-terminal symbols on the right-hand side.

### 6. `eliminate_unit_rules` Function

```python
def eliminate_unit_rules(self):
    unit_productions = {}
    for nonterminal, productions in self.productions.items():
        unit_productions[nonterminal] = [
            rhs[0] for rhs in productions if len(rhs) == 1 and rhs[0].isupper()
        ]

    transitive_closure = {}
    for nonterminal in self.productions:
        transitive_closure[nonterminal] = set()
        stack = [nonterminal]
        while stack:
            current = stack.pop()
            for target in unit_productions.get(current, []):
                if target not in transitive_closure[nonterminal]:
                    transitive_closure[nonterminal].add(target)
                    stack.append(target)
```

The first part of the function identifies all unit productions in the grammar. A unit production is a production rule with a single non-terminal symbol on the right-hand side. The `unit_productions` dictionary stores a list of non-terminal symbols that are the targets of unit productions for each non-terminal.

The second part computes the transitive closure of unit productions for each non-terminal. The `transitive_closure` dictionary stores a set of non-terminals that can be reached from a given non-terminal through a sequence of unit productions. This is done using a depth-first search approach, where a stack is used to keep track of non-terminals to be processed.

```python
    new_productions = {}
    for nonterminal, productions in self.productions.items():
        if nonterminal not in new_productions:
            new_productions[nonterminal] = []
        non_unit_prods = [rhs for rhs in productions if not (len(rhs) == 1 and rhs[0].isupper())]
        new_productions[nonterminal].extend(non_unit_prods)
        for target in transitive_closure[nonterminal]:
            new_productions[nonterminal].extend(
                rhs for rhs in self.productions[target] if not (len(rhs) == 1 and rhs[0].isupper())
            )
    self.productions = new_productions
```

The third part creates a new dictionary `new_productions` to store the updated productions after eliminating unit rules. For each non-terminal, the function first adds all non-unit productions (productions that are not unit productions) to the `new_productions` dictionary.

Then, for each non-terminal in the transitive closure of the current non-terminal, the function adds all non-unit productions of that non-terminal to the `new_productions` dictionary. This effectively replaces unit productions with the productions of their target non-terminals.

Finally, the `productions` attribute of the `Grammar` object is updated with the `new_productions` dictionary, effectively eliminating all unit productions from the grammar.

### Main Program

The `main.py` file contains the code for creating a sample grammar, converting it to Chomsky Normal Form, and printing the resulting grammar at each step of the transformation process.

```python
from Grammar import Grammar

def pretty_print(grammar):
    superscript_map = {
        # ...
    }

    for nonterminal, productions in grammar.productions.items():
        readable_productions = []
        for production in productions:
            readable_production = []
            for symbol in production:
                if '_' in symbol:
                    parts = symbol.split('_')
                    superscript = ''.join(superscript_map.get(char, char) for char in parts[1])
                    readable_production.append(parts[0] + superscript)
                else:
                    readable_production.append(symbol)
            readable_productions.append(' '.join(readable_production))
        print(f"{nonterminal} -> {' | '.join(readable_productions)}")
```

The `pretty_print` function is a helper function that formats the grammar for better readability by converting internal representations to a more human-readable format. It uses a `superscript_map` dictionary to map characters to their superscript equivalents. The function iterates over all productions in the grammar and converts any symbols with an underscore (`_`) to a superscript representation.

```python
grammar = Grammar("S", {
    'S': [['A']],
    'A': [['d'], ['d', 'S'], ['a', 'A', 'd', 'A', 'B']],
    'B': [['a', 'C'], ['a', 'S'], ['A', 'C']],
    'C': [['ε']],
    'E': [['A', 'S']],
})

pretty_print(grammar)
print("\nSTART Transformation:")
grammar.eliminate_start_symbol()
pretty_print(grammar)

print("\nDEL Transformation:")
grammar.eliminate_epsilon_rules()
pretty_print(grammar)

print("\nTERM Transformation:")
grammar.eliminate_nonsolitary_terminals()
pretty_print(grammar)

print("\nBIN Transformation:")
grammar.eliminate_rhs_with_more_than_two_nonterminals()
pretty_print(grammar)

print("\nUNIT Transformation:")
grammar.eliminate_unit_rules()
pretty_print(grammar)
```

The `main.py` file creates a sample grammar and stores it in the `Grammar` object. It then calls the `pretty_print` function to print the initial grammar.

After that, the program applies each transformation step by calling the corresponding methods from the `Grammar` class (`eliminate_start_symbol`, `eliminate_epsilon_rules`, `eliminate_nonsolitary_terminals`, `eliminate_rhs_with_more_than_two_nonterminals`, and `eliminate_unit_rules`). After each transformation, the resulting grammar is printed using the `pretty_print` function.
                              
                              
## Results

The program takes a context-free grammar as input and applies the necessary transformations to convert it into an equivalent grammar in Chomsky Normal Form. Here's an example of the program's output:

```
Initial Grammar:
S -> A
A -> d | d S | a A d A B
B -> a C | a S | A C
C -> ε
E -> A S

START Transformation:
S -> A
A -> d | d S | a A d A B
B -> a C | a S | A C
C -> ε
E -> A S
S0 -> S

DEL Transformation:
S -> A
A -> d | d S | a A d A B
B -> a | a S | A
E -> A S
S0 -> S

TERM Transformation:
S -> A
A -> d | Nᵈ S | Nᵃ A Nᵈ A B
B -> a | Nᵃ S | A
E -> A S
S0 -> S
N_d -> d
N_a -> a

BIN Transformation:
S -> A
A -> d | Nᵈ S | Nᵃ Aᴮᴵᴺ⁰
B -> a | Nᵃ S | A
E -> A S
S0 -> S
N_d -> d
N_a -> a
A_BIN0 -> A Aᴮᴵᴺ¹
A_BIN1 -> Nᵈ Aᴮᴵᴺ²
A_BIN2 -> A B

UNIT Transformation:
S -> d | Nᵈ S | Nᵃ Aᴮᴵᴺ⁰
A -> d | Nᵈ S | Nᵃ Aᴮᴵᴺ⁰
B -> a | Nᵃ S | d | Nᵈ S | Nᵃ Aᴮᴵᴺ⁰
E -> A S
S0 -> d | Nᵈ S | Nᵃ Aᴮᴵᴺ⁰
N_d -> d
N_a -> a
A_BIN0 -> A Aᴮᴵᴺ¹
A_BIN1 -> Nᵈ Aᴮᴵᴺ²
A_BIN2 -> A B
```

In the example output, the initial grammar is first printed, followed by the grammar after each transformation step (START, DEL, TERM, BIN, and UNIT). The final grammar is in Chomsky Normal Form, with all production rules adhering to the required format.

## Conclusion

In this laboratory work, I explored the concept of Chomsky Normal Form. I implemented a Python program that takes a context-free grammar as input and converts it into an equivalent grammar in Chomsky Normal Form through a series of transformations.

The implementation followed the standard steps for converting a grammar to CNF, including eliminating epsilon productions, unit productions, non-solitary terminals, and long productions with more than two non-terminal symbols on the RHS. Additionally, a new start symbol was introduced to handle cases where the original start symbol generated terminal symbols directly.

The program successfully transformed the input grammar into Chomsky Normal Form, as demonstrated by the example output. The resulting grammar adheres to the strict rules of CNF, with each production rule being either of the form "non-terminal to non-terminals" or "start symbol to terminal."

By converting grammars to Chomsky Normal Form, one can simplify their structure and make them more suitable for various applications in formal language theory, such as parsing algorithms and language recognition tasks.

