def test(item):
    print(f"Checking {item}")
    return item > 0

numbers = [-2, -1, 0, 1, 2, 3]
if any(test(num) for num in numbers):
    print("At least one number is positive")
