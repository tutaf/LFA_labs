# Laboratory Work 3: Lexer & Scanner

### Course: Formal Languages & Finite Automata
### Author: Cernisov Andrei

----

## Theory
A lexer (short for **lex**ical analyz**er**) is a program that takes input text (such as source code / markup) and breaks it down into a sequence of tokens. Tokens represent the basic building blocks of the language, like keywords, identifiers, operators, punctuation marks, etc. The lexer identifies and classifies these tokens based on the language's rules and patterns, essentially converting the raw input text into a structured stream of tokens that can be further processed and analyzed by other components, like the parser. Unlike a parser, lexer does not understand the meaning or structure of these tokens; it simply identifies and classifies them.



## Objectives:

* Understand what lexical analysis is
* Get familiar with the inner workings of a lexer/scanner/tokenizer
* Implement a sample lexer and show how it works


## Implementation description

I decided to implement a lexer for simplified version of Markdown language. Here are some from Markdown that are supported by this lexer:

- `TEXT` - Regular text content
- `HASH` - Heading marker (`#`)
- `UNDERSCORE` - Underscore (`_`) for italics
- `STAR` - Asterisk (`*`) for bold or italics
- `NEWLINE` - Line break (`\n`)
- `DASH` - Hyphen (`-`) for unordered lists
- `STRAIGHTBRACEOPEN` - Opening square bracket (`[`) for links and images
- `STRAIGHTBRACECLOSE` - Closing square bracket (`]`) for links and images
- `PARENOPEN` - Opening parenthesis (`(`) for links and images
- `PARENCLOSE` - Closing parenthesis (`)`) for links and images
- `GREATERTHAN` - Greater than symbol (`>`) for quotes
- `BANG` - Exclamation mark (`!`) for images

All these types of tokens are defined in the `TokenKind` class/enum, alognside the `Token` class itself:

```python
class TokenKind:
    TEXT = 1
    HASH = 2
    # other kinds of tokens...
    
class Token:
    def __init__(self, kind, value, pos, line):
        self.kind = kind
        self.value = value
        self.pos = pos
        self.line = line
```

Next, the `Lexer` class is defined. During initialization, the input string is preprocessed by splitting it into lines and removing leading/trailing whitespaces, line breaks, and empty lines. Markdown ignores all of these outside code blocks (which are not part of this simplified Markdown version), so there's no point in keeping them.
```python
class Lexer:
    def __init__(self, input_string):
        # ...
        raw_input_lines = input_string.split('\n')
        for line in raw_input_lines: 
            line = line.strip()  # remove unnecessary spaces, tabs and line breaks
            if line:  # ignore empty lines
                line += "\n"
                self.input_lines.append(line)
```

The `advance` method is used to move the character position to the next character in the current line. It updates `current_char` with the new character and increments the `char_pos` counter.

The `advance_line` method moves the lexer to the next line of input. It first checks if there are more lines left in `input_lines`. If so, it updates `current_line` with the next line, increments `line_number`, resets `char_pos` to 0 (start of line), and calls `advance` to set `current_char` to the first character of the new line. If there are no more lines, it sets `current_char` to `None` to indicate the end of input.

```python
class Lexer:
    # ...

    def advance(self):
        if self.char_pos < len(self.current_line):
            self.current_char = self.current_line[self.char_pos]
            self.char_pos += 1

    def advance_line(self):
        if self.line_number < len(self.input_lines):
            self.current_line = self.input_lines[self.line_number]
            self.line_number += 1
            self.char_pos = 0
            self.advance()
        else:
            self.current_char = None  # the end
```

The `lex` method is the core of the lexer. It iterates through the input string character by character, recognizing special characters and creating tokens for them. For regular text, it collects characters until a special character is encountered and creates a `TEXT` token.
```python
class Lexer:
    # ...
    
    def lex(self):
        while self.current_char is not None:
            # ... check for special characters and create tokens ...
            
            else:
                value += self.current_char
                self.advance()
                while (self.current_char is not None) and (self.current_char not in ' \n\t#_*-[]()>!`'):
                    value += self.current_char
                    self.advance()
                self.add_token(TokenKind.TEXT, value)
            # ...
    
    def add_token(self, kind, value=""):
        # ... create Token instance and append to processed tokens list ...
```

Additionally, this implementation of lexer treats each word as a separate `TEXT` token. This was done because Markdown ignores duplicate spaces/tabs in text.
```python
class Lexer:
    # ...
    
    def lex(self):
        while self.current_char is not None:
            if self.current_char in ' \t':  # skip duplicate whitespaces/tabs
                self.advance()
                continue
```


## Input / Output Example
Input:
```
## Heading 2
```
Output:
```
HASH                  pos=0 	 line=1 	 value=''
HASH                  pos=1 	 line=1 	 value=''
TEXT                  pos=3 	 line=1 	 value='Heading'
TEXT                  pos=11 	 line=1 	 value='2'
NEWLINE               pos=12 	 line=1 	 value=''
```


## References
* [Lexical analysis of Markdown in Go](https://xnacly.me/posts/2023/lexer-markdown/)
* [What is a Lexer](https://www.youtube.com/watch?v=BI3K-ME3L74)