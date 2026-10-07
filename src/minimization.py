
def validate(variables, on_set, off_set):
    """Reject input that is not a complete truth table."""
    if not variables:
        raise ValueError("variables cannot be empty")

    for name in variables:
        if not isinstance(name, str) or len(name) != 1 or not name.isalpha():
            raise ValueError("variables must be single-letter names")

    if len(set(variables)) != len(variables):
        raise ValueError("variables must be unique")

    number_of_rows = 2 ** len(variables)

    for index in on_set:
        if type(index) is not int or index < 0 or index >= number_of_rows:
            raise ValueError(f"on_set has an invalid index: {index}")
    if len(set(on_set)) != len(on_set):
        raise ValueError("on_set contains duplicate indices")

    for index in off_set:
        if type(index) is not int or index < 0 or index >= number_of_rows:
            raise ValueError(f"off_set has an invalid index: {index}")
    if len(set(off_set)) != len(off_set):
        raise ValueError("off_set contains duplicate indices")

    if set(on_set) & set(off_set):
        raise ValueError("ON-set and OFF-set cannot overlap")

    all_rows = set(range(number_of_rows))
    if set(on_set) | set(off_set) != all_rows:
        raise ValueError("ON-set and OFF-set must cover every input row")


def covers(cube, index, width):
    """Return True if a cube includes the row numbered index."""
    for position in range(width):
        cube_bit = cube[position]
        row_bit = (index >> (width - 1 - position)) & 1

        if cube_bit is not None and cube_bit != row_bit:
            return False

    return True


def find_prime_implicants(minterms, width):
    """Merge minterms until no larger cubes can be made."""
    current = set()

    # Convert each integer index to a tuple of bits.
    for index in minterms:
        bits = []
        for position in range(width):
            bit = (index >> (width - 1 - position)) & 1
            bits.append(bit)
        current.add(tuple(bits))

    primes = set()

    while current:
        current_list = list(current)
        merged_cubes = set()
        next_level = set()

        # Two cubes merge if exactly one fixed bit differs.
        for i in range(len(current_list)):
            for j in range(i + 1, len(current_list)):
                first = current_list[i]
                second = current_list[j]
                different_positions = []

                for position in range(width):
                    if first[position] != second[position]:
                        different_positions.append(position)

                if len(different_positions) == 1:
                    position = different_positions[0]
                    if first[position] is not None and second[position] is not None:
                        combined = list(first)
                        combined[position] = None
                        next_level.add(tuple(combined))
                        merged_cubes.add(first)
                        merged_cubes.add(second)

        # Anything that could not merge is a prime implicant.
        for cube in current:
            if cube not in merged_cubes:
                primes.add(cube)

        current = next_level

    return sorted(primes, key=str)


def literal_count(cubes):
    """Count all fixed bits in a collection of cubes."""
    count = 0
    for cube in cubes:
        for bit in cube:
            if bit is not None:
                count += 1
    return count


def choose_cover(primes, minterms, width):
    """Find essential primes and a cover with the fewest literals."""
    if not minterms:
        return [], []

    # For each prime, record which rows it covers.
    covered_by_prime = []
    for cube in primes:
        covered_rows = set()
        for index in minterms:
            if covers(cube, index, width):
                covered_rows.add(index)
        covered_by_prime.append(covered_rows)

    # A prime is essential if it is the only one covering some row.
    essential_indices = set()
    for index in minterms:
        covering_indices = []
        for prime_index in range(len(primes)):
            if index in covered_by_prime[prime_index]:
                covering_indices.append(prime_index)
        if len(covering_indices) == 1:
            essential_indices.add(covering_indices[0])

    initial_covered = set()
    for prime_index in essential_indices:
        initial_covered.update(covered_by_prime[prime_index])

    best_indices = None
    best_score = None

    def search(selected_indices, covered_rows):
        nonlocal best_indices, best_score

        remaining = set(minterms) - covered_rows
        if not remaining:
            chosen = sorted(selected_indices)
            chosen_cubes = []
            for prime_index in chosen:
                chosen_cubes.append(primes[prime_index])
            score = (literal_count(chosen_cubes), len(chosen), chosen)
            if best_score is None or score < best_score:
                best_score = score
                best_indices = chosen
            return

        # Pick one uncovered row, then try each prime that can cover it.
        row = min(remaining)
        for prime_index in range(len(primes)):
            if row in covered_by_prime[prime_index]:
                if prime_index not in selected_indices:
                    next_selected = selected_indices | {prime_index}
                    next_covered = covered_rows | covered_by_prime[prime_index]
                    search(next_selected, next_covered)

    search(essential_indices, initial_covered)

    assert best_indices is not None
    selected_cubes = []
    for prime_index in best_indices:
        selected_cubes.append(primes[prime_index])

    essential_cubes = []
    for prime_index in sorted(essential_indices):
        essential_cubes.append(primes[prime_index])
    return selected_cubes, essential_cubes


def sop_term(cube, variables):
    """Example: (0, 1, None) -> A'B."""
    literals = []
    for position in range(len(variables)):
        name = variables[position]
        bit = cube[position]
        if bit == 1:
            literals.append(name)
        elif bit == 0:
            literals.append(name + "'")
    return "".join(literals) if literals else "1"


def pos_term(cube, variables):
    """Make a POS sum term from a cube where the function is zero."""
    literals = []
    for position in range(len(variables)):
        name = variables[position]
        bit = cube[position]
        if bit == 0:
            literals.append(name)
        elif bit == 1:
            literals.append(name + "'")
    return "(" + "+".join(literals) + ")" if literals else "0"


def minimize(variables, on_set, off_set):
    """Return minimized expressions, implicants, and literal savings."""
    validate(variables, on_set, off_set)
    width = len(variables)

    on_primes = find_prime_implicants(on_set, width)
    sop_cover, essential_primes = choose_cover(on_primes, on_set, width)

    # Minimize the OFF-set, then invert its cubes to produce POS terms.
    off_primes = find_prime_implicants(off_set, width)
    pos_cover, unused_essentials = choose_cover(off_primes, off_set, width)

    sop_terms = []
    for cube in sop_cover:
        sop_terms.append(sop_term(cube, variables))
    minimized_sop = " + ".join(sop_terms) if sop_terms else "0"

    pos_terms = []
    for cube in pos_cover:
        pos_terms.append(pos_term(cube, variables))
    minimized_pos = "".join(pos_terms) if pos_terms else "1"

    prime_terms = []
    for cube in on_primes:
        prime_terms.append(sop_term(cube, variables))

    essential_terms = []
    for cube in essential_primes:
        essential_terms.append(sop_term(cube, variables))

    result = {
        "minimized_sop": minimized_sop,
        "minimized_pos": minimized_pos,
        "prime_implicants": prime_terms,
        "prime_implicant_count": len(prime_terms),
        "essential_prime_implicants": essential_terms,
        "essential_prime_implicant_count": len(essential_terms),
        "sop_literals_saved": len(on_set) * width - literal_count(sop_cover),
        "pos_literals_saved": len(off_set) * width - literal_count(pos_cover),
    }
    return result


if __name__ == "__main__":
    variables = ["A", "B", "C"]
    on_set = [1, 5, 7]
    off_set = [0, 2, 3, 4, 6]

    result = minimize(variables, on_set, off_set)
    print("Minimized SOP:", result["minimized_sop"])
    print("Minimized POS:", result["minimized_pos"])
    print("Prime implicants:", result["prime_implicants"])
    print("Prime implicant count:", result["prime_implicant_count"])
    print("Essential prime implicants:", result["essential_prime_implicants"])
    print("Essential prime implicant count:", result["essential_prime_implicant_count"])
    print("SOP literals saved:", result["sop_literals_saved"])
    print("POS literals saved:", result["pos_literals_saved"])
