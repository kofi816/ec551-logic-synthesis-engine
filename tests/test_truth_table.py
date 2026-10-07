"""Run a set of truth-table inputs one after another."""

import subprocess


test_inputs = [
    "AB",
    "A AND B",
    "A&B",
    "A*B",

    "~A",
    "NOT A",
    "!A",
    "A'",

    "A+B",
    "A OR B",
    "A|B",

    "(A+B)C",
    "(A+B)(C+D)",
    "~(A+B)",
    "(A+B)'",
    "A+B'C",

    "A'B' + AB",
]


for expression in test_inputs:

    print("=" * 50)
    print(f"Testing truth table: {expression}")
    print("=" * 50)

    subprocess.run(
        ["python3", "src/truth_table.py", expression],
        check=False,
    )

    print()