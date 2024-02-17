import random


class Grammar:
    def __init__(self):
        self.VN = ['S', 'D', 'R']
        self.VT = ['a', 'b', 'c', 'd', 'f']
        self.P = {
            'S': ['aS', 'bD', 'fR'],
            'D': ['cD', 'dR', 'd'],
            'R': ['bR', 'f']
        }


def print_strings(number_of_strings):
    grammar = Grammar()
    for i in range(number_of_strings):
        start = grammar.VN[0]
        while start[-1] not in grammar.VT:
            t = start[-1]
            start = start[:-1] + random.choice(grammar.P[t])
        print(start)



print_strings(5)
