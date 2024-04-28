import re
from typing import List
from graphviz import Digraph


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
    HEADING = 'HEADING'
    BOLD = 'BOLD'
    ITALIC = 'ITALIC'
    IMAGE = 'IMAGE'
    LINK = 'LINK'
    TEXT = 'TEXT'


class Node:
    def __init__(self, node_type, node_value, input_tokens: List[Token], children=None):
        if children is None:
            children = []
        self.node_type = node_type
        self.node_value = node_value
        self.children = children
        self.tokens = input_tokens

        if node_type == NodeType.ROOT:
            self.__process_paragraphs__()
        else:
            self.__process_paragraph_contents__()

    def __process_paragraphs__(self):
        paragraph_contents = []
        for token in self.tokens:
            if token.kind == TokenKind.NEWLINE and len(paragraph_contents) > 0:
                if paragraph_contents[0].kind == TokenKind.HASH:
                    node_value = len(paragraph_contents[0].value)
                    paragraph_contents.pop(0)
                    self.children.append(Node(NodeType.HEADING, node_value, paragraph_contents))
                else:
                    self.children.append(Node(NodeType.PARAGRAPH, None, paragraph_contents))
                paragraph_contents = []

            if token.kind != TokenKind.NEWLINE:
                paragraph_contents.append(token)

    def __process_paragraph_contents__(self):
        emphasized_contents = []
        star_number = 0  # 0 - not currently parsing any emphasized contents
        for token in self.tokens:
            if token.kind == TokenKind.STAR and star_number == 0:
                star_number = len(token.value)
                continue

            if star_number != 0 and not (token.kind == TokenKind.STAR and len(token.value) == star_number):
                emphasized_contents.append(token)

            if star_number == 0:  # we're not inside an emphasized block
                if token.kind == TokenKind.TEXT:
                    self.children.append(Node(NodeType.TEXT, token.value, []))
                elif token.kind == TokenKind.LINK:
                    link_content_tokens = lexer(token.value[0])
                    self.children.append(Node(NodeType.LINK, token.value[1], link_content_tokens))
                elif token.kind == TokenKind.IMAGE:
                    alttext_content_tokens = lexer(token.value[0])
                    self.children.append(Node(NodeType.IMAGE, token.value[1], alttext_content_tokens))

            if token.kind == TokenKind.STAR and len(token.value) == star_number:  # if it's a closing star
                if star_number == 1:
                    self.children.append(Node(NodeType.ITALIC, None, emphasized_contents))
                elif star_number == 2:
                    self.children.append(Node(NodeType.BOLD, None, emphasized_contents))
                elif star_number == 3:
                    new_node = Node(NodeType.ITALIC, None, emphasized_contents)
                    self.children.append(Node(NodeType.BOLD, None, [], children=[new_node]))
                else:
                    raise SyntaxError("Incorrect number of stars")
                emphasized_contents = []
                star_number = 0

    def __str__(self, level=0):
        ret = "  " * level + f"{self.node_type} {self.node_value if self.node_value else ''}\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def visualize(self, graph=None, parent=None):
        if graph is None:
            graph = Digraph(node_attr={'shape': 'rectangle', 'fontname': 'Arial'})

        # Create a label for the node based on its type and value
        node_label = f"{self.node_type}: {self.node_value if self.node_value else ''}"
        # Each node must have a unique identifier
        node_id = str(id(self))
        graph.node(node_id, label=node_label)

        if parent:
            graph.edge(parent, node_id)

        for child in self.children:
            child.visualize(graph, node_id)

        return graph



markdown_text = """
# Heading 1
### Heading 3 with *italic*
[some **bold** link](http://example.com)
[Link](http://example.com)
![Image](http://example.com/img.png)
Text   here
*italic* **bold** ***bold AND italic***
*italic text* **[some link](http://example.com) some other text** ***bold AND italic***
"""


example_tokens = lexer(markdown_text)
print("Lexer output:\n")
for example_token in example_tokens:
    print(example_token)


print("\n===========================\nAST:\n")
node = Node(NodeType.ROOT, None, example_tokens)
print(node)

graph = node.visualize()
graph.render('output', view=True)
