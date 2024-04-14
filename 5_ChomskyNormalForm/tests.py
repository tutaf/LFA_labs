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


if __name__ == "__main__":
    unittest.main()
