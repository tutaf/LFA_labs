import copy
import unittest
from Grammar import Grammar


def generate_expressions(grammar, start_symbol, depth_limit):
    if depth_limit == 0:
        return set()  # Avoid infinite recursion by stopping at a depth limit

    expressions = set()
    if start_symbol not in grammar.productions:
        return expressions  # If no production rules, return empty set

    for production in grammar.productions[start_symbol]:
        # If production is a terminal
        if all(symbol.islower() or symbol == 'ε' for symbol in production):
            expressions.add(''.join(symbol for symbol in production if symbol != 'ε'))
        else:
            # Generate combinations of nonterminal expansions
            current_combinations = ['']
            for symbol in production:
                new_combinations = []
                if symbol.islower():  # Terminal
                    for combo in current_combinations:
                        new_combinations.append(combo + symbol)
                else:  # Non-terminal
                    expansions = generate_expressions(grammar, symbol, depth_limit - 1)
                    if not expansions:  # If no expansions, continue with what we have
                        expansions = ['']
                    for combo in current_combinations:
                        for expansion in expansions:
                            new_combinations.append(combo + expansion)
                current_combinations = new_combinations
            expressions.update(current_combinations)

    return expressions


def compare_grammars(grammar1, grammar2, depth_limit):
    expressions1 = generate_expressions(grammar1, grammar1.start_symbol, depth_limit)
    expressions2 = generate_expressions(grammar2, grammar2.start_symbol, depth_limit)

    # Compare sets of expressions
    if expressions1 == expressions2:
        return True
    else:
        return False


class TestSTART(unittest.TestCase):

    def test1(self):
        grammar = Grammar("S",
                          {
                              "S": [["a", "S"], ["b"]]
                          })

        grammar = self.perform_basic_actions(grammar)

        self.assertIn(grammar.start_symbol, grammar.productions)
        self.assertEqual(grammar.productions[grammar.start_symbol], [["S"]])
        self.assertNotEqual(grammar.start_symbol, "S")

    def test2(self):
        grammar = Grammar("S",
                          {
                              "S": [["S"], ["b"]],
                              "A": [["S"]]
                           })

        grammar = self.perform_basic_actions(grammar)

        for lhs in grammar.productions.keys():
            self.assertTrue(grammar.start_symbol not in grammar.productions[lhs])

    def perform_basic_actions(self, grammar):
        print(f"before: \n{grammar}")
        print(generate_expressions(grammar, grammar.start_symbol, 3))
        original_grammar = copy.deepcopy(grammar)
        grammar.eliminate_start_symbol()
        print(f"\n\n\nafter: \n{grammar}")
        print(generate_expressions(grammar, grammar.start_symbol, 3))
        self.assertTrue(compare_grammars(original_grammar, grammar, 3),
                        "The grammars should generate the same language after transformation.")
        return grammar


class TestTERM(unittest.TestCase):
    def test_term_single_occurrence(self):
        grammar = Grammar("S",
                          {
                              "S": [["a", "S", "b"], ["b"]]
                          })

        grammar = self.perform_basic_actions(grammar)

        self.assertIn("N_a", grammar.productions)
        self.assertIn("N_b", grammar.productions)
        self.assertEqual(grammar.productions["N_a"], [["a"]])
        self.assertEqual(grammar.productions["N_b"], [["b"]])
        self.assertEqual(grammar.productions["S"], [["N_a", "S", "N_b"], ["b"]])

    def test_term_multiple_occurrences(self):
        grammar = Grammar("S",
                          {
                              "S": [["a", "X", "a", "b"], ["c"]]
                          })

        grammar = self.perform_basic_actions(grammar)

        self.assertIn("N_a", grammar.productions)
        self.assertIn("N_b", grammar.productions)
        self.assertEqual(grammar.productions["N_a"], [["a"]])
        self.assertEqual(grammar.productions["N_b"], [["b"]])
        self.assertEqual(grammar.productions["S"], [["N_a", "X", "N_a", "N_b"], ["c"]])

    def test_term_no_change_needed(self):
        grammar = Grammar("S",
                          {
                              "S": [["N_a"], ["b"]],
                              "N_a": [["a"]]
                          })
        grammar = self.perform_basic_actions(grammar)
        self.assertNotIn("N_b", grammar.productions)
        self.assertEqual(grammar.productions["S"], [["N_a"], ["b"]])

    def test_term_empty_productions(self):
        grammar = Grammar("S", {})
        grammar = self.perform_basic_actions(grammar)
        self.assertEqual(grammar.productions, {})


    def perform_basic_actions(self, grammar):
        print(f"before: \n{grammar}")
        print(generate_expressions(grammar, grammar.start_symbol, 3))
        original_grammar = copy.deepcopy(grammar)
        grammar.eliminate_nonsolitary_terminals()
        print(f"\n\n\nafter: \n{grammar}")
        print(generate_expressions(grammar, grammar.start_symbol, 3))
        self.assertTrue(compare_grammars(original_grammar, grammar, 3),
                        "The grammars should generate the same language after transformation.")
        return grammar


class TestBIN(unittest.TestCase):
    def test_bin_basic_split(self):
        grammar = Grammar("S",
                          {
                              "S": [["A", "B", "C", "D"]]
                          })
        grammar = self.perform_basic_actions(grammar)

        # We expect S -> A A1, A1 -> B A2, A2 -> C D
        self.assertEqual(len(grammar.productions["S"]), 1)
        self.assertTrue(len(grammar.productions["S"][0]) == 2)
        self.assertTrue(all(len(rhs) == 2 for rhs_list in grammar.productions.values() for rhs in rhs_list))

    def test_bin_no_split_needed(self):
        grammar = Grammar("S",
                          {
                              "S": [["A", "B"], ["C"]]
                          })
        grammar = self.perform_basic_actions(grammar)

        self.assertEqual(grammar.productions["S"], [["A", "B"], ["C"]])

    def test_bin_complex_case(self):
        grammar = Grammar("S",
                          {
                              "S": [["A", "B", "C", "D", "E", "F"]]
                          })

        grammar = self.perform_basic_actions(grammar)

        self.assertEqual(len(grammar.productions["S"]), 1)
        self.assertTrue(len(grammar.productions["S"][0]) == 2)
        non_terminals = [prod for nt, prods in grammar.productions.items() for prod in prods if nt != "S"]
        self.assertTrue(all(len(prod) == 2 for prod in non_terminals))

    def test_bin_length_check(self):
        grammar = Grammar("S",
                          {
                              "S": [["A", "B", "C", "D", "E"]]
                          })
        grammar = self.perform_basic_actions(grammar)

        # We expect transformations but focus on verifying the rule lengths.
        for production_list in grammar.productions.values():
            for production in production_list:
                self.assertTrue(len(production) <= 2)

    def perform_basic_actions(self, grammar):
        print(f"before: \n{grammar}")
        print(generate_expressions(grammar, grammar.start_symbol, 3))
        original_grammar = copy.deepcopy(grammar)
        grammar.eliminate_rhs_with_more_than_two_nonterminals()
        print(f"\n\n\nafter: \n{grammar}")
        print(generate_expressions(grammar, grammar.start_symbol, 3))
        self.assertTrue(compare_grammars(original_grammar, grammar, 3),
                        "The grammars should generate the same language after transformation.")
        return grammar

class TestDEL(unittest.TestCase):
    def test_eliminate_simple_epsilon(self):
        grammar = Grammar("S",
                          {
                              "S": [["A", "B"], ["ε"]],
                              "A": [["a"], ["ε"]],
                              "B": [["b"]]
                          })
        print(f"before: \n{grammar}")

        original_grammar = copy.deepcopy(grammar)
        grammar.eliminate_epsilon_rules()
        print(f"\n\n\nafter: \n{grammar}")

        # Verify that the transformed grammar preserves the language
        self.assertTrue(compare_grammars(original_grammar, grammar, 3),
                        "The grammars should generate the same language after transformation.")

        # Ensure ε is correctly handled
        self.assertNotIn(["ε"], grammar.productions["A"])
        self.assertNotIn(["ε"], grammar.productions["B"])
        self.assertIn(["ε"], grammar.productions["S"])

    def test_preserve_start_symbol_epsilon(self):
        grammar = Grammar("S",
                          {
                              "S": [["S", "B"], ["ε"]],
                              "B": [["b"], ["B", "S"]]
                          })
        print(f"before: \n{grammar}")

        original_grammar = copy.deepcopy(grammar)
        grammar.eliminate_epsilon_rules()
        print(f"\n\n\nafter: \n{grammar}")

        # Ensure the transformation preserves language generation
        self.assertTrue(compare_grammars(original_grammar, grammar, 3),
                        "The grammars should generate the same language after transformation.")

        # Ensure ε is still correctly present in the start symbol productions
        self.assertIn(["ε"], grammar.productions["S"])

    def test_eliminate_epsilon_with_nullable_nonterminals(self):
        grammar = Grammar("S",
                          {
                              "S": [["A", "B"]],
                              "A": [["a"], ["ε"]],
                              "B": [["b"], ["ε"]]
                          })

        print(f"before: \n{grammar}")
        print(generate_expressions(grammar, grammar.start_symbol, 3))
        original_grammar = copy.deepcopy(grammar)
        grammar.eliminate_epsilon_rules()
        print(f"\n\n\nafter: \n{grammar}")
        print(generate_expressions(grammar, grammar.start_symbol, 3))
        self.assertTrue(compare_grammars(original_grammar, grammar, 3),
                        "The grammars should generate the same language after transformation.")

        # Ensure all nullable productions are expanded properly
        self.assertIn(["ε"], grammar.productions["S"])
        self.assertNotIn(["ε"], grammar.productions["A"])
        self.assertNotIn(["ε"], grammar.productions["B"])

    def test_no_epsilon_to_eliminate(self):
        grammar = Grammar("S",
                          {
                              "S": [["A", "B"]],
                              "A": [["a"]],
                              "B": [["b"]]
                          })
        print(f"before: \n{grammar}")
        print(generate_expressions(grammar, grammar.start_symbol, 3))

        original_grammar = copy.deepcopy(grammar)
        grammar.eliminate_epsilon_rules()
        print(f"\n\n\nafter: \n{grammar}")
        print(generate_expressions(grammar, grammar.start_symbol, 3))


        # Ensure no changes when there are no ε rules
        self.assertTrue(compare_grammars(original_grammar, grammar, 3),
                        "The grammars should remain identical after transformation.")
        self.assertEqual(grammar.productions, original_grammar.productions)


if __name__ == "__main__":
    unittest.main()
