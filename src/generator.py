"""Write structural Verilog for a minimized SOP circuit.

Each cube has one bit per variable. A 1 uses the input, a 0 uses its
inverted input, and None means that input is absent from the term.
"""

from pathlib import Path


def generate_verilog(variables, sop_cubes, output_path):
    """Create a .v file and return its path."""
    if not variables or len(set(variables)) != len(variables):
        raise ValueError("variables must be a nonempty list of unique names")

    for name in variables:
        if not isinstance(name, str) or len(name) != 1 or not name.isascii() or not name.isalpha():
            raise ValueError("Verilog inputs must have single ASCII-letter names")

    for cube in sop_cubes:
        if len(cube) != len(variables):
            raise ValueError("each cube must have one bit per variable")
        for bit in cube:
            if bit not in (0, 1, None):
                raise ValueError("cube bits must be 0, 1, or None")

    always_one = False
    for cube in sop_cubes:
        if cube.count(None) == len(variables):
            always_one = True

    ports = []
    for name in variables:
        ports.append("input " + name)
    ports.append("output logic_out")

    lines = ["module generated_logic(" + ", ".join(ports) + ");"]

    if not sop_cubes:
        # No ON-set rows: the function is always zero.
        lines.append("    supply0 constant_zero;")
        lines.append("    buf g_output(logic_out, constant_zero);")
    elif always_one:
        # A cube with no fixed bits covers every row: the function is one.
        lines.append("    supply1 constant_one;")
        lines.append("    buf g_output(logic_out, constant_one);")
    else:
        inverted = []
        for position in range(len(variables)):
            for cube in sop_cubes:
                if cube[position] == 0:
                    inverted.append(variables[position])
                    break

        for name in inverted:
            lines.append("    wire not_" + name + ";")

        if len(sop_cubes) > 1:
            for term_number in range(len(sop_cubes)):
                lines.append("    wire term_" + str(term_number) + ";")

        for name in inverted:
            lines.append("    not g_not_" + name + "(not_" + name + ", " + name + ");")

        for term_number in range(len(sop_cubes)):
            cube = sop_cubes[term_number]
            term_inputs = []

            for position in range(len(variables)):
                if cube[position] == 1:
                    term_inputs.append(variables[position])
                elif cube[position] == 0:
                    term_inputs.append("not_" + variables[position])

            if len(sop_cubes) == 1:
                term_output = "logic_out"
            else:
                term_output = "term_" + str(term_number)

            if len(term_inputs) == 1:
                gate = "buf"
            else:
                gate = "and"

            connections = ", ".join([term_output] + term_inputs)
            lines.append("    " + gate + " g_term_" + str(term_number) + "(" + connections + ");")

        if len(sop_cubes) > 1:
            term_wires = []
            for term_number in range(len(sop_cubes)):
                term_wires.append("term_" + str(term_number))
            connections = ", ".join(["logic_out"] + term_wires)
            lines.append("    or g_output(" + connections + ");")

    lines.append("endmodule")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path
