# sys.argv[1] => file name

import operator
import sys
import re

# declare dictionary
words = {}

# read file as string
with open(sys.argv[1], 'r') as corpus:
	string = corpus.read()

tweet_count = string.count('\n')

word_count = 0
tweet_list = string.split('\n')
for tweet in tweet_list:
	tweet_words = tweet.split(' ')
	word_count += len(tweet_words)

string = string.replace('\n', ' ')

string = string.lower()

# remove links
string = [word for word in string.split() if 'http' not in word]
string = ' '.join(string)

# remove some unused words
removed_string = ['&amp', '&gt', 'rt']
for s in removed_string:
	string = string.replace(s, ' ')

# remove non alphabetic character
regex = re.compile('[^a-zA-Z]')
string = regex.sub(' ', string)

# replace abbreviations
replacement_word_list = [line.rstrip('\n').rstrip('\r') for line in open('replacement_word_list.txt')]

replacement_words = {}
for replacement_word in replacement_word_list:
	replacement_words[replacement_word.split(',')[0]] = replacement_word.split(',')[1]

new_string = []
for word in string.split():
	if replacement_words.get(word, None) is not None:
		word = replacement_words[word]
	new_string.append(word)

string = ' '.join(new_string)

# remove words that starts with &, numbers, remove mention, remove one-letter word
for word in string.split():
	if word[0] is not '&' and \
		word[0] is not '@' and \
		not word[0].isnumeric() and \
		len(word) is not 1:
		if words.get(word, None) is None:
			words[word] = 1
		else:
			words[word] += 1


words = sorted(words.items(), key=operator.itemgetter(1), reverse=True)
print('Analyzed', tweet_count, 'tweets.')
print('Average words per tweet:', word_count/tweet_count, '\n')
print('Top 50 words:')

for word in words[:50]:
	print('(', word[1], ')', word[0])
