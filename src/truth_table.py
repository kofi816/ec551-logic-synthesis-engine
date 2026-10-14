"""Generate a truth table from the expression tree returned by parser.py."""

from itertools import product
from parser import NodeType, parse, get_variables
import sys


def evaluate(node, values):
    """Evaluate one parser tree for one assignment of input values."""

    if node.type == NodeType.INPUT:
        return values[node.name]

    if node.type == NodeType.NOT:
        return not evaluate(node.inputs[0], values)

    if node.type == NodeType.AND:
        return all(
            evaluate(child, values)
            for child in node.inputs
        )

    if node.type == NodeType.OR:
        return any(
            evaluate(child, values)
            for child in node.inputs
        )

    raise ValueError(
        f"Unknown node type: {node.type}"
    )


def generate_truth_table(tree):
    """Generate every input combination and its output."""

    variables = get_variables(tree)
    table = []

    for bits in product(
        [0, 1],
        repeat=len(variables)
    ):

        values = dict(
            zip(variables, bits)
        )

        output = int(
            evaluate(tree, values)
        )

        table.append(
            (values, output)
        )

    return variables, table


def main():

    if len(sys.argv) < 2:

        print(
            'Usage: python3 src/truth_table.py "A\'B\' + AB"'
        )

        sys.exit(1)

    # Get Boolean expression from command line
    expression = " ".join(
        sys.argv[1:]
    )

    # Call parser.py
    tree = parse(expression)

    # Generate truth table from returned parser tree
    variables, table = generate_truth_table(tree)

    print()
    print("Expression:")
    print(expression)

    print()
    print("Parsed representation:")
    print(tree)

    print()
    print("Truth table:")

    print(
        " | ".join(variables + ["F"])
    )

    print(
        "-" * (4 * (len(variables) + 1) - 1)
    )

    for values, output in table:

        row = [
            str(values[var])
            for var in variables
        ]

        print(
            " | ".join(row + [str(output)])
        )

    print()


if __name__ == "__main__":
    main()