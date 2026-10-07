"""Simple checks for src/minimization.py.

Run from the project folder: python tests/test_minimization.py
"""

import sys
from pathlib import Path

# Let this test file import minimization.py from the src folder.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from minimization import minimize


def show_result(title, variables, on_set, off_set, result):
    print("=" * 50)
    print("Testing minimization:", title)
    print("=" * 50)
    print("Input:")
    print("  Variables:", variables)
    print("  ON-set:", on_set)
    print("  OFF-set:", off_set)
    print("Output:")
    print("  Minimized SOP:", result["minimized_sop"])
    print("  Minimized POS:", result["minimized_pos"])
    print("  Prime implicants:", result["prime_implicants"])
    print("  Prime implicant count:", result["prime_implicant_count"])
    print("  Essential prime implicants:", result["essential_prime_implicants"])
    print("  Essential prime implicant count:", result["essential_prime_implicant_count"])
    print("  SOP literals saved:", result["sop_literals_saved"])
    print("  POS literals saved:", result["pos_literals_saved"])


def test_current_example():
    variables = ["A", "B", "C"]
    on_set = [1, 5, 7]
    off_set = [0, 2, 3, 4, 6]

    result = minimize(variables, on_set, off_set)
    show_result("current example", variables, on_set, off_set, result)

    assert set(result["minimized_sop"].split(" + ")) == {"AC", "B'C"}
    assert result["minimized_pos"] == "(A+B')(C)"
    assert set(result["prime_implicants"]) == {"AC", "B'C"}
    assert set(result["essential_prime_implicants"]) == {"AC", "B'C"}
    assert result["prime_implicant_count"] == 2
    assert result["essential_prime_implicant_count"] == 2
    assert result["sop_literals_saved"] == 5
    assert result["pos_literals_saved"] == 12


def test_function_equal_to_c():
    variables = ["A", "B", "C"]
    on_set = [1, 3, 5, 7]
    off_set = [0, 2, 4, 6]
    result = minimize(variables, on_set, off_set)
    show_result("function simplifies to C", variables, on_set, off_set, result)

    assert result["minimized_sop"] == "C"
    assert result["minimized_pos"] == "(C)"
    assert result["prime_implicants"] == ["C"]
    assert result["essential_prime_implicants"] == ["C"]
    assert result["sop_literals_saved"] == 11
    assert result["pos_literals_saved"] == 11


def test_constant_outputs():
    variables = ["A", "B"]

    zero_on_set = []
    zero_off_set = [0, 1, 2, 3]
    always_zero = minimize(variables, zero_on_set, zero_off_set)
    show_result("constant 0", variables, zero_on_set, zero_off_set, always_zero)
    assert always_zero["minimized_sop"] == "0"
    assert always_zero["minimized_pos"] == "0"
    assert always_zero["prime_implicant_count"] == 0

    one_on_set = [0, 1, 2, 3]
    one_off_set = []
    always_one = minimize(variables, one_on_set, one_off_set)
    show_result("constant 1", variables, one_on_set, one_off_set, always_one)
    assert always_one["minimized_sop"] == "1"
    assert always_one["minimized_pos"] == "1"
    assert always_one["prime_implicant_count"] == 1


def test_invalid_input():
    variables = ["A", "B"]
    on_set = [0, 1]
    off_set = [1, 2, 3]
    print("=" * 50)
    print("Testing minimization: overlapping ON-set and OFF-set")
    print("=" * 50)
    print("Input:")
    print("  Variables:", variables)
    print("  ON-set:", on_set)
    print("  OFF-set:", off_set)
    try:
        minimize(variables, on_set, off_set)
    except ValueError as error:
        print("Output: ValueError:", error)
    else:
        raise AssertionError("Overlapping ON-set and OFF-set should fail")


if __name__ == "__main__":
    test_current_example()
    print("PASS\n")

    test_function_equal_to_c()
    print("PASS\n")

    test_constant_outputs()
    print("PASS\n")

    test_invalid_input()
    print("PASS\n")

    print("All 4 minimization tests passed.")
