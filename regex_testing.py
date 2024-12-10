import regex as re

# Test strings
test_strings = [
    "sin(x)**cos(y)",
    "(3)**(5)",
    "(sin(x))**cos(y)",
    "((bob)bobby)**(sunny(boy))"
]

# Define the regex to capture nested expressions on either side of "**"
regex_pattern = r'(-?\w*\((?:[^()]++|(?1))*+\)|-?\b\w+\b|\d+\.\d+|\d+)\*\*(-?\w*\((?:[^()]++|(?1))*+\)|-?\b\w+\b|\d+\.\d*|\d+)'

# Compile the regex pattern with the regex module
regex = re.compile(regex_pattern)

# Apply the regex to each test string and print the matches
for test_string in test_strings:
    matches = regex.findall(test_string)
    print(f"Matches in '{test_string}': {matches}")
