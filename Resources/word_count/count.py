import operator

f = open('book.txt','r')

data = f.read()

data = data.split()

word_count = {}

for word in data:
  if not word in word_count:
    word_count[word] = 0
  word_count[word] += 1
  
sorted_x = sorted(word_count.items(), key=operator.itemgetter(1))

print(sorted_x)
