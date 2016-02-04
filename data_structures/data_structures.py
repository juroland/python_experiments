import operator

# Dictionary

word_freqs = {'zero' : 0, 'seven' : 777}

word_freqs['one'] = 14
word_freqs['two'] = 10
word_freqs['three'] = 24

for key in word_freqs:
    print(key)

print('=====')

for key in word_freqs.keys():
    print(key)

print('=====')

for value in word_freqs.values():
    print(value)

print('=====')

for key, value in word_freqs.items():
    print(key, value, sep=' : ')

print('=====')

for element in word_freqs.items():
    print(element[0], element[1], sep=' : ')

print('=====')

sorted_pairs = sorted(word_freqs.items(), key=operator.itemgetter(1), reverse=True)

print(sorted_pairs)

print('=====')