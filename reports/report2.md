# Report: Determinism in Finite Automata and Conversion from NDFA to DFA

### Course: Formal Languages & Finite Automata
### Author: Andrei Cernisov
#### Variant 3

----

## Theory

In this lab, we delve into the concepts of determinism and non-determinism within the context of finite automata. A finite automaton can be seen as a state machine that processes input sequences to determine if they belong to a specific language. The essence of determinism in this context lies in the predictability of the system's response to a given input. Conversely, non-determinism introduces a layer of complexity where multiple states can be reached from a given state under the same input condition.

The lab also explores the Chomsky Hierarchy and representation of Finite Automaton through a Regular Grammar. An integral part of the lab is the practical implementation of algorithms that can convert non-deterministic finite automata (NDFA) into deterministic finite automata (DFA), a process crucial for simplifying and analyzing automata.

## Objectives

1. **To grasp the fundamental concepts of finite automata**, including their deterministic and non-deterministic forms, and to understand their applications in representing languages.
2. **To implement a conversion from a finite automaton to a regular grammar**, thereby bridging the conceptual gap between automata and grammatical representations of languages.
3. **To classify grammars based on the Chomsky hierarchy**, providing a practical understanding of the theoretical underpinnings of language representation.
4. **To convert an NDFA to a DFA**, showcasing the algorithmic approach to achieving determinism in automata.
5. **To graphically represent finite automata** as an optional task to visually comprehend the transitions and states involved.

## Implementation Description

The implementation involved the creation of two primary classes: `FiniteAutomaton` and `Grammar`. The `FiniteAutomaton` class encapsulates the definition of a finite automaton, including its states, alphabet, final states, and transition function. A method within this class, `convert_to_grammar`, enables the conversion of the automaton to a regular grammar. This method adheres to the principles of creating a right-linear grammar from the given automaton.

The `Grammar` class represents the structure of a grammar, containing non-terminals, terminals, and production rules. It includes a method, `classify`, to determine the Chomsky hierarchy type of the grammar, crucial for understanding the grammar's complexity and capabilities.

A significant part of the implementation was the `is_deterministic` method in the `FiniteAutomaton` class, which checks the determinism of the automaton. This method is essential for identifying whether an automaton requires conversion to a DFA.

### Code Snippets

**FiniteAutomaton to Grammar Conversion:**
```python
class FiniteAutomaton:
    ...
    def convert_to_grammar(self):
        VN = self.Q
        VT = self.E
        P = {}

        for q in self.Q:  #initializing production rules for each non terminal
            P[q] = []

        # converting transitions to productions
        for state, transitions in self.sigma.items():
            for transition in transitions:
                input_symbol, next_state = transition
                P[state].append(input_symbol + next_state)

        # adding empty production for final states
        for final_state in self.F:
            if '' not in P[final_state]:
                P[final_state].append('')

        return Grammar(VN, VT, P)
```

**Determining Automaton Determinism:**
```python
class FiniteAutomaton:
    ...
    def is_deterministic(self):
        for state, transitions in self.sigma.items():
            seen_symbols = set()
            for transition in transitions:
                symbol = transition[0]
                # encountering the same symbol more than once means it's NFA
                if symbol in seen_symbols:
                    return False
                seen_symbols.add(symbol)
        # we haven't seen any symbol more than once - this is DFA
        return True
```

**Grammar Classification:**
```python
class Grammar:
    ...
    def classify(self):
        is_type_3 = True
        is_type_2 = True

        for left, productions in self.P.items():
            if len(left) != 1:
                # this violates rules for type 2 and 3 (only 1 non-terminal on the left)
                is_type_2 = False
                is_type_3 = False
                break

            for production in productions:
                if not production:
                    # empty production is fine for type 2 but not for 3
                    is_type_3 = False
                elif len(production) == 2 and production[1] in self.VN:
                    # A -> aB  -  this is okay for type 3
                    continue
                elif len(production) == 1 and production[0] in self.VT:
                    # A -> a  -  also okay for type 3
                    continue
                else:
                    # failing both of the previous 2 checks means this isn't a type 3 grammar
                    is_type_3 = False

        if is_type_3:
            return 3  # regular
        elif is_type_2:
            return 2  # context free grammar
        else:
            for left, productions in self.P.items():
                for production in productions:
                    if len(left) <= len(production):
                        pass
                    else:
                        return 0 # recursively enumerable grammar
            return 1  # context sensivive grammar
```

## Evaluation and Conclusions

The lab successfully achieved its objectives, demonstrating the theoretical concepts of determinism and the Chomsky hierarchy through practical implementations. The conversion from a finite automaton to a regular grammar and the classification of grammars based on the Chomsky hierarchy were particularly insightful, providing a hands-on understanding of these concepts.

Additionally, the process of converting an NDFA to a DFA, although not detailed in this report, is a critical skill in automata theory and its applications. The optional task of graphically representing finite automata offers a visual understanding of the automata's structure and transitions, which can be beneficial for comprehension and analysis.

Overall, this lab has laid a solid foundation for understanding finite automata, their classifications, and their representations through grammars, serving as a stepping stone for more advanced studies in formal languages and automata theory.