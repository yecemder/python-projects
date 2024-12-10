def is_combination_sufficient(combination, imps):
    combined = imps.copy()
    for lst in combination:
        combined = [x or y for x, y in zip(combined, lst)]
    return all(combined)

def find_minimal_combination(imps, table):
    from itertools import combinations

    n = len(table)
    
    # Try combinations of increasing size
    for r in range(1, n + 1):
        for combo in combinations(table, r):
            if is_combination_sufficient(combo, imps):
                return combo
                
    return []

# Example usage:
imps = [False, True, False, False, True]
table = [
    [True, False, False, False, False],
    [False, False, True, False, False],
    [False, False, False, True, False],
    [False, False, False, False, False],
    [False, True, False, False, False]
]

minimal_combination = find_minimal_combination(imps, table)
print("Minimal combination that covers all True values:")
for lst in minimal_combination:
    print(lst)
