data = {}

def get(category):
	return data.get(category, [])

def add(word, category):
	data.setdefault(category, []).append(word)
	print(data)
