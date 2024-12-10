start = 100
second = -100

while start != -100 or second != 100:
    print(f"[{start}, {second}],", end=" ")
    if second == 100:
        second = -100
        start -= 20
        continue
    second += 20
