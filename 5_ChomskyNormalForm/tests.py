import unittest
from Grammar import Grammar


class TestSTART(unittest.TestCase):

    def test1(self):
        grammar = Grammar("S",
                          {
                              "S": [["a", "S"], ["b"]]
                          })
        grammar.eliminate_start_symbol()
        print(grammar)
        self.assertIn(grammar.start_symbol, grammar.productions)
        self.assertEqual(grammar.productions[grammar.start_symbol], [["S"]])
        self.assertNotEqual(grammar.start_symbol, "S")

    def test2(self):
        grammar = Grammar("S",
                          {
                              "S": [["S"], ["b"]],
                              "A": [["S"]]
                           })
        grammar.eliminate_start_symbol()
        print(grammar)
        for lhs in grammar.productions.keys():
            self.assertTrue(grammar.start_symbol not in grammar.productions[lhs])


class TestTERM(unittest.TestCase):
    def test_term_single_occurrence(self):
        grammar = Grammar("S",
                          {
                              "S": [["a", "S", "b"], ["b"]]
                          })
        print(f"before: \n{grammar}")

        grammar.eliminate_nonsolitary_terminals()
        print(f"\n\n\nafter: \n{grammar}")

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
        print(f"before: \n{grammar}")

        grammar.eliminate_nonsolitary_terminals()
        print(f"\n\n\nafter: \n{grammar}")

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
        grammar.eliminate_nonsolitary_terminals()
        self.assertNotIn("N_b", grammar.productions)
        self.assertEqual(grammar.productions["S"], [["N_a"], ["b"]])

    def test_term_empty_productions(self):
        grammar = Grammar("S", {})
        grammar.eliminate_nonsolitary_terminals()
        self.assertEqual(grammar.productions, {})


class TestBIN(unittest.TestCase):
    def test_bin_basic_split(self):
        grammar = Grammar("S",
                          {
                              "S": [["A", "B", "C", "D"]]
                          })
        print(f"before: \n{grammar}")
        grammar.eliminate_rhs_with_more_than_two_nonterminals()
        print(f"\n\n\nafter: \n{grammar}")

        # We expect S -> A A1, A1 -> B A2, A2 -> C D
        self.assertEqual(len(grammar.productions["S"]), 1)
        self.assertTrue(len(grammar.productions["S"][0]) == 2)
        self.assertTrue(all(len(rhs) == 2 for rhs_list in grammar.productions.values() for rhs in rhs_list))

    def test_bin_no_split_needed(self):
        grammar = Grammar("S",
                          {
                              "S": [["A", "B"], ["C"]]
                          })
        print(f"before: \n{grammar}")
        grammar.eliminate_rhs_with_more_than_two_nonterminals()
        print(f"\n\n\nafter: \n{grammar}")
        self.assertEqual(grammar.productions["S"], [["A", "B"], ["C"]])

    def test_bin_complex_case(self):
        grammar = Grammar("S",
                          {
                              "S": [["A", "B", "C", "D", "E", "F"]]
                          })
        print(f"before: \n{grammar}")
        grammar.eliminate_rhs_with_more_than_two_nonterminals()
        print(f"\n\n\nafter: \n{grammar}")        # Expecting a chain like S -> A A1, A1 -> B A2, ..., An-2 -> E F
        self.assertEqual(len(grammar.productions["S"]), 1)
        self.assertTrue(len(grammar.productions["S"][0]) == 2)
        non_terminals = [prod for nt, prods in grammar.productions.items() for prod in prods if nt != "S"]
        self.assertTrue(all(len(prod) == 2 for prod in non_terminals))

    def test_bin_length_check(self):
        grammar = Grammar("S",
                          {
                              "S": [["A", "B", "C", "D", "E"]]
                          })
        print(f"before: \n{grammar}")
        grammar.eliminate_rhs_with_more_than_two_nonterminals()
        print(f"\n\n\nafter: \n{grammar}")
        # We expect transformations but focus on verifying the rule lengths.
        for production_list in grammar.productions.values():
            for production in production_list:
                self.assertTrue(len(production) <= 2)


if __name__ == "__main__":
    unittest.main()
