from Grammar import Grammar


def pretty_print(grammar):
    # Mapping available superscript characters including capital letters
    superscript_map = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
        'a': 'ᵃ', 'b': 'ᵇ', 'c': 'ᶜ', 'd': 'ᵈ', 'e': 'ᵉ',
        'f': 'ᶠ', 'g': 'ᵍ', 'h': 'ʰ', 'i': 'ⁱ', 'j': 'ʲ',
        'k': 'ᵏ', 'l': 'ˡ', 'm': 'ᵐ', 'n': 'ⁿ', 'o': 'ᵒ',
        'p': 'ᵖ', 'q': 'ᵠ', 'r': 'ʳ', 's': 'ˢ', 't': 'ᵗ',
        'u': 'ᵘ', 'v': 'ᵛ', 'w': 'ʷ', 'x': 'ˣ', 'y': 'ʸ', 'z': 'ᶻ',
        'A': 'ᴬ', 'B': 'ᴮ', 'C': 'ᶜ', 'D': 'ᴰ', 'E': 'ᴱ',
        'F': 'ᶠ', 'G': 'ᴳ', 'H': 'ᴴ', 'I': 'ᴵ', 'J': 'ᴶ',
        'K': 'ᴷ', 'L': 'ᴸ', 'M': 'ᴹ', 'N': 'ᴺ', 'O': 'ᴼ',
        'P': 'ᴾ', 'Q': 'ᵠ', 'R': 'ᴿ', 'S': 'ˢ', 'T': 'ᵀ',
        'U': 'ᵁ', 'V': 'ⱽ', 'W': 'ᵂ', 'X': 'ˣ', 'Y': 'ᵞ', 'Z': 'ᶻ'
    }

    # Convert internal representation to pretty output
    for nonterminal, productions in grammar.productions.items():
        readable_productions = []
        for production in productions:
            readable_production = []
            for symbol in production:
                if '_' in symbol:  # Assume superscript follows an underscore
                    parts = symbol.split('_')
                    # Convert to superscript if possible
                    superscript = ''.join(superscript_map.get(char, char) for char in parts[1])
                    readable_production.append(parts[0] + superscript)
                else:
                    readable_production.append(symbol)
            readable_productions.append(' '.join(readable_production))
        print(f"{nonterminal} -> {' | '.join(readable_productions)}")


grammar = Grammar("S", {
            'S': [['A']],
            'A': [['d'], ['d', 'S'], ['a', 'A', 'd', 'A', 'B']],
            'B': [['a', 'C'], ['a', 'S'], ['A', 'C']],
            'C': [['ε']],
            'E': [['A', 'S']],
        })

pretty_print(grammar)

print("\nSTART Transformation:")
grammar.eliminate_start_symbol()
pretty_print(grammar)

print("\nDEL Transformation:")
grammar.eliminate_epsilon_rules()
pretty_print(grammar)

print("\nTERM Transformation:")
grammar.eliminate_nonsolitary_terminals()
pretty_print(grammar)

print("\nBIN Transformation:")
grammar.eliminate_rhs_with_more_than_two_nonterminals()
pretty_print(grammar)

print("\nUNIT Transformation:")
grammar.eliminate_unit_rules()
pretty_print(grammar)

