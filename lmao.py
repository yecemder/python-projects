import itertools



# Define the variables

variables = ['A', 'B', 'C', 'D', 'E', 'F']



# Define the formula components as Python lambda functions for evaluation

# Original formula: (!A!B!CD!E) | (!AB!C!D!E) | (A!B!CDE!F) | (AB!CD!E!F) |

#                   (ABC!D!F) | (!A!D!E!F) | (!ABCDF) | (ABC!EF)

formula = lambda A, B, C, D, E, F: (

    (not A and not B and not C and D and not E) or

    (not A and B and not C and not D and not E) or

    (A and not B and not C and D and E and not F) or

    (A and B and not C and D and not E and not F) or

    (A and B and C and not D and not F) or

    (not A and not D and not E and not F) or

    (not A and B and C and D and F) or

    (A and B and C and not E and F)

)



# Generate the truth table

truth_table = []

for vals in itertools.product([False, True], repeat=len(variables)):

    row = dict(zip(variables, vals))

    row['Result'] = formula(**row)

    truth_table.append(row)


import numpy as np



# Function to calculate the K-map index for 6 variables

def kmap_index(A, B, C, D, E, F):

    # Gray code order for columns and rows to ensure adjacency

    gray_code = [0, 1, 3, 2]

    row = gray_code[A * 2 + B]

    col = gray_code[C * 2 + D] * 4 + gray_code[E * 2 + F]

    return row, col



# Initialize a 4x16 K-map for 6 variables (AB as rows, CDEF as columns)

kmap = np.zeros((4, 16), dtype=int)



# Populate the K-map with the truth table results

for entry in truth_table:

    A, B, C, D, E, F, result = entry['A'], entry['B'], entry['C'], entry['D'], entry['E'], entry['F'], entry['Result']

    row, col = kmap_index(int(A), int(B), int(C), int(D), int(E), int(F))

    kmap[row, col] = int(result)


def find_groups(kmap):

    """

    Identify groups of 1s in the K-map to simplify the Boolean expression.

    Groups must be power-of-2 sizes and can wrap around edges.

    """

    rows, cols = kmap.shape

    groups = []



    # Helper function to check if a group is valid

    def is_valid_group(r, c, size_r, size_c):

        for i in range(size_r):

            for j in range(size_c):

                if kmap[(r + i) % rows, (c + j) % cols] == 0:

                    return False

        return True



    # Check for all possible groups

    for size_r in [1, 2, 4]:  # Group sizes for rows (1, 2, 4)

        for size_c in [1, 2, 4, 8, 16]:  # Group sizes for columns (1, 2, 4, 8, 16)

            for r in range(rows):

                for c in range(cols):

                    if is_valid_group(r, c, size_r, size_c):

                        groups.append((r, c, size_r, size_c))



    # Remove subgroups (smaller groups contained within larger groups)

    final_groups = []

    for group in groups:

        r, c, size_r, size_c = group

        if all(

            not (r2 <= r < r2 + size_r2 and c2 <= c < c2 + size_c2)

            or (r2 == r and c2 == c and size_r2 == size_r and size_c2 == size_c)

            for r2, c2, size_r2, size_c2 in final_groups

        ):

            final_groups.append(group)



    return final_groups



# Find the groups in the K-map

groups = find_groups(kmap)


def group_to_term(group, variables):
    """
    Translate a group in the K-map into a Boolean term.
    Each group is represented as (row, col, height, width).
    """
    r, c, size_r, size_c = group
    rows, cols = 4, 16  # K-map dimensions

    # Gray code inverse mapping for rows and columns
    gray_code_inv = [0, 1, 3, 2]
    fixed_vars = {}

    # Row variables (A, B)
    for i, var in enumerate(variables[:2]):  # A, B
        row_range = [gray_code_inv[(r + x) % rows] // (2**i) % 2 for x in range(size_r)]
        if all(val == row_range[0] for val in row_range):  # If all values in range are the same
            fixed_vars[var] = row_range[0]

    # Column variables (C, D, E, F)
    for i, var in enumerate(variables[2:]):  # C, D, E, F
        col_range = [
            gray_code_inv[((c + x) // 4) % 4] // (2**i) % 2 if x < cols else 0 for x in range(size_c)
        ]
        if all(val == col_range[0] for val in col_range):  # If all values in range are the same
            fixed_vars[var] = col_range[0]

    # Generate the product term for this group
    term = ''.join(f"!{var}" if not fixed_vars[var] else var for var in fixed_vars)
    return term


# Map the groups into Boolean terms
variables = ['A', 'B', 'C', 'D', 'E', 'F']
terms = [group_to_term(group, variables) for group in groups]

# Simplified expression (sum of terms)
simplified_expression = ' | '.join(terms)
print(simplified_expression)
