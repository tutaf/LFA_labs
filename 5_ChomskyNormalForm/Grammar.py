class Grammar:
    def __init__(self, start_symbol, productions=None):
        self.start_symbol = start_symbol
        self.productions = productions if productions is not None else {}

    def add_production(self, nonterminal, rhs):
        if nonterminal not in self.productions:
            self.productions[nonterminal] = []
        self.productions[nonterminal].append(rhs)

    def to_cnf(self):
        self.eliminate_start_symbol()
        self.eliminate_nonsolitary_terminals()
        self.eliminate_rhs_with_more_than_two_nonterminals()
        self.eliminate_epsilon_rules()
        self.eliminate_unit_rules()

    def eliminate_start_symbol(self):
        """ Eliminates S (start symbol) from RHS by turning it into a non-terminal and creating a new start symbol """
        new_start_symbol = self.start_symbol + "0"                  # ensure the new start symbol is unique
        self.productions[new_start_symbol] = [[self.start_symbol]]  # add new start rule
        self.start_symbol = new_start_symbol                        # update the start symbol to the new one

    def eliminate_nonsolitary_terminals(self):
        pass

    def eliminate_rhs_with_more_than_two_nonterminals(self):
        pass

    def eliminate_epsilon_rules(self):
        pass

    def eliminate_unit_rules(self):
        pass

    def __str__(self):
        return "\n".join(f"{nt} -> {' | '.join(' '.join(sym for sym in prod) for prod in prods)}"
                         for nt, prods in self.productions.items())
