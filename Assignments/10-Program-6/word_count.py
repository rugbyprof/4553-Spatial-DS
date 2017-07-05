import operator

f = open('book.txt','r')

book = f.read().split()

word_count = {}

for word in book:
  
    if not word in word_count:
      word_count[word] = 0
    word_count[word] += 1
    

sorted_book = sorted(word_count.items(), key=operator.itemgetter(1))

print(sorted_book)
