def GetPrimeImplicants(minterms):
    primeImplicants = []
    merges = [False] * len(minterms)
    numberOfMerges = 0
    mergedMinterm = minterm1 = minterm2 = ""
    for i in range(len(minterms)):
        for c in range(i + 1, len(minterms)):
            minterm1 = minterms[i]
            minterm2 = minterms[c]
            if CheckDashesAlign(minterm1, minterm2) and CheckMintermDifference(minterm1, minterm2):
                mergedMinterm = MergeMinterms(minterm1, minterm2)
                primeImplicants.append(mergedMinterm)
                numberOfMerges += 1
                merges[i], merges[c] = True, True
    
    for j in range(len(minterms)):
        if not merges[j] and minterms[j] not in primeImplicants:
            primeImplicants.append(minterms[j])
    
    if numberOfMerges == 0:
        return primeImplicants
    else:
        return GetPrimeImplicants(primeImplicants)

def MergeMinterms(minterm1, minterm2):
    mergedMinterm = ""
    for i in range(len(minterm1)):
        if minterm1[i] != minterm2[i]:
            mergedMinterm += '-'
        else:
            mergedMinterm += minterm1[i]
    return mergedMinterm

def CheckDashesAlign(minterm1, minterm2):
    for i in range(len(minterm1)):
        if minterm1[i] != '-' and minterm2[i] == '-':
            return False
    return True

def CheckMintermDifference(minterm1, minterm2):
    m1, m2 = BinStringToInt(minterm1), BinStringToInt(minterm2)
    res = m1 ^ m2
    return res != 0 and (res & (res - 1)) == 0

def BinStringToInt(string):
    replaced = string.replace("-", "0")[::-1]
    return sum([int(replaced[i]) * (2**i) for i in range(len(replaced))])

def NumsToBinaries(nums):
    if len(nums) == 0:
        return []
    binaries = []
    for i in nums:
        remainderStack = []
        while i > 0:
            rem = i % 2
            remainderStack.append(rem)
            i = i // 2
        binary = ""
        while len(remainderStack) > 0:
            binary += str(remainderStack.pop())
        binaries.append(binary)
    maxLen = max(len(bin(max(nums))) - 2, max([len(i) for i in binaries]))
    for i in range(len(binaries)):
        while len(binaries[i]) < maxLen:
            binaries[i] = "0" + binaries[i]
    return binaries

def RepresentableByImplicant(num, implicant):
    implicant = list(implicant)
    dashIndices = [i for i, x in enumerate(implicant) if x == "-"][::-1]
    trialImplicant = [i if i != "-" else "0" for i in implicant]
    for i in range(2**len(dashIndices)):
        asInt = BinStringToInt("".join(trialImplicant))
        if asInt == num:
            return True
        for j in range(len(dashIndices)):
            if trialImplicant[dashIndices[j]] == "0":
                for k in range(j):
                    trialImplicant[dashIndices[k]] = "0"
                trialImplicant[dashIndices[j]] = "1"
                break
        else:
            return False
        
    return False

def GenerateImplicantTable(trues, implicants):
    table = []
    for i in implicants:  # As many rows as there are prime implicants
        table.append([])
    for i in range(len(table)):
        for j in range(len(trues)):
            table[i].append(RepresentableByImplicant(trues[j], implicants[i]))
    return table

def FindNeededImplicants(table, implicants):
    implicantsOut = []
    conditionsMet = [False] * len(table[0])

    # Find essential implicants
    essential_implicants = []
    for i in range(len(table[0])):  # for each column
        trueFound = 0
        lastRowTrue = float('inf')
        for j in range(len(table)):  # in each row
            if table[j][i]:
                trueFound += 1
                lastRowTrue = j
        if trueFound == 1:  # Essential prime implicant found
            essential_implicant = table[lastRowTrue]
            if implicants[lastRowTrue] not in essential_implicants:
                essential_implicants.append(implicants[lastRowTrue])
            for k in range(len(conditionsMet)):
                if essential_implicant[k]:
                    conditionsMet[k] = True

    implicantsOut.extend(essential_implicants)

    # Remove the columns (minterms) covered by essential implicants
    uncovered_minterms = []
    for i, condition in enumerate(conditionsMet):
        if not condition:
            uncovered_minterms.append(i)

    # Use a greedy algorithm to cover the remaining minterms
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
    terms = []
    for i in range(len(implicant)):
        if implicant[i] == '1':
            terms.append(variables[i])
        elif implicant[i] == '0':
            terms.append(variables[i] + "'")
    return ''.join(terms)

def ImplicantsToFormula(implicants, variables):
    formula = ' + '.join([ImplicantToFormula(implicant, variables) for implicant in implicants])
    return formula

def main():
    # "trues" and "unknowns" together make up our minterms
    trues = [1, 3, 7, 8, 13, 18, 21]
    unknowns = [9, 14]
    num_bits = max(len(bin(max(trues + unknowns))[2:]), len(bin(max(trues))[2:]))
    variables = [chr(i) for i in range(ord('A'), ord('A') + num_bits)]  # Generate variable names like A, B, C, etc.
    
    binary_minterms = NumsToBinaries(trues+unknowns)
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
