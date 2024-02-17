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


def print_strings(number_of_strings, showProgress):
    grammar = Grammar()

    for i in range(number_of_strings):
        tmp = "S"
        start = grammar.VN[0]
        while start[-1] not in grammar.VT:
            t = start[-1]
            start = start[:-1] + random.choice(grammar.P[t])
            tmp += f" -> {start}"
        print(start)
        if (showProgress): print(tmp + "\n")



print_strings(5, True)
