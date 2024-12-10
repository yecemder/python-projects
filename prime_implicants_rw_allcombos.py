from timeit import default_timer as time

def GetPrimeImplicants(minterms):
    primeImplicants = []
    while minterms:
        newMinterms = []
        merges = set()
        for i in range(len(minterms)):
            for j in range(i + 1, len(minterms)):
                minterm1 = minterms[i]
                minterm2 = minterms[j]
                if CheckMintermDifference(minterm1, minterm2):
                    mergedMinterm = MergeMinterms(minterm1, minterm2)
                    newMinterms.append(mergedMinterm)
                    merges.add(i)
                    merges.add(j)
        primeImplicants.extend([minterms[k] for k in range(len(minterms)) if k not in merges])
        minterms = newMinterms
    return list(set(primeImplicants))

def MergeMinterms(minterm1, minterm2):
    return ''.join('-' if a != b else a for a, b in zip(minterm1, minterm2))

def CheckMintermDifference(minterm1, minterm2):
    return sum(a != b for a, b in zip(minterm1, minterm2)) == 1

def NumsToBinaries(nums, num_bits):
    return [bin(num)[2:].zfill(num_bits) for num in nums]

def RepresentableByImplicant(num, implicant):
    binary = bin(num)[2:].zfill(len(implicant))
    return all(implicant[i] == '-' or implicant[i] == binary[i] for i in range(len(implicant)))

def GenerateImplicantTable(trues, implicants):
    return [[RepresentableByImplicant(num, implicant) for num in trues] for implicant in implicants]

def FindNeededImplicants(table, implicants):
    implicantsOut = []
    conditionsMet = [False] * len(table[0])
    essential_implicants = []

    # Find essential implicants
    for col in range(len(table[0])):  # for each column
        true_count = sum(row[col] for row in table)
        if true_count == 1:  # Essential prime implicant found
            for row_idx, row in enumerate(table):
                if row[col]:
                    if implicants[row_idx] not in essential_implicants:
                        essential_implicants.append(implicants[row_idx])
                    for k in range(len(conditionsMet)):
                        if row[k]:
                            conditionsMet[k] = True
                    break

    implicantsOut.extend(essential_implicants)

    # Identify uncovered minterms
    uncovered_minterms = [i for i, covered in enumerate(conditionsMet) if not covered]

    # Use a greedy algorithm to cover the remaining minterms
    while uncovered_minterms:
        best_implicant = None
        best_cover_count = -1

        for row_idx, implicant in enumerate(implicants):
            if implicant not in implicantsOut:
                cover_count = sum(table[row_idx][j] for j in uncovered_minterms)
                if cover_count > best_cover_count:
                    best_cover_count = cover_count
                    best_implicant = implicant

        if best_implicant:
            implicantsOut.append(best_implicant)
            uncovered_minterms = [minterm for minterm in uncovered_minterms if not table[implicants.index(best_implicant)][minterm]]

    return implicantsOut


def ImplicantToFormula(implicant, variables):
    # ¬
    terms = [(variables[i] if char == '1' else "!" + variables[i]) for i, char in enumerate(implicant) if char != '-']
    return ''.join(terms)

def ImplicantsToFormula(implicants, variables):
    return '(' + ') | ('.join([ImplicantToFormula(implicant, variables) for implicant in implicants]) + ')'

def HandleInputs(trues, falses, unknowns, *, MODE=0):
    """Takes in inputs, and returns a tuple as (trues, unknowns).

    Mode 0 (default): Missing values are FALSES. Use if you have trues and unknowns.
    Mode 1: Missing values are UNKNOWNS. Use if you have trues and falses, and don't care about the rest.
    Mode 2: Missing values are TRUES. Use if you have falses and unknowns.
    """
    trues, unknowns = sorted(trues), sorted(unknowns)
    match MODE:
        case 0:
            return (trues, [i for i in range(2**len(bin(max(trues))[2:])) if (i not in trues) and (i not in unknowns)], unknowns)
        case 1:
            return (trues, falses, [i for i in range(2**len(bin(max(trues))[2:])) if (i not in trues) and (i not in falses)])
        case 2:
            return ([i for i in range(2**len(bin(max(trues))[2:])) if (i not in unknowns) and (i not in falses)], falses, unknowns)

        case _:
            print("Mode set incorrectly")
            return (trues, unknowns)

def PrintInputs(trues, falses, unknowns):
    truesPrint, falsesPrint, unknownsPrint = FormatString(trues), FormatString(falses), FormatString(unknowns)
    print("\nInputs:\n")
    print(f"Trues:\n{truesPrint}\n")
    print(f"Falses:\n{falsesPrint}\n")
    print(f"Unknowns:\n{unknownsPrint}\n")

def FormatString(listToFormat):
    return ", ".join([str(i) for i in listToFormat]) if len(listToFormat) > 0 else "None"

def main():
    trues = [0, 4, 5, 16, 17, 24, 29, 38, 52, 56, 57, 58]
    falses = []
    unknowns = [8, 9, 31, 43, 61]

    trues, falses, unknowns = HandleInputs(trues, falses, unknowns, MODE=0)
    PrintInputs(trues, falses, unknowns)

    num_bits = len(bin(max(trues + falses + unknowns))[2:]) # In case "unknowns" has fixed values that are 2^(n+i) bigger than those in "trues"
    variables = [chr(i) for i in range(ord('A'), ord('A') + num_bits)]  # Generate variable names like A, B, C, etc.
    beg = time()
    binary_minterms = NumsToBinaries(trues + unknowns, num_bits)
    initial_boolean_formula = ImplicantsToFormula(binary_minterms, variables)
    primeImplicants = GetPrimeImplicants(binary_minterms)
    table = GenerateImplicantTable(trues, primeImplicants)
    neededImplicants = FindNeededImplicants(table, primeImplicants)
    boolean_formula = ImplicantsToFormula(neededImplicants, variables)
    end = time()
    duration = (end-beg)
    print(f"Initial Boolean Formula:")
    print(initial_boolean_formula)
    print()
    
    print("Prime implicants:")
    for i in primeImplicants:
        print(i)
    print()
        
    print("Needed Implicants:")
    for implicant in neededImplicants:
        print(implicant)
    print()    
    
    print("Simplified Boolean Formula:")
    print(boolean_formula)
    
    print("Elapsed time: " + str(duration) + " seconds")

if __name__ == "__main__":
    main()
