import re, random

regex1 = 'O(P|Q|R)+2(3|4)'


def generate_example(pattern: str):
    attempt = 0
    non_regex_symbols = pattern
    regex_symbols = ['[', ']', '(', ')', '{', '}', '*', '+', '.', '^', '$', '\\', '|', '?']
    for symbol in regex_symbols:
        non_regex_symbols = non_regex_symbols.replace(symbol, '')
    non_regex_symbols = list(set(list(non_regex_symbols)))
    # print(non_regex_symbols)

    while True:
        result = ""
        for i in range(random.randint(2, 10)):
            result += random.choice(non_regex_symbols)
        result_string = "".join(result)
        if re.fullmatch(pattern, result_string):
            return result_string
        else:
            attempt += 1


r = generate_example(regex1)
print(r)
