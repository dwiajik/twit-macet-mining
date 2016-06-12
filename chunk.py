import nltk
import os
import re
import sys
import time

def clean_tweet(tweet):
	tweet = tweet.lower()

	# remove non alphabetic character
	regex = re.compile('\shttp.+\s')
	tweet = regex.sub(' ', tweet)
	regex = re.compile('@[a-zA-Z0-9_]+')
	tweet = regex.sub(' ', tweet)
	regex = re.compile('RT\s')
	tweet = regex.sub(' ', tweet)
	regex = re.compile('[^a-zA-Z]')
	tweet = regex.sub(' ', tweet)

	regex = re.compile('kondisi')
	tweet = regex.sub(' ', tweet)
	regex = re.compile('lalin')
	tweet = regex.sub(' ', tweet)
	regex = re.compile('lintas')
	tweet = regex.sub(' ', tweet)
	regex = re.compile('arus')
	tweet = regex.sub(' ', tweet)

	# replace abbreviations
	replacement_word_list = [line.rstrip('\n').rstrip('\r') for line in open('replacement_word_list.txt')]

	replacement_words = {}
	for replacement_word in replacement_word_list:
		replacement_words[replacement_word.split(',')[0]] = replacement_word.split(',')[1]

	new_string = []
	for word in tweet.split():
		if replacement_words.get(word, None) is not None:
			word = replacement_words[word]
		new_string.append(word)

	tweet = ' '.join(new_string)
	return tweet

#f = open('pos_tagged_corpus/UI-1M-tagged-edited.txt', 'r')
f = open('pos_tagged_corpus/UI-1M-tagged-edited-simplified.txt', 'r')
#f = open('pos_tagged_corpus/Indonesian_Manually_Tagged_Corpus.txt', 'r')

tagged = []
for line in f:
	tagged.append([nltk.tag.str2tuple(t) for t in line.split()])

print('Analyzed sentences:', len(tagged))

#train_data = tagged[:30000]
#test_data = tagged[30000:]
train_data = tagged

from nltk.tag import tnt
tnt_pos_tagger = tnt.TnT()

start_time = time.time()
tnt_pos_tagger.train(train_data)
training_time = round(time.time() - start_time, 2)
print('Training time:', training_time, 'seconds')
#print(tnt_pos_tagger.evaluate(test_data), training_time)

f = open(sys.argv[1], 'r')
for line in f:
	line = clean_tweet(line)
	#print(tnt_pos_tagger.tag(nltk.word_tokenize(line)))
	grammar = r"""
	  NP: {<NN>(<NN>|<NNP>|<Unk>)+}
	  JJP: {<JJ>+}
	"""
	cp = nltk.RegexpParser(grammar)

	tagged_chunked_line = cp.parse(tnt_pos_tagger.tag(nltk.word_tokenize(line)))

	result = ''
	for subtree in tagged_chunked_line.subtrees():
		if subtree.label() == 'NP': 
			for leave in subtree.leaves():
				result += leave[0] + ' '
			result = result[:-1]
			result += ', '
			
	result = result[:-2]
	result += ' | '

	for subtree in tagged_chunked_line.subtrees():
		if subtree.label() == 'JJP': 
			for leave in subtree.leaves():
				result += leave[0] + ' '
			result = result[:-1]
			result += ', '

	#for leaf in tagged_chunked_line.leaves():
	#	if leaf[1] == 'JJ':
	#		result += leaf[0] + ', '

	result = result[:-2]

	print(result)
		#print(subtree.leaves())
		#if subtree.label() == 'NP': print(subtree.leaves())

	#print(noun_phrase)
	#print(tagged_chunked_line)
