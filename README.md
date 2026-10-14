# ec551-logic-synthesis-engine

Programming Assignment 1 on logic synthesis engine.

## System Architecture

```text
Input
  ↓
Parser
  ↓
Truth table / ON-OFF sets
  ↓
Canonical forms
  ↓
Minimizer
  ↓
Prime implicants
  ↓
Minimized expression
  ↓
Structural Verilog
  ↓
FPGA
```

## Testing the Parser

To test a Boolean expression manually, run:

```bash
python3 src/parser.py "A'B' + AB"
```

Replace the expression in quotes with any expression you want to test.

To run all predefined parser test cases at once, run:

```bash
python3 tests/test_parser.py
```

## Testing the Truth Table Generation

To test a Boolean expression manually, run:

```bash
python3 src/truth_table.py "A'B' + AB"
```

Replace the expression in quotes with any expression you want to test.

To run all predefined truth-table test cases at once, run:

```bash
python3 tests/test_truth_table.py
```

## Testing the Top-Level Logic Synthesis Engine

The top-level program runs the complete logic synthesis flow:

```text
Input expression
  ↓
Parser
  ↓
Truth table
  ↓
ON-set / OFF-set
  ↓
Canonical forms
  ↓
Minimization
  ↓
Structural Verilog
```

There are two ways to run the top-level program:

1. Interactive CLI mode for a single expression
2. Input file mode for one or more expressions

### Interactive CLI Mode

To enter and process a single Boolean expression from the terminal, run:

```bash
python3 src/top.py
```

The program will prompt:

```text
Enter a Boolean expression:
```

For example, enter:

```text
A'B' + AB
```

The complete result is printed to the terminal.

The same result is also saved to:

```text
output/cli_result.txt
```

The generated structural Verilog is saved to:

```text
output/generated_logic.v
```

### Input File Mode

Multiple Boolean expressions can be processed automatically from an input file.

Place the expressions in:

```text
input/expressions.txt
```

Each line should contain one Boolean expression.

For example:

```text
A'B' + AB
A + B
AB + AC
A'BC + ABC'
```

Then run:

```bash
python3 src/top.py input/expressions.txt
```

The program processes each expression in order.

The results for all expressions are printed to the terminal and also saved to:

```text
output/expressions_result.txt
```

Each expression is separated in the result file so that its truth table, canonical forms, minimized forms, and other results can be viewed independently.

### Verilog Output for Multiple Expressions

When using input file mode, each Boolean expression receives its own structural Verilog file.

For example, if `expressions.txt` contains four expressions, the program generates:

```text
output/generated_logic_1.v
output/generated_logic_2.v
output/generated_logic_3.v
output/generated_logic_4.v
```

This prevents the Verilog generated for one expression from overwriting the Verilog generated for another expression.

### Top-Level Output

For each Boolean expression, `top.py` generates:

- Variables
- Truth table
- ON-set
- Total number of ON-set minterms
- OFF-set
- Total number of OFF-set minterms
- Canonical SOP
- Canonical POS
- Inverse canonical SOP
- Inverse canonical POS
- Minimized SOP
- Minimized POS
- Prime implicants
- Prime implicant count
- Essential prime implicants
- Essential prime implicant count
- SOP literal savings
- POS literal savings
- Structural Verilog output path

### Example Commands

Process one expression interactively:

```bash
python3 src/top.py
```

Process all expressions in the default input file:

```bash
python3 src/top.py input/expressions.txt
```

## Project Structure

```text
ec551-logic-synthesis-engine/
│
├── src/
│   ├── top.py
│   ├── parser.py
│   ├── truth_table.py
│   ├── on_off_set.py
│   ├── canonical.py
│   ├── minimization.py
│   └── generator.py
│
├── input/
│   └── expressions.txt
│
├── output/
│   ├── cli_result.txt
│   ├── expressions_result.txt
│   ├── generated_logic.v
│   ├── generated_logic_1.v
│   ├── generated_logic_2.v
│   └── ...
│
├── tests/
│   ├── test_parser.py
│   └── test_truth_table.py
│
└── README.md
```

## Team Split

### Paul — Front End & Logic Representation

- Input parser / expression handling
- Truth-table generation
- ON-set / OFF-set generation
- Canonical SOP
- Canonical POS
- Inverse SOP / POS
- Basic CLI
- Front-end testing

### Aaron — Minimization & Hardware Output

- Minimization engine
- Quine–McCluskey algorithm
- Prime implicant generation
- Essential prime implicant selection
- Literal-savings metrics
- Minimized POS generation
- Structural Verilog generator
- FPGA wrapper / Vivado deployment
- Minimizer and Verilog testing

### Shared

- Define interfaces between modules
- End-to-end testing and debugging
- Final FPGA validation