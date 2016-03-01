import nltk
import os
import re
import time

def clean_tweet(tweet):
	#tweet = tweet.lower()

	# remove non alphabetic character
	regex = re.compile('\shttp.+\s')
	tweet = regex.sub(' ', tweet)
	regex = re.compile('[^a-zA-Z]')
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

#f = open('tagged_corpus/UI-1M-tagged-edited.txt', 'r')
f = open('tagged_corpus/UI-1M-tagged-edited-simplified.txt', 'r')
#f = open('tagged_corpus/Indonesian_Manually_Tagged_Corpus.txt', 'r')

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
print(training_time)
#print(tnt_pos_tagger.evaluate(test_data), training_time)

f = open('selected_tweets.txt', 'r')
for line in f:
	line = clean_tweet(line)
	print(tnt_pos_tagger.tag(nltk.word_tokenize(line)))
	#grammar = r"""
	#  NP: {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and noun
	#	  {<NNP>+}                # chunk sequences of proper nouns
	#"""
	#cp = nltk.RegexpParser(grammar)

	#print(cp.parse(tnt_pos_tagger.tag(nltk.word_tokenize(line))))
