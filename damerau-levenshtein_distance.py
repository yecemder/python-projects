def dl_distance(a, b):
    # Define the alphabet size (assumed to be ASCII)
    ALPHABET_SIZE = 256

    # Initialize the array da with the alphabet size
    da = [0] * ALPHABET_SIZE

    # Initialize the maximum distance
    maxdist = len(a) + len(b)

    # Create a 2D array d with dimensions (len(a) + 2) x (len(b) + 2)
    d = [[0] * (len(b) + 2) for _ in range(len(a) + 2)]

    # Initialize the starting points of the array d
    d[0][0] = maxdist
    for i in range(1, len(a) + 2):
        d[i][0] = maxdist
        d[i][1] = i - 1
    for j in range(1, len(b) + 2):
        d[0][j] = maxdist
        d[1][j] = j - 1

    # Compute the Damerau-Levenshtein distance
    for i in range(1, len(a) + 1):
        db = 0
        for j in range(1, len(b) + 1):
            k = da[ord(b[j - 1])]
            l = db
            if a[i - 1] == b[j - 1]:
                cost = 0
                db = j
            else:
                cost = 1
            d[i + 1][j + 1] = min(d[i][j] + cost,  # substitution
                                  d[i + 1][j] + 1,  # insertion
                                  d[i][j + 1] + 1,  # deletion
                                  d[k][l] + (i - k) + 1 + (j - l))  # transposition
        da[ord(a[i - 1])] = i

    return d[len(a) + 1][len(b) + 1]

# Example usage:
a = "penis"
b = "penis"
print(dl_distance(a, b))
