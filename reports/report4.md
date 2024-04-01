# Regular Expressions

### Course: Formal languages & Finite Automata
### Author: Andrei Cernisov
#### Variant 3

----

## Theory

Regular expressions, often abbreviated as regex, are sequences of characters that define a search pattern. They are primarily used for string pattern matching and manipulation operations, such as finding, replacing, or validating text based on specific rules. Regular expressions provide a concise and flexible way to describe complex patterns using a formal syntax.

Regular expressions are based on the theory of finite automata and formal languages. They are designed to match strings that belong to a specific regular language, which is a set of strings that can be recognized by a finite automaton. Regular languages are described by regular expressions, which are constructed using a set of operators and symbols.

The basic building blocks of regular expressions are:

1. **Literal characters**: These are the characters that represent themselves in the pattern, such as letters, digits, or punctuation marks.
2. **Special characters**: These characters have a specific meaning in regular expressions, such as `.` (dot) which matches any character except a newline, `\d` which matches any digit, and `\s` which matches any whitespace character.
3. **Character classes**: These are used to match a set of characters, such as `[abc]` which matches any of the characters 'a', 'b', or 'c', or `[^abc]` which matches any character except 'a', 'b', or 'c'.
4. **Quantifiers**: These operators specify how many times a particular pattern should be matched. Some common quantifiers are `*` (zero or more times), `+` (one or more times), `?` (zero or one time), and `{n}` (exactly n times).
5. **Anchors**: These are used to specify the position of the pattern within the string, such as `^` which matches the start of the string, and `$` which matches the end of the string.
6. **Alternation**: The `|` (pipe) symbol is used to specify alternatives, such as `cat|dog` which matches either the string 'cat' or the string 'dog'.
7. **Grouping**: Parentheses `()` are used to group patterns together and apply quantifiers or alternations to the entire group.

Regular expressions are widely used in various applications, including text processing, data validation, information extraction, and programming. They are supported by many programming languages and tools, making them a powerful and widely used tool for working with text data.

## Objectives:

* Understand the concept of regular expressions and their applications.
* Implement a program that generates valid combinations of symbols according to user-provided regular expressions.
* Demonstrate the step-by-step processing of regular expressions.

## Implementation description

The implementation consists of three main components: a `Step` class, a `generate_steps` function, and a `parse_regex_to_steps` function.

### Step Class

The `Step` class remains the same as in the previous implementation. It represents a single step in the process of generating a valid string for a given regular expression.

```python
class Step:
    def __init__(self):
        self.symbols = []  # '.' - any symbol
        self.repetitions = 0  # '*' - zero or more; '+' - once or more; '?' - optional (0 or 1)

    def get_matching_string_and_description(self):
        # ... (same implementation as before)
```

The `get_matching_string_and_description` method is responsible for generating a valid string based on the `symbols` and `repetitions` attributes, and also returns a description of the step and a progress string showing the intermediate steps.

### generate_steps Function

The `generate_steps` function remains unchanged from the previous implementation. It takes a list of tuples containing `symbols` and `repetitions` for each step, and yields `Step` objects representing those steps.

```python
def generate_steps(regex):
    for symbols, repetitions in regex:
        step = Step()
        step.symbols = symbols
        step.repetitions = repetitions
        yield step
```

### parse_regex_to_steps Function

```python
def parse_regex_to_steps(regex):
    steps = []
    i = 0
    while i < len(regex):
        symbols = []
        repetitions = 1
```

This part initializes an empty list `steps` to store the steps and sets the initial values for `symbols` (an empty list) and `repetitions` (1, which represents a single occurrence).

```python
        if regex[i] == '(':
            # group start, find closing parenthesis
            group_end = regex.find(')', i)
            symbols = regex[i + 1:group_end].split('|')
            i = group_end
```

This block of code handles character groups enclosed within parentheses, such as `(P|Q|R)`. It finds the closing parenthesis using the `find` method and then splits the characters between the parentheses using the `|` (pipe) symbol as the separator. The resulting list of symbols is assigned to the `symbols` variable, and the index `i` is updated to the position after the closing parenthesis.

```python
        elif regex[i] == '[':
            # bracket start, find closing bracket
            bracket_end = regex.find(']', i)
            symbols = list(regex[i + 1:bracket_end])  # consider each symbol within brackets individually
            i = bracket_end
```

This block of code handles character classes enclosed within square brackets, such as `[abc]`. It finds the closing bracket using the `find` method and then converts the characters between the brackets into a list, where each character is treated as an individual symbol. The resulting list of symbols is assigned to the `symbols` variable, and the index `i` is updated to the position after the closing bracket.

```python
        else:
            # handle single characters
            symbols = [regex[i]]
```

If the current character is neither an opening parenthesis nor an opening bracket, it is treated as a single literal character. The character is added to the `symbols` list.

```python
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
```

This part of the code looks ahead to handle repetition symbols such as `*`, `+`, `?`, and `{n}`. If the next character is `*`, `+`, or `?`, the corresponding repetition symbol is assigned to the `repetitions` variable, and the index `i` is incremented to skip over the repetition symbol. If the next character is `{`, the function finds the closing brace and extracts the repetition number, which is then assigned to the `repetitions` variable as an integer. The index `i` is updated to the position after the closing brace.

```python
        steps.append((symbols, repetitions))

        # move to the next symbol
        i += 1

    return steps
```

After processing the current symbol(s) and repetition, the `symbols` and `repetitions` are appended as a tuple to the `steps` list. The index `i` is then incremented to move to the next symbol in the regular expression. Finally, the `steps` list containing all the steps is returned.

This implementation allows the `parse_regex_to_steps` function to handle various elements of regular expressions, including character groups, character classes, literal characters, and different repetition patterns. The resulting list of tuples can be used by the `generate_steps` function to generate valid strings based on the provided regular expression.
### Main Program

The main program prompts the user to input a regular expression and then processes it using the `parse_regex_to_steps` function.

```python
input_ = input("Enter the number of regular expression: ")

steps_parsed = parse_regex_to_steps(input_)

steps_generator = generate_steps(steps_parsed)
steps = list(steps_generator)
```

The rest of the main program iterates over the `steps` list, generating the valid string, and displaying the step-by-step process and the final result.

```python
regex_result = ""
for i in range(len(steps)):
    step = steps[i]
    result, description, progress_string = step.get_matching_string_and_description()
    print(f"Step {i+1}: {description}")
    print(f"{progress_string}")
    regex_result += result

print(f"\nResult: {regex_result}")
print(f"Is a valid string: {re.fullmatch(input_, regex_result) is not None}")
```

## Results

The program accepts user-inputted regular expressions and generates valid strings accordingly. It also displays the step-by-step process of generating the string and checks if the final string matches the provided regular expression.

Here's an example of input/output:

```
Enter the number of regular expression: J+K(L|M|N)*O?(P|Q){3}

Step 1: Repeating 'J' one or more times
J -> JJ -> JJJ
Step 2: Repeating 'K' exactly 1 times
K
Step 3: Picking random element from ['L', 'M', 'N'] zero or more times
N -> NL -> NLM -> NLMM
Step 4: Repeating 'O' is optional (0 or 1 repetitions)
O 
Step 5: Picking random element from ['P', 'Q'] exactly 3 times
P -> PQ -> PQP

Result: JJJKNLMMOPQP
Is a valid string: True
```

The program accurately generates a valid string "JJJKNLMMOPQP" for the user-inputted regular expression `J+K(L|M|N)*O?(P|Q){3}` and confirms its validity using the `re.fullmatch`.

## Conclusion
In conclusion, this project demonstrates a program that generates valid strings based on user-provided regular expressions. The `parse_regex_to_steps` function enables handling arbitrary regular expressions. The program displays both the final result and the intermediate steps. Overall, the project achieves its objectives by generating strings that match a regular expressions.