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
* Implement a program that generates valid combinations of symbols according to provided regular expressions.
* Demonstrate the step-by-step processing of regular expressions.

## Implementation description

The implementation consists of two main components: a `Step` class and a `generate_steps` function.

### Step Class

The `Step` class represents a single step in the process of generating a valid string for a given regular expression. It has two attributes:

- `symbols`: A list of characters or the special symbol '.' representing any character.
- `repetitions`: A character representing the repetition pattern ('*', '+', '?', or a specific number).

The `__init__` method initializes the `symbols` list and `repetitions` attribute:

```python
def __init__(self):
    self.symbols = []  # '.' - any symbol
    self.repetitions = 0  # '*' - zero or more; '+' - once or more; '?' - optional (0 or 1)
```

The `get_matching_string_and_description` method is the core of the `Step` class. It generates a valid string based on the `symbols` and `repetitions` attributes, and also returns a description of the step and a progress string showing the intermediate steps. Here's a breakdown of the `get_matching_string_and_description` method:

```python
def get_matching_string_and_description(self):
    result = ""
    progress = []
    description = ""
    exact_repetitions = 0
```

This part of code initializes three varialbes: `result` to store the generated string, `progress` to keep track of the intermediate steps, and `description` to hold the description of the step.

```python
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
```

This block of code determines the exact number of repetitions based on the `repetitions` attribute. If the repetition is '*', the number of repetitions is randomly chosen between 0 and the `REPETITION_LIMIT` constant. If the repetition is '+', the number of repetitions is randomly chosen between 1 and the `REPETITION_LIMIT`. If the repetition is '?', the number of repetitions is randomly chosen between 0 and 1. Otherwise, the exact number of repetitions is taken from the `repetitions` attribute.

```python
description = (f"Repeating '{self.symbols[0]}' " if len(self.symbols) == 1 else
               f"Picking random element from {self.symbols} ") + description
```

This line constructs the description string based on whether the `symbols` list contains a single element or multiple elements.

```python
for i in range(exact_repetitions):
    choice = random.choice(self.symbols)
    if choice == '.':
        choice = random.choice(string.ascii_lowercase)
    result += choice
    progress.append(result)
```

This loop iterates `exact_repetitions` times. In each iteration, it randomly selects a symbol from the `symbols` list. If the selected symbol is '.', it is replaced with a randomly chosen lowercase letter. The selected symbol is then appended to the `result` string, and the current `result` is added to the `progress` list.

```python
progress_string = " -> ".join(progress)

return result, description, progress_string
```

Finally, the `progress` list is joined into a single string with the arrows (`->`) separating the intermediate steps, and the `result`, `description`, and `progress_string` are returned.

### generate_steps Function

The `generate_steps` function takes a regular expression as input and yields a sequence of `Step` objects representing each step in the regular expression.

```python
def generate_steps(regex):
    for symbols, repetitions in regex:
        step = Step()
        step.symbols = symbols
        step.repetitions = repetitions
        yield step
```

This function iterates over the provided `regex` list, which consits of tuples containing the `symbols` and `repetitions` for each step. For each tuple, a new `Step` object is created, and its `symbols` and `repetitions` attributes are set accordingly. The `Step` object is then yielded to the caller.

### Main Program

The main program consists of three parts:

1. Defining the regular expression patterns and their corresponding steps.
2. Taking user input to select the regular expression to be processed.
3. Generating valid strings and displaying the step-by-step process.

```python
regex_patterns = [
    'O(P|Q|R)+2(3|4)',
    # ... other patterns ...
]

regex_steps = [
    [
        (['O'], 1),
        (['P', 'Q', 'R'], '+'),
        (['2'], 1),
        (['3', '4'], 1)
    ],
    # ... steps for other expressions ...
]
```
This is the definition of regular expressions for which the program will generate valid strings.

```
regex_number = int(input("Enter the number of regular expression: ")) - 1
print(f"Expression {regex_number+1}: {regex_patterns[regex_number]}\n")
```
This code snippet prompts the user to enter the number of the regular expression to be processed.

```
steps_generator = generate_steps(regex_steps[regex_number])
steps = list(steps_generator)
```
Next, the `generate_steps` function is called with the selected regular expression steps, and its output is converted to a list using `list(steps_generator)`.


```
regex_result = ""
for i in range(len(steps)):
    step = steps[i]
    result, description, progress_string = step.get_matching_string_and_description()
    print(f"Step {i+1}: {description}")
    print(f"{progress_string}")
    regex_result += result

print(f"\nResult: {regex_result}")
```
The program then iterates over the `steps` list. For each step, it calls the `get_matching_string_and_description` method to obtain the generated string, description, and progress string. It prints the step number, description, and progress string, and appends the generated string to the `regex_result` variable.


```
print(f"Is a valid string: {re.fullmatch(regex_patterns[regex_number], regex_result) is not None}")
```

Finally, the program prints the final `regex_result` string and checks if it matches the selected regular expression pattern using the `re.fullmatch` function.

## Results

The program successfully generates valid strings based on the provided regular expressions. It also displays the step-by-step process of generating the string, making it easier to understand the logic behind regular expression processing.

Here's an example of input/output:

```
Enter the number of regular expression: 2
Expression 2: A*B(C|D|E)F(G|H|i){2}

Step 1: Picking random element from ['A'] zero or more times
-> AA -> AAA -> AAAA
Step 2: Repeating 'B' exactly 1 times
B
Step 3: Picking random element from ['C', 'D', 'E'] exactly 1 times
D
Step 4: Repeating 'F' exactly 1 times
F
Step 5: Picking random element from ['G', 'H', 'i'] exactly 2 times
H -> HH

Result: AAAABDFHH
Is a valid string: True
```

The program accurately generates a valid string "AAAABDFHH" for the regular expression "A*B(C|D|E)F(G|H|i){2}" and confirms its validity using the `re.fullmatch` function from the Python `re` module.

## Conclusion
In conclusion, this project successfully demonstrates the implementation of a program that generates valid strings based on regular expressions. The step-by-step approach, which breaks down the regular expression into individual steps, provides a clear understanding of the process and facilitates the generation of valid combinations. The program's output not only displays the final result, but also the intermediate steps. Overall, the project fulfills its objectives by generating strings that match specific regular expressions.
