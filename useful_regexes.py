# Interesting/useful regex expressions

# Grabs all expressions inside tags
"/(<(?:(?(R)[^<>]++|[^<>]*+)|(?R))*>)/gm"

# Current expression for capturing groups for "pow()" in solve_for_x
"""
(-?\([^()]+\)|-?\b\w+\b|\d+\.+\d+|\d+|-?\b\w+\((?:[^()]+)*\))
\*\*
(-?\b\w+\((?:[^()]+|(?1))*\)|-?\([^()]+\)|-?\d+\.+\d*|-?\b\w+\b)
"""

# Best version for capturing pow() groups
"""
(-?\w*\((?:[^()]++|(?1))*+\)|-?\b\w+\b|\d+\.\d+|\d+)
\*\*
(-?\w*\((?:[^()]++|(?1))*+\)|-?\b\w+\b|\d+\.\d*|\d+)
"""

# BV, ignores preceding negatives unless in parentheses
"""
(\w*\((?:[^()]++|(?1))*+\)|\b\w+\b|\d+\.\d+|\d+)
\*\*
(-?\w*\((?:[^()]++|(?1))*+\)|-?\b\w+\b|\d+\.\d*|\d+)
"""
