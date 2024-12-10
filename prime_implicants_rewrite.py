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
        minterms = list(set(newMinterms))
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
    table = [[RepresentableByImplicant(num, implicant) for num in trues] for implicant in implicants]
    return table

def FindNeededImplicants(table, implicants):
    num_minterms = len(table[0])
    conditionsMet = [False] * num_minterms

    essential_implicants = []
    for i in range(num_minterms):
        covering_implicants = [j for j in range(len(implicants)) if table[j][i]]
        if len(covering_implicants) == 1:
            essential = covering_implicants[0]
            if implicants[essential] not in essential_implicants:
                essential_implicants.append(implicants[essential])
            for k in range(num_minterms):
                if table[essential][k]:
                    conditionsMet[k] = True
    
    uncovered_minterms = [i for i in range(num_minterms) if not conditionsMet[i]]
    implicantsOut = essential_implicants[:]
    
    while uncovered_minterms:
        best_implicant = None
        best_cover = []

        for i, implicant in enumerate(implicants):
            if implicant not in implicantsOut:
                cover = [j for j in uncovered_minterms if table[i][j]]
                if len(cover) > len(best_cover):
                    best_implicant = implicant
                    best_cover = cover
        
        if best_implicant:
            implicantsOut.append(best_implicant)
            for minterm in best_cover:
                uncovered_minterms.remove(minterm)

    return implicantsOut

def ImplicantToFormula(implicant, variables):
    terms = [(variables[i] if char == '1' else variables[i] + "'") for i, char in enumerate(implicant) if char != '-']
    return ''.join(terms)

def ImplicantsToFormula(implicants, variables):
    return ' + '.join([ImplicantToFormula(implicant, variables) for implicant in implicants])

def main():
    trues = [2, 3, 4, 5, 6, 8, 9]
    #falses = [i for i in range(2**len(bin(max(trues))[2:])) if (i not in trues)]
    falses = [0, 1, 7]
    unknowns = [i for i in range(2**len(bin(max(trues))[2:])) if (i not in trues) and (i not in falses)] # if everything else we don't care about
    num_bits = len(bin(max(trues + falses + unknowns))[2:]) # In case "unknowns" has fixed values that are 2^(n+i) bigger than those in "trues"
    variables = [chr(i) for i in range(ord('A'), ord('A') + num_bits)]  # Generate variable names like A, B, C, etc.

    binary_minterms = NumsToBinaries(trues + unknowns, num_bits)
    primeImplicants = GetPrimeImplicants(binary_minterms)

    print("Prime implicants:")
    for i in primeImplicants:
        print(i)
    print()
    
    table = GenerateImplicantTable(trues, primeImplicants)
    neededImplicants = FindNeededImplicants(table, primeImplicants)
    
    print("Needed Implicants:")
    for implicant in neededImplicants:
        print(implicant)
    print()
    
    boolean_formula = ImplicantsToFormula(neededImplicants, variables)
    print("Boolean Formula:")
    print(boolean_formula)

if __name__ == "__main__":
    main()
