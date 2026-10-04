"""Run a set of parser inputs one after another."""

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
]


for expression in test_inputs:

    print("=" * 50)
    print(f"Testing: {expression}")
    print("=" * 50)

    subprocess.run(
        ["python3", "src/parser.py", expression],
        check=False,
    )

    print()