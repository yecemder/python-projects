from random import shuffle
f = open("dict.txt", "r")
contents = f.read()
contents = contents.lower().split()

allow_prev_words = True
prev_words = []
while True:
    syllable = input("syllable:\n").strip().lower()
    found_matches = [x for x in contents if syllable in x]
    shuffle(found_matches)
    print(f"\n{len(found_matches)} matches found.\n")
    for i in sorted(found_matches[:15] + found_matches[-10:], key=len):
        print(i)
    print()
    
