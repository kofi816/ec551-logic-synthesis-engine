"""
Boolean expression parser for the EC551 Logic Synthesis Engine.

All accepted Boolean notation is converted into four internal gate types:

    INPUT
    NOT
    AND
    OR

Examples:

    AB
    A AND B
    A&B
    A*B

all become:

    AND(A, B)


    A'
    ~A
    !A
    NOT A

all become:

    NOT(A)


    A+B
    A OR B
    A|B

all become:

    OR(A, B)


Operator precedence:

    1. NOT
    2. AND
    3. OR

Variables are currently single letters: A, B, C, ...
"""

from dataclasses import dataclass
from enum import Enum
import sys


# ============================================================
# Internal gate representation
# ============================================================

class NodeType(Enum):
    INPUT = "INPUT"
    NOT = "NOT"
    AND = "AND"
    OR = "OR"


@dataclass
class Node:
    type: NodeType
    inputs: tuple = ()
    name: str | None = None

    def __str__(self):

        # Input variable
        if self.type == NodeType.INPUT:
            return self.name

        # NOT gate
        if self.type == NodeType.NOT:
            return f"NOT({self.inputs[0]})"

        # AND or OR gate
        children = ", ".join(str(child) for child in self.inputs)

        return f"{self.type.value}({children})"


# ============================================================
# Tokenizer
# ============================================================

def tokenize(expression):
    """
    Convert the user's expression into tokens.

    Example:

        A'B + ~C

    becomes approximately:

        VAR A
        POST_NOT
        VAR B
        OR
        NOT
        VAR C
    """

    tokens = []

    i = 0

    while i < len(expression):

        # Ignore spaces
        if expression[i].isspace():
            i += 1
            continue

        # ----------------------------------------------------
        # Word operators: AND, OR, NOT
        # ----------------------------------------------------

        matched_word = False

        for word, token_type in (
            ("NOT", "NOT"),
            ("AND", "AND"),
            ("OR", "OR")
        ):

            end = i + len(word)

            if expression[i:end].upper() == word:

                # Make sure AND/OR/NOT are separate words.
                #
                # Example:
                #
                # A AND B
                #
                # should detect AND.

                before_ok = (
                    i == 0
                    or not expression[i - 1].isalnum()
                )

                after_ok = (
                    end == len(expression)
                    or not expression[end].isalnum()
                )

                if before_ok and after_ok:

                    tokens.append(
                        (token_type, word)
                    )

                    i = end

                    matched_word = True

                    break

        if matched_word:
            continue

        # ----------------------------------------------------
        # Single-character operators / variables
        # ----------------------------------------------------

        char = expression[i]

        # Variable
        if char.isalpha():

            tokens.append(
                ("VAR", char.upper())
            )

        # Postfix NOT
        elif char == "'":

            tokens.append(
                ("POST_NOT", char)
            )

        # Prefix NOT
        elif char in ("~", "!"):

            tokens.append(
                ("NOT", char)
            )

        # AND
        elif char in ("&", "*"):

            tokens.append(
                ("AND", char)
            )

        # OR
        elif char in ("+", "|"):

            tokens.append(
                ("OR", char)
            )

        # Left parenthesis
        elif char == "(":

            tokens.append(
                ("LPAREN", char)
            )

        # Right parenthesis
        elif char == ")":

            tokens.append(
                ("RPAREN", char)
            )

        else:

            raise SyntaxError(
                f"Invalid character: {char}"
            )

        i += 1

    # Marks the end of the expression
    tokens.append(
        ("EOF", "")
    )

    return tokens


# ============================================================
# Parser
# ============================================================

class Parser:

    def __init__(self, expression):

        self.tokens = tokenize(expression)

        self.position = 0


    # --------------------------------------------------------
    # Get current token type
    # --------------------------------------------------------

    def current_type(self):

        return self.tokens[self.position][0]


    # --------------------------------------------------------
    # Consume expected token
    # --------------------------------------------------------

    def consume(self, expected_type):

        token_type, value = self.tokens[self.position]

        if token_type != expected_type:

            raise SyntaxError(
                f"Expected {expected_type}, found '{value}'"
            )

        self.position += 1

        return token_type, value


    # ========================================================
    # Parse complete expression
    # ========================================================

    def parse(self):

        if self.current_type() == "EOF":

            raise SyntaxError(
                "Expression cannot be empty"
            )

        tree = self.parse_or()

        # There should be nothing left after parsing
        if self.current_type() != "EOF":

            value = self.tokens[self.position][1]

            raise SyntaxError(
                f"Unexpected token '{value}'"
            )

        return tree


    # ========================================================
    # OR
    #
    # A + B
    # A OR B
    # A | B
    # ========================================================

    def parse_or(self):

        nodes = [
            self.parse_and()
        ]

        while self.current_type() == "OR":

            self.consume("OR")

            nodes.append(
                self.parse_and()
            )

        # No OR required
        if len(nodes) == 1:
            return nodes[0]

        # Create OR gate
        return Node(
            NodeType.OR,
            tuple(nodes)
        )


    # ========================================================
    # AND
    #
    # Explicit AND:
    #
    # A AND B
    # A & B
    # A * B
    #
    # Implicit AND:
    #
    # AB
    # A'B
    # A(B+C)
    # (A+B)(C+D)
    # ========================================================

    def parse_and(self):

        nodes = [
            self.parse_not()
        ]

        while True:

            # ------------------------------------------------
            # Explicit AND
            # ------------------------------------------------

            if self.current_type() == "AND":

                self.consume("AND")

                nodes.append(
                    self.parse_not()
                )

            # ------------------------------------------------
            # Implicit AND
            #
            # If another variable, NOT, or "(" immediately
            # follows, treat it as AND.
            #
            # AB
            # A~B
            # A(B+C)
            # ------------------------------------------------

            elif self.current_type() in (
                "VAR",
                "NOT",
                "LPAREN"
            ):

                nodes.append(
                    self.parse_not()
                )

            else:

                break

        # Only one term means no AND gate is necessary
        if len(nodes) == 1:
            return nodes[0]

        return Node(
            NodeType.AND,
            tuple(nodes)
        )


    # ========================================================
    # NOT
    #
    # Prefix:
    #
    # ~A
    # !A
    # NOT A
    #
    # Postfix:
    #
    # A'
    #
    # Parentheses:
    #
    # ~(A+B)
    # (A+B)'
    # ========================================================

    def parse_not(self):

        # Prefix NOT
        if self.current_type() == "NOT":

            self.consume("NOT")

            child = self.parse_not()

            node = Node(
                NodeType.NOT,
                (child,)
            )

        else:

            node = self.parse_primary()

        # Postfix NOT
        #
        # Example:
        #
        # A'
        #
        # or
        #
        # (A+B)'

        while self.current_type() == "POST_NOT":

            self.consume("POST_NOT")

            node = Node(
                NodeType.NOT,
                (node,)
            )

        return node


    # ========================================================
    # Variables and parentheses
    # ========================================================

    def parse_primary(self):

        # ----------------------------------------------------
        # Variable
        # ----------------------------------------------------

        if self.current_type() == "VAR":

            _, variable = self.consume("VAR")

            return Node(
                NodeType.INPUT,
                name=variable
            )

        # ----------------------------------------------------
        # Parenthesized expression
        # ----------------------------------------------------

        if self.current_type() == "LPAREN":

            self.consume("LPAREN")

            node = self.parse_or()

            self.consume("RPAREN")

            return node

        # ----------------------------------------------------
        # Invalid syntax
        # ----------------------------------------------------

        value = self.tokens[self.position][1]

        raise SyntaxError(
            f"Expected variable or '(', found '{value}'"
        )


# ============================================================
# Public parse function
# ============================================================

def parse(expression):

    parser = Parser(expression)

    return parser.parse()


# ============================================================
# Get variables from parsed expression
# ============================================================

def get_variables(node):

    # Input node
    if node.type == NodeType.INPUT:

        return [node.name]

    variables = set()

    # Search children
    for child in node.inputs:

        variables.update(
            get_variables(child)
        )

    return sorted(variables)


# ============================================================
# CLI
# ============================================================

def main():

    # Make sure an expression was provided
    if len(sys.argv) < 2:

        print("Usage:")

        print(
            "python src/parser.py \"A'B' + AB\""
        )

        sys.exit(1)

    # Join CLI arguments into one expression
    expression = " ".join(
        sys.argv[1:]
    )

    try:

        tree = parse(expression)

        print()
        print("Input:")
        print(expression)

        print()
        print("Variables:")
        print(get_variables(tree))

        print()
        print("Internal gate representation:")
        print(tree)

        print()

    except SyntaxError as error:

        print()
        print("Syntax error:")
        print(error)
        print()

        sys.exit(1)

if __name__ == "__main__":
    main()