"""Top-level driver for the logic synthesis engine."""

import os
import sys

from parser import parse
from truth_table import generate_truth_table
from on_off_set import generate_on_off_sets
from canonical import generate_canonical_forms
from minimization import minimize
from generator import generate_verilog
import csv

def export_truth_table_csv(variables, table, output_path):
    """Export a truth table to CSV with one column per input and F."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(list(variables) + ["F"])

        for values, output in table:
            writer.writerow([values[var] for var in variables] + [output])

def process_expression(expression, verilog_path):
    """Run the complete synthesis flow for one Boolean expression."""

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
        canonical_sop,
        canonical_pos,
        inverse_canonical_sop,
        inverse_canonical_pos
    ) = generate_canonical_forms(
        variables,
        on_set,
        off_set
    )

    # Minimize expression
    result = minimize(
        variables,
        on_set,
        off_set
    )

    # Generate structural Verilog
    generated_verilog_path = generate_verilog(
        variables,
        result["sop_cubes"],
        verilog_path
    )

    return {
        "expression": expression,
        "variables": variables,
        "table": table,
        "on_set": on_set,
        "off_set": off_set,
        "canonical_sop": canonical_sop,
        "canonical_pos": canonical_pos,
        "inverse_canonical_sop": inverse_canonical_sop,
        "inverse_canonical_pos": inverse_canonical_pos,
        "result": result,
        "verilog_path": generated_verilog_path
    }


def format_result(data):
    """Format one synthesis result for terminal and file output."""

    lines = []

    # Expression
    lines.append("Expression:")
    lines.append(data["expression"])

    # Variables
    lines.append("")
    lines.append("Variables:")
    lines.append(str(data["variables"]))

    # Truth table
    lines.append("")
    lines.append("Truth table:")

    lines.append(
        " | ".join(data["variables"] + ["F"])
    )

    lines.append(
        "-" * (4 * (len(data["variables"]) + 1) - 1)
    )

    for values, output in data["table"]:

        row = [
            str(values[var])
            for var in data["variables"]
        ]

        lines.append(
            " | ".join(row + [str(output)])
        )

    # ON-set
    lines.append("")
    lines.append("ON-set:")
    lines.append(str(data["on_set"]))

    lines.append(
        "Total number of ON-set minterms: "
        + str(len(data["on_set"]))
    )

    # OFF-set
    lines.append("")
    lines.append("OFF-set:")
    lines.append(str(data["off_set"]))

    lines.append(
        "Total number of OFF-set minterms: "
        + str(len(data["off_set"]))
    )

    # Canonical forms
    lines.append("")
    lines.append("Canonical SOP:")
    lines.append(data["canonical_sop"])

    lines.append("")
    lines.append("Canonical POS:")
    lines.append(data["canonical_pos"])

    lines.append("")
    lines.append("Inverse Canonical SOP:")
    lines.append(data["inverse_canonical_sop"])

    lines.append("")
    lines.append("Inverse Canonical POS:")
    lines.append(data["inverse_canonical_pos"])

    # Minimized forms
    lines.append("")
    lines.append("Minimized SOP:")
    lines.append(data["result"]["minimized_sop"])

    lines.append("")
    lines.append("Minimized POS:")
    lines.append(data["result"]["minimized_pos"])

    # Prime implicants
    lines.append("")
    lines.append("Prime implicants:")
    lines.append(
        str(data["result"]["prime_implicants"])
    )

    lines.append(
        "Prime implicant count: "
        + str(
            data["result"]["prime_implicant_count"]
        )
    )

    # Essential prime implicants
    lines.append("")
    lines.append("Essential prime implicants:")
    lines.append(
        str(
            data["result"][
                "essential_prime_implicants"
            ]
        )
    )

    lines.append(
        "Essential prime implicant count: "
        + str(
            data["result"][
                "essential_prime_implicant_count"
            ]
        )
    )

    # Literal savings
    lines.append("")
    lines.append(
        "SOP literals saved: "
        + str(
            data["result"]["sop_literals_saved"]
        )
    )

    lines.append(
        "POS literals saved: "
        + str(
            data["result"]["pos_literals_saved"]
        )
    )

    # Verilog output
    lines.append("")
    lines.append("Structural Verilog file:")
    lines.append(str(data["verilog_path"]))

    return "\n".join(lines)


def run_cli_mode():
    """Process one expression entered from the terminal."""

    expression = input(
        "Enter a Boolean expression: "
    ).strip()

    if not expression:
        print("No expression entered.")
        return

    # CLI Verilog output
    verilog_path = "output/generated_logic.v"

    data = process_expression(
        expression,
        verilog_path
    )


    export_truth_table_csv(
    data["variables"],
    data["table"],
    "output/truth_table.csv"
    )   

    output_text = format_result(data)

    # Print results to terminal
    print()
    print(output_text)
    print()

    # Save same results to file
    with open(
        "output/cli_result.txt",
        "w"
    ) as output_file:

        output_file.write(output_text)
        output_file.write("\n")

    print(
        "Results saved to: "
        "output/cli_result.txt"
    )


def run_file_mode(input_path):
    """Process all expressions from an input file."""

    # Read expressions from file
    with open(
        input_path,
        "r"
    ) as input_file:

        expressions = [
            line.strip()
            for line in input_file
            if line.strip()
        ]

    if not expressions:
        print(
            "No expressions found in input file."
        )
        return

    all_results = []

    # Process each expression
    for index, expression in enumerate(
        expressions,
        start=1
    ):

        # Give every expression its own
        # structural Verilog file
        verilog_path = (
            f"output/generated_logic_{index}.v"
        )

        data = process_expression(
            expression,
            verilog_path
        )

        export_truth_table_csv(
            data["variables"],
            data["table"],
            f"output/truth_table_{index}.csv"
        )

        output_text = format_result(data)

        # Separate each expression clearly
        section = (
            "=" * 60
            + f"\nExpression {index}\n"
            + "=" * 60
            + "\n\n"
            + output_text
        )

        all_results.append(section)

        # Also print each result to terminal
        print()
        print(section)

    # Combine all results into one text file
    combined_output = (
        "\n\n".join(all_results)
        + "\n"
    )

    with open(
        "output/expressions_result.txt",
        "w"
    ) as output_file:

        output_file.write(
            combined_output
        )

    print()
    print(
        "Results saved to: "
        "output/expressions_result.txt"
    )

    print(
        f"Generated {len(expressions)} "
        "Verilog file(s)."
    )


def main():
    """Select CLI mode or input-file mode."""

    # Make sure output directory exists
    os.makedirs(
        "output",
        exist_ok=True
    )

    # No argument:
    # Ask user for one expression
    if len(sys.argv) == 1:

        run_cli_mode()

    # One argument:
    # Treat it as an input file
    elif len(sys.argv) == 2:

        input_path = sys.argv[1]

        if not os.path.isfile(input_path):

            print(
                f"Input file not found: "
                f"{input_path}"
            )

            sys.exit(1)

        run_file_mode(
            input_path
        )

    # Too many arguments
    else:

        print("Usage:")

        print(
            "  python3 src/top.py"
        )

        print(
            "  python3 src/top.py "
            "input/expressions.txt"
        )

        sys.exit(1)


if __name__ == "__main__":
    main()