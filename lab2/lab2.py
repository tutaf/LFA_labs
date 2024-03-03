from Grammar import Grammar
from FiniteAutomaton import FiniteAutomaton


fa = FiniteAutomaton()
g = fa.convert_to_grammar()
g.print1()
print(g.classify())
print(fa.is_deterministic())
