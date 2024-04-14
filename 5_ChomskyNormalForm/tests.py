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


if __name__ == "__main__":
    unittest.main()
