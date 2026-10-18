"""Generate canonical SOP/POS and inverse canonical SOP/POS."""

import sys

from parser import parse
from truth_table import generate_truth_table
from on_off_set import generate_on_off_sets


def minterm_expression(index, variables):
    """Convert a minterm index into its Boolean product term."""

    bits = format(
        index,
        f"0{len(variables)}b"
    )

    literals = []

    for variable, bit in zip(variables, bits):

        if bit == "1":
            literals.append(variable)

        else:
            literals.append(variable + "'")

    return "".join(literals)


def maxterm_expression(index, variables):
    """Convert a maxterm index into its Boolean sum term."""

    bits = format(
        index,
        f"0{len(variables)}b"
    )

    literals = []

    for variable, bit in zip(variables, bits):

        if bit == "0":
            literals.append(variable)

        else:
            literals.append(variable + "'")

    return "(" + "+".join(literals) + ")"


def canonical_sop(indices, variables):
    """Build canonical SOP from minterm indices."""

    if not indices:
        return "0"

    return " + ".join(
        minterm_expression(index, variables)
        for index in indices
    )


def canonical_pos(indices, variables):
    """Build canonical POS from maxterm indices."""

    if not indices:
        return "1"

    return "".join(
        maxterm_expression(index, variables)
        for index in indices
    )


def generate_canonical_forms(
    variables,
    on_set,
    off_set
):
    """Generate canonical forms for F and F'."""

    # F
    sop = canonical_sop(
        on_set,
        variables
    )

    pos = canonical_pos(
        off_set,
        variables
    )

    # F'
    inverse_sop = canonical_sop(
        off_set,
        variables
    )

    inverse_pos = canonical_pos(
        on_set,
        variables
    )

    return (
        sop,
        pos,
        inverse_sop,
        inverse_pos
    )


def main():

    if len(sys.argv) < 2:

        print(
            'Usage: python3 src/canonical.py "A\'B\' + AB"'
        )

        sys.exit(1)

    expression = " ".join(
        sys.argv[1:]
    )

    # Parse expression
    tree = parse(expression)

    # Generate truth table
    variables, table = generate_truth_table(tree)

    # Generate ON-set and OFF-set
    on_set, off_set = generate_on_off_sets(
        variables,
        table
    )

    # Generate canonical forms
    (
        sop,
        pos,
        inverse_sop,
        inverse_pos
    ) = generate_canonical_forms(
        variables,
        on_set,
        off_set
    )

    print()
    print("Expression:")
    print(expression)

    print()
    print("Canonical SOP:")
    print(sop)

    print()
    print("Canonical POS:")
    print(pos)

    print()
    print("Inverse Canonical SOP:")
    print(inverse_sop)

    print()
    print("Inverse Canonical POS:")
    print(inverse_pos)

    print()


if __name__ == "__main__":
    main()