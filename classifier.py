import random
import re
import nltk
import nltk.classify
from sklearn.svm import LinearSVC

def clean_tweet(tweet):
	tweet = tweet.lower()

	# remove non alphabetic character
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

def tweet_features(tweet):
	features = {}
	tweet = clean_tweet(tweet)

	for word in open('feature_word_list.txt'):
		word = word.rstrip('\n').rstrip('\r')
		features["count({})".format(word)] = tweet.count(word)

	return features

labeled_tweets = ([(line, 'traffic') for line in open('corpus/traffic_tweets_combined.txt')] + [(line, 'non_traffic') for line in open('corpus/random_tweets.txt')])
random.shuffle(labeled_tweets)
feature_sets = [(tweet_features(tweet), category) for (tweet, category) in labeled_tweets]
train_set, test_set = feature_sets[20000:], feature_sets[:20000]
naive_bayes_classifier = nltk.NaiveBayesClassifier.train(train_set)
svm_classifier = nltk.classify.SklearnClassifier(LinearSVC()).train(train_set)
print('Naive Bayes Classifier accuracy', nltk.classify.accuracy(naive_bayes_classifier, test_set))
print('SVM Classifier accuracy', nltk.classify.accuracy(svm_classifier, test_set))
