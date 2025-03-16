from time import perf_counter_ns as time

def get_prime_implicants(minterms):
    primeImplicants = []
    counter = 0
    while minterms:
        newMinterms = []
        merges = set()
        for i in range(len(minterms)):
            for j in range(i + 1, len(minterms)):
                minterm1 = minterms[i]
                minterm2 = minterms[j]
                if check_minterm_difference(minterm1, minterm2):
                    mergedMinterm = merge_minterms(minterm1, minterm2)
                    newMinterms.append(mergedMinterm)
                    merges.add(i)
                    merges.add(j)
        primeImplicants.extend([minterms[k] for k in range(len(minterms)) if k not in merges])
        minterms = list(set(newMinterms))
        counter += 1
##        print("counter:", counter)
##        print(minterms)
##    print("finished with prime implicants")
    return sorted(list(set(primeImplicants)))

def merge_minterms(minterm1, minterm2):
    return ''.join('-' if a != b else a for a, b in zip(minterm1, minterm2))

def check_minterm_difference(minterm1, minterm2):
    difference_count = 0
    for a, b in zip(minterm1, minterm2):
        if a != b:
            difference_count += 1
            if difference_count > 1:
                return False

    return difference_count == 1

def nums_to_binaries(nums, num_bits):
    return [bin(num)[2:].zfill(num_bits) for num in nums]

def representable_by_implicant(num, implicant):
    binary = bin(num)[2:].zfill(len(implicant))
    return all(implicant[i] == '-' or implicant[i] == binary[i] for i in range(len(implicant)))

def generate_implicant_table(trues, implicants):
    return [[representable_by_implicant(num, implicant) for num in trues] for implicant in implicants]

def find_needed_implicants(table, implicants):
    conditions_met = [False] * len(table[0])
    essential_implicants = []

    # Find essential implicants
    for col in range(len(table[0])):
        if sum(row[col] for row in table) == 1:
            for row_idx, row in enumerate(table):
                if row[col] and implicants[row_idx] not in essential_implicants:
                    essential_implicants.append(implicants[row_idx])
                    for k in range(len(conditions_met)):
                        if row[k]:
                            conditions_met[k] = True
                    break

    # Identify uncovered minterms
    uncovered_minterms = [i for i, covered in enumerate(conditions_met) if not covered]

    # Use a greedy algorithm to cover the remaining minterms
    needed_implicants = essential_implicants[:]
    while uncovered_minterms:
        best_implicant = None
        best_cover_count = -1

        for row_idx, implicant in enumerate(implicants):
            if implicant not in needed_implicants:
                cover_count = sum(table[row_idx][j] for j in uncovered_minterms)
                if cover_count > best_cover_count:
                    best_cover_count = cover_count
                    best_implicant = implicant

        if best_implicant:
            needed_implicants.append(best_implicant)
            uncovered_minterms = [minterm for minterm in uncovered_minterms if not table[implicants.index(best_implicant)][minterm]]

    return needed_implicants

def implicant_to_formula(implicant, variables):
    return ''.join([(variables[i] if char == '1' else "¬" + variables[i]) for i, char in enumerate(implicant) if char != '-'])

def implicants_to_formula(implicants, variables):
    return ' | '.join([f'({implicant_to_formula(implicant, variables)})' for implicant in implicants])

def handle_inputs(trues, falses, unknowns, mode=0):
    # 0 fills falses
    # 1 fills unknowns
    # 2 fills trues
    trues = sorted(set(trues), key=trues.index)
    falses = sorted(set(falses) - set(trues), key=falses.index)
    unknowns = sorted(set(unknowns) - set(falses) - set(trues), key=unknowns.index)
    max_val = max(trues + falses + unknowns, default=0)
    all_possible_values = set(range(2**(len(bin(max_val)) - 2)))

    if mode == 0:
        falses = list(all_possible_values - set(trues) - set(unknowns))
    elif mode == 1:
        unknowns = list(all_possible_values - set(trues) - set(falses))
    elif mode == 2:
        trues = list(all_possible_values - set(falses) - set(unknowns))
    else:
        raise ValueError("Invalid mode. Mode must be 0, 1, or 2.")

    return trues, falses, unknowns

def print_inputs(trues, falses, unknowns):
    print("\nInputs:\n")
    print(f"Trues:\n{format_string(trues)}\n")
    print(f"Falses:\n{format_string(falses)}\n")
    print(f"Unknowns:\n{format_string(unknowns)}\n")

def format_string(lst):
    return ", ".join(map(str, lst)) if lst else "None"

def main():
##    trues = [0, 4, 5, 16, 17, 24, 29, 38, 52, 56, 57, 58]
##    falses = []
##    unknowns = [0, 8, 9, 31, 43, 61]

    trues = [2, 3, 5, 7, 9, 12, 13, 14, 16, 18, 23, 24, 25, 28, 29, 30, 33, 37, 39, 40, 41, 43, 44, 45, 49, 52, 53, 56, 58, 59, 61]
    falses = []
    unknowns = []

    trues, falses, unknowns = handle_inputs(trues, falses, unknowns, mode=0)
    print_inputs(trues, falses, unknowns)
    num_bits = len(bin(max(trues + falses + unknowns, default=0))[2:])
    variables = [chr(i) for i in range(ord('A'), ord('A') + num_bits)]

    # Compute
    beg = time()
    binary_minterms = nums_to_binaries(trues + unknowns, num_bits)
    initial_boolean_formula = implicants_to_formula(binary_minterms, variables)
    prime_implicants = get_prime_implicants(binary_minterms)
    table = generate_implicant_table(trues, prime_implicants)
    needed_implicants = find_needed_implicants(table, prime_implicants)
    boolean_formula = implicants_to_formula(needed_implicants, variables)
    end = time()

    print(f"Initial Boolean Formula:\n{initial_boolean_formula}\n")
    print("Prime Implicants:")
##    for implicant in prime_implicants:
##        print(implicant)
    print("\n".join(prime_implicants))
    print()
    print("Needed Implicants:")
    print("\n".join(needed_implicants))
    print()
    print(f"Simplified Boolean Formula:\n{boolean_formula}")
    print(f"Elapsed time: {(end - beg)/1e9:,} seconds")

if __name__ == "__main__":
    main()
