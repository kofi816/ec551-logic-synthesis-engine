from parser import parse
from truth_table import generate_truth_table
from on_off_set import generate_on_off_sets
from minimization import minimize
from generator import generate_verilog


expression = input("Enter a Boolean expression: ")

tree = parse(expression)
variables, table = generate_truth_table(tree)
on_set, off_set = generate_on_off_sets(variables, table)
result = minimize(variables, on_set, off_set)
verilog_path = generate_verilog(variables, result["sop_cubes"], "output/generated_logic.v")

print()
print("Expression:", expression)
print("Variables:", variables)
print("ON-set:", on_set)
print("OFF-set:", off_set)
print()
print("Minimized SOP:", result["minimized_sop"])
print("Minimized POS:", result["minimized_pos"])
print("Prime implicants:", result["prime_implicants"])
print("Prime implicant count:", result["prime_implicant_count"])
print("Essential prime implicants:", result["essential_prime_implicants"])
print("Essential prime implicant count:", result["essential_prime_implicant_count"])
print("SOP literals saved:", result["sop_literals_saved"])
print("POS literals saved:", result["pos_literals_saved"])
print("Structural Verilog file:", verilog_path)
