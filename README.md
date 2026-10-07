# ec551-logic-synthesis-engine
Programming Assignment 1 on logic synthesis engine

System Architecture

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

To run all predefined parser test cases at once, run:

```bash
python3 tests/test_truth_table.py
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