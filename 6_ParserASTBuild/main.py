import re
from typing import List


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


class NodeType:
    ROOT = 'ROOT'
    PARAGRAPH = 'PARAGRAPH'
    BOLD = 'BOLD'
    ITALIC = 'ITALIC'
    IMAGE = 'IMAGE'
    LINK = 'LINK'
    TEXT = 'TEXT'


class Node:
    def __init__(self, node_type, node_value, input_tokens: List[Token]):
        self.node_type = node_type
        self.node_value = node_value
        self.children = []
        self.tokens = input_tokens

        if node_type == NodeType.ROOT:
            self.__process_paragraphs__()

    def __process_paragraphs__(self):
        paragraph_contents = []
        for token in self.tokens:
            if token.kind == TokenKind.NEWLINE and len(paragraph_contents) > 0:
                self.children.append(Node(NodeType.PARAGRAPH, None, paragraph_contents))
                paragraph_contents = []

            if token.kind != TokenKind.NEWLINE:
                paragraph_contents.append(token)


    # def __parse_paragraph_contents__(self):


    # def __str__(self):
    #
    #     return f"{self.node_type}: {self.node_value}, {self.children} ||| {self.tokens}"



markdown_text = """
[Link](http://example.com)
![Image](http://example.com/img.png)
Text   here
*italic* **bold** ***bold AND italic***
*italic text* **[some link](http://example.com) some other text** ***bold AND italic***
"""


example_tokens = lexer(markdown_text)
for example_token in example_tokens:
    print(example_token)


print("\n===========================\n")
node = Node(NodeType.ROOT, None, example_tokens)
print(node)

