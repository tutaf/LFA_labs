import re, random
import string

REPETITION_LIMIT = 5


class Step:
    def __init__(self):
        self.symbols = []  # '.' - any symbol
        self.repetitions = 0  # '*' - zero or more; '+' - once or more; '?' - optional (0 or 1)

    def get_matching_string_and_description(self):
        result = ""
        progress = []
        description = ""
        exact_repetitions = 0
        if self.repetitions == '*':
            description = "zero or more times"
            exact_repetitions = random.randint(0, REPETITION_LIMIT)
        elif self.repetitions == '+':
            description = "one or more times"
            exact_repetitions = random.randint(1, REPETITION_LIMIT)
        elif self.repetitions == '?':
            description = "is optional (0 or 1 repetitions)"
            exact_repetitions = random.randint(0, 1)
        else:
            description = f"exactly {self.repetitions} times"
            exact_repetitions = self.repetitions

        description = (f"Repeating '{self.symbols[0]}' " if len(self.symbols) == 1 else
                       f"Picking random element from {self.symbols} ") + description

        for i in range(exact_repetitions):
            choice = random.choice(self.symbols)
            if choice == '.':
                choice = random.choice(string.ascii_lowercase)
            result += choice
            progress.append(result)

        progress_string = " -> ".join(progress)

        return result, description, progress_string


def generate_steps(regex):
    for symbols, repetitions in regex:
        step = Step()
        step.symbols = symbols
        step.repetitions = repetitions
        yield step


regex_patterns = [
    'O(P|Q|R)+2(3|4)',
    'A*B(C|D|E)F(G|H|i){2}',
    'J+K(L|M|N)*O?(P|Q){3}'
]

regex_steps = [
    [
        (['O'], 1),
        (['P', 'Q', 'R'], '+'),
        (['2'], 1),
        (['3', '4'], 1)
    ],
    [
        (['A'], '*'),
        (['B'], 1),
        (['C', 'D', 'E'], 1),
        (['F'], 1),
        (['G', 'H', 'i'], 2)
    ],
    [
        (['J'], '+'),
        (['K'], 1),
        (['L', 'M', 'N'], '*'),
        (['O'], '?'),
        (['P', 'Q'], 3)
    ]
]

regex_number = int(input("Enter the number of regular expression: ")) - 1
print(f"Expression {regex_number}: {regex_patterns[regex_number]}\n")

steps_generator = generate_steps(regex_steps[regex_number])
steps = list(steps_generator)

regex_result = ""
for i in range(len(steps)):
    step = steps[i]
    result, description, progress_string = step.get_matching_string_and_description()
    print(f"Step {i+1}: {description}")
    print(f"{progress_string}")
    regex_result += result

print(f"\nResult: {regex_result}")
print(f"Is a valid string: {re.fullmatch(regex_patterns[regex_number], regex_result) is not None}")


