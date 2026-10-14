"""Generate ON-set and OFF-set minterm indices from a truth table."""

import sys

from parser import parse
from truth_table import generate_truth_table


def generate_on_off_sets(variables, table):
    """Generate ON-set and OFF-set minterm indices from truth-table rows."""

    on_set = []
    off_set = []

    for values, output in table:

        # Convert the input values into a binary number
        bits = "".join(
            str(values[var])
            for var in variables
        )

        # Convert binary to its minterm number
        minterm = int(bits, 2)

        # Output 1 -> ON-set
        if output == 1:
            on_set.append(minterm)

        # Output 0 -> OFF-set
        else:
            off_set.append(minterm)

    return on_set, off_set


def main():

    if len(sys.argv) < 2:

        print(
            'Usage: python3 src/on_off_set.py "A\'B\' + AB"'
        )

        sys.exit(1)

    expression = " ".join(
        sys.argv[1:]
    )

    # Parse expression
    tree = parse(expression)

    # Call truth_table.py
    variables, table = generate_truth_table(tree)

    # Generate ON-set and OFF-set from returned truth table
    on_set, off_set = generate_on_off_sets(
        variables,
        table
    )

    print()
    print("Expression:")
    print(expression)

    print()
    print("Variables:")
    print(variables)

    print()
    print("ON-set:")
    print(on_set)

    print()
    print("OFF-set:")
    print(off_set)

    print()


if __name__ == "__main__":
    main()