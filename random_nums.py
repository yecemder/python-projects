import random

max_nums = 64

num_count = random.randint(1, max_nums)  # Random number between 1 and 1024

random_numbers = random.sample(range(max_nums), num_count)

print(sorted(random_numbers))

