from timeit import default_timer as time

# snt = input("give a sentence to count vowels in: ").lower()

with open('monologue.txt', 'r') as file:
    snt = file.read().replace('\n', ' ')

def checkVowel(letter):
    VOWELS = "3"
    return letter in VOWELS

def checkVowel2(s, VOWELS):
    v = 0
    for c in s:
        v += c in VOWELS
    return v

start1 = time()
vowelCount = 0
for char in snt:
    vowelCount += checkVowel(char)
time1 = time() - start1

print("")
print(f"There {'is' if vowelCount == 1 else 'are'} {vowelCount} vowel{'' if vowelCount == 1 else 's'} in that text. \nTook {time1} seconds. (v1)\n")

totalTime = 0
for i in range(10):
    start2 = time()
    vowels = checkVowel2(snt, str(i))
    time2 = time() - start2
    totalTime += time2
    print(f"There {'is' if vowels == 1 else 'are'} {vowels} occurance{'' if vowels == 1 else 's'} of {i} in that text. Took {time2} seconds. (v2)\n")
print(f"Took {totalTime} seconds to process total. ({totalTime/10} seconds on average per search)")
