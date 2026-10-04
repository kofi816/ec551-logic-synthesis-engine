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