import re

def convert_to_pow(expression):
    # Regex pattern to match the base and exponent of ** operator
    pattern = re.compile(r'(\b\w+\([^()]*\)|\([^()]+\)|-\d+|\d+|\b\w+\b)\*\*(\b\w+\([^()]*\)|\([^()]+\)|-\d+|\d+|\b\w+\b)')
    
    while '**' in expression:
        expression = pattern.sub(r'pow(\1, \2)', expression)
    
    return expression

# Test cases
print(convert_to_pow("x**2"))           # "pow(x, 2)"
print(convert_to_pow("3**x"))           # "pow(3, x)"
print(convert_to_pow("x**-2"))          # "pow(x, -2)"
print(convert_to_pow("(x+1)**2"))       # "pow((x+1), 2)"
print(convert_to_pow("sin(x)**2"))      # "pow(sin(x), 2)"
print(convert_to_pow("x**sin(x)"))      # "pow(x, sin(x))"
print(convert_to_pow("sin(x**2)**3"))   # "pow(sin(pow(x, 2)), 3)"
print(convert_to_pow("cos(3)**x"))      # "pow(cos(3), x)"
print(convert_to_pow("3**cos(x)"))      # "pow(3, cos(x))"
print(convert_to_pow("cos(x**3)**2"))   # "pow(cos(pow(x, 3)), 2)"
