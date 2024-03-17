class TokenKind:
    TEXT = 1
    HASH = 2
    UNDERSCORE = 3
    STAR = 4
    NEWLINE = 5
    DASH = 6
    STRAIGHTBRACEOPEN = 7
    STRAIGHTBRACECLOSE = 8
    PARENOPEN = 9
    PARENCLOSE = 10
    GREATERTHAN = 11
    BANG = 12


class Token:
    def __init__(self, kind, value, pos, line):
        self.kind = kind
        self.value = value
        self.pos = pos
        self.line = line

    def get_string(self):
        token_kind_name = [k for k, v in TokenKind.__dict__.items() if v == self.kind][0]
        return f"{token_kind_name} {' '*(19-len(token_kind_name))}  pos={self.pos} \t line={self.line} \t value='{self.value}'"


class Lexer:
    def __init__(self, input_string):
        self.input_lines = []
        self.line_number = 0
        self.char_pos = 0
        self.current_line = ''
        self.current_char = ''
        self.tokens = []

        raw_input_lines = input_string.split('\n')
        for line in raw_input_lines:  # markdown ignores empty lines
            line = line.strip()
            if line:
                line += "\n"
                self.input_lines.append(line)

        self.advance_line()  # init first line

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

    def add_token(self, kind, value=""):
        if self.current_char == '\n' and kind == TokenKind.NEWLINE:  # adjust position for \n
            adjusted_pos = len(self.current_line)-1
        else:
            adjusted_pos = self.char_pos - len(value)-1 if value else self.char_pos-1
        self.tokens.append(Token(kind, value, adjusted_pos, self.line_number))

    def lex(self):
        while self.current_char is not None:
            if self.current_char in ' \t':  # markdown ignores whitespaces and tabs
                self.advance()
                continue

            token_kind = None
            value = ""

            if self.current_char == '#':
                token_kind = TokenKind.HASH
            elif self.current_char == '_':
                token_kind = TokenKind.UNDERSCORE
            elif self.current_char == '*':
                token_kind = TokenKind.STAR
            elif self.current_char == '\n':
                token_kind = TokenKind.NEWLINE
            elif self.current_char == '-':
                token_kind = TokenKind.DASH
            elif self.current_char == '[':
                token_kind = TokenKind.STRAIGHTBRACEOPEN
            elif self.current_char == ']':
                token_kind = TokenKind.STRAIGHTBRACECLOSE
            elif self.current_char == '(':
                token_kind = TokenKind.PARENOPEN
            elif self.current_char == ')':
                token_kind = TokenKind.PARENCLOSE
            elif self.current_char == '>':
                token_kind = TokenKind.GREATERTHAN
            elif self.current_char == '!':
                token_kind = TokenKind.BANG
            else:
                value += self.current_char
                self.advance()
                while (self.current_char is not None) and (self.current_char not in ' \n\t#_*-[]()>!`'):
                    value += self.current_char
                    self.advance()
                self.add_token(TokenKind.TEXT, value)
                continue

            if token_kind:
                self.add_token(token_kind, value)

            if token_kind == TokenKind.NEWLINE:
                self.advance_line()
                continue

            self.advance()

    def print_tokens(self):
        for token in self.tokens:
            print(token.get_string())


markdown_input = """
# Heading 1
## Heading 2
- [ ] Todo item
- [x] Done item
_italic_

[Link](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
![Image](https://example.com/image.jpg)
justtext
> Quote"""


lexer = Lexer(markdown_input)
lexer.lex()
lexer.print_tokens()
