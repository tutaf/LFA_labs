import re


class TokenKind:
    TEXT = 'TEXT'
    HASH = 'HASH'
    UNDERSCORE = 'UNDERSCORE'
    STAR = 'STAR'
    NEWLINE = 'NEWLINE'
    DASH = 'DASH'
    BRACKET_OPEN = 'BRACKET_OPEN'
    BRACKET_CLOSE = 'BRACKET_CLOSE'
    PAREN_OPEN = 'PAREN_OPEN'
    PAREN_CLOSE = 'PAREN_CLOSE'
    LINK = 'LINK'
    IMAGE = 'IMAGE'
    WHITESPACE = 'WHITESPACE'
    OTHER = 'OTHER'


TOKEN_PATTERNS = [
    (TokenKind.LINK, re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')),    # since we're going through patterns sequentially,
    (TokenKind.IMAGE, re.compile(r'!\[([^\]]+)\]\(([^\)]+)\)')),  # it's important to put LINK and IMAGE before [ and ]
    (TokenKind.HASH, re.compile(r'^#+')),
    (TokenKind.UNDERSCORE, re.compile(r'^_+')),
    (TokenKind.STAR, re.compile(r'^\*+')),
    (TokenKind.NEWLINE, re.compile(r'^\n')),
    (TokenKind.DASH, re.compile(r'^-+')),
    (TokenKind.BRACKET_OPEN, re.compile(r'^\[+')),
    (TokenKind.BRACKET_CLOSE, re.compile(r'^\]+')),
    (TokenKind.PAREN_OPEN, re.compile(r'^\(+')),
    (TokenKind.PAREN_CLOSE, re.compile(r'^\)+')),
    (TokenKind.WHITESPACE, re.compile(r'^\s+')),
    (TokenKind.TEXT, re.compile(r'^[^\s\[\]#!\*_\(\)-]+')),
]

class Token:
    def __init__(self, kind, value, position):
        self.kind = kind
        self.value = value
        self.position = position

    def __str__(self):
        return f"{self.kind} {self.value if len(self.value) > 1 else str()}"


def lexer(input_text):
    tokens = []
    position = 0
    skip_types = {TokenKind.WHITESPACE}  # we'll ignore whitespaces because they don't matter in markdown
    while position < len(input_text):
        match = None
        for kind, pattern in TOKEN_PATTERNS:
            match = pattern.match(input_text[position:])
            if match:
                value = match.group(0)
                if kind in [TokenKind.LINK, TokenKind.IMAGE]:
                    value = match.groups()
                if kind not in skip_types:
                    if tokens and tokens[-1].kind == TokenKind.TEXT and kind == TokenKind.TEXT:
                        tokens[-1].value += ' ' + value  # merge consecutive text tokens
                    else:
                        tokens.append(Token(kind, value, position))
                position += len(match.group(0))
                break
        if not match:
            tokens.append(Token(TokenKind.OTHER, input_text[position], position))
            print("Can't match token to any pattern")
            position += 1
    return tokens

markdown_text = """
# Heading
[Link](http://example.com)
![Image](http://example.com/img.png)
Text   here
*italic* **bold** ***bold AND italic***
"""

tokens = lexer(markdown_text)
for token in tokens:
    print(token)
