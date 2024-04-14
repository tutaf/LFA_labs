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
        """Eliminates S (start symbol) from RHS by turning it into a non-terminal and creating a new start symbol"""
        new_start_symbol = self.start_symbol + "0"                  # ensure the new start symbol is unique
        self.productions[new_start_symbol] = [[self.start_symbol]]  # add new start rule
        self.start_symbol = new_start_symbol                        # update the start symbol to the new one

    def eliminate_nonsolitary_terminals(self):
        """Eliminate terminals from RHS if they exist with other terminals or non-terminals"""
        # dict to store new nonterminal mappings for terminals
        terminal_to_nonterminal = {}

        # temporary dictionary to accumulate new rules to be added after the loop
        additional_productions = {}

        # cloning productions
        new_productions = {nt: [list(rhs) for rhs in rhs_list] for nt, rhs_list in self.productions.items()}

        for nonterminal, rhs_list in new_productions.items():
            for rhs in rhs_list:
                for i, symbol in enumerate(rhs):
                    if symbol.islower() and len(rhs) > 1:  # it's a terminal and not solitary
                        if symbol not in terminal_to_nonterminal:
                            # create a new nonterminal for this terminal if not already created
                            new_nonterminal = f'N_{symbol}'
                            terminal_to_nonterminal[symbol] = new_nonterminal
                            additional_productions[new_nonterminal] = [[symbol]]
                        # replace the terminal with nonterminal in RHS
                        rhs[i] = terminal_to_nonterminal[symbol]

        # add new productions for new nonterminals to the main productions dict
        for nonterminal, rules in additional_productions.items():
            if nonterminal in new_productions:
                new_productions[nonterminal].extend(rules)
            else:
                new_productions[nonterminal] = rules

        self.productions = new_productions

    def eliminate_rhs_with_more_than_two_nonterminals(self):
        """Eliminates all productions with more than 2 symbols by creating new productions"""
        # temp dict to store new rules
        new_productions = {nt: [] for nt, _ in self.productions.items()}

        count = 0  # a counter to create unique names

        for nonterminal, rhs_list in self.productions.items():
            for rhs in rhs_list:
                if len(rhs) > 2:
                    current_nonterminal = nonterminal
                    remaining_rhs = rhs[:]

                    # create new rules until only two symbols are left in the remaining_rhs
                    while len(remaining_rhs) > 2:
                        # this isn't the best way to create a unique name, but it works
                        new_nonterminal = f"{nonterminal}_BIN{count}"
                        count += 1

                        # ensure the new nonterminal is initialized in the dict
                        if new_nonterminal not in new_productions:
                            new_productions[new_nonterminal] = []

                        # create a new rule
                        new_productions[current_nonterminal].append([remaining_rhs.pop(0), new_nonterminal])
                        current_nonterminal = new_nonterminal

                    # the final production
                    new_productions[current_nonterminal].append(remaining_rhs)
                else:
                    # production is already binary
                    new_productions[nonterminal].append(rhs)

        self.productions = new_productions

    def eliminate_epsilon_rules(self):
        pass

    def eliminate_unit_rules(self):
        pass

    def __str__(self):
        return "\n".join(f"{nt} -> {' | '.join(' '.join(sym for sym in prod) for prod in prods)}"
                         for nt, prods in self.productions.items())
