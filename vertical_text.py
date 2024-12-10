def vertical_text(text):
	maxlen = len(max((text := text.split()), key=len))
	text = [i.ljust(maxlen) for i in text]
	return [[text[word][line] for word in range(len(text))] for line in range(maxlen)]

def vtp(text):
    for i in vertical_text(text):
        print(i)

v = vtp("balls in your mouth")
