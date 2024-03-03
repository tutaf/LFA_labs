from Grammar import Grammar

class FiniteAutomaton:
    # def __init__(self):
    #     self.Q = ['q0', 'q1', 'q2', 'q3', 'q4']
    #     self.E = ['a', 'b']
    #     self.F = ['q4']
    #     self.sigma = {
    #         'q0': [['a', 'q1']],
    #         'q1': [['b', 'q1'], ['a', 'q2']],
    #         'q2': [['b', 'q2'], ['b', 'q3']],
    #         'q3': [['b', 'q4'], ['a', 'q1']]
    #     }

    def __init__(self):
        self.Q = ['0', '1', '2', '3', '4']  # I replaced 'qX' strings with just 'X' because of Grammar class incorrectly
        self.E = ['a', 'b']                 # handling strings that are longer than 1 character
        self.F = ['4']
        self.sigma = {
            '0': [['a', '1']],
            '1': [['b', '1'], ['a', '2']],
            '2': [['b', '2'], ['b', '3']],
            '3': [['b', '4'], ['a', '1']]
        }

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
        # TODO fix Grammar.classify incorrectly identifying grammar type as 2
        for final_state in self.F:
            if '' not in P[final_state]:
                P[final_state].append('')

        return Grammar(VN, VT, P)

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

