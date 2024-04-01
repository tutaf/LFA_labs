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


def parse_regex_to_steps(regex):
    steps = []
    i = 0
    while i < len(regex):
        symbols = []
        repetitions = 1

        # handle character or group
        if regex[i] == '(':
            # group start, find closing parenthesis
            group_end = regex.find(')', i)
            symbols = regex[i + 1:group_end].split('|')
            i = group_end
        elif regex[i] == '[':
            # bracket start, find closing bracket
            bracket_end = regex.find(']', i)
            symbols = list(regex[i + 1:bracket_end])  # consider each symbol within brackets individually
            i = bracket_end
        else:
            # handle single characters
            symbols = [regex[i]]

        # look ahead for repetition symbols
        if i + 1 < len(regex):
            if regex[i + 1] in '*+?':
                repetitions = regex[i + 1]
                i += 1  # skip the repetition symbol
            elif regex[i + 1] == '{':
                # find closing brace and extract repetition number
                brace_end = regex.find('}', i)
                repetitions = int(regex[i + 2:brace_end])
                i = brace_end

        steps.append((symbols, repetitions))

        # move to the next symbol
        i += 1

    return steps

# Test patterns:
# O(P|Q|R)+2(3|4)
# A*B(C|D|E)F(G|H|i){2}
# J+K(L|M|N)*O?(P|Q){3}


input_ = input("Enter the number of regular expression: ")
print()

steps_parsed = parse_regex_to_steps(input_)

steps_generator = generate_steps(steps_parsed)
steps = list(steps_generator)

regex_result = ""
for i in range(len(steps)):
    step = steps[i]
    result, description, progress_string = step.get_matching_string_and_description()
    print(f"Step {i+1}: {description}")
    print(f"{progress_string}")
    regex_result += result

print(f"\nResult: {regex_result}")
print(f"Is a valid string: {re.fullmatch(input_, regex_result) is not None}")


