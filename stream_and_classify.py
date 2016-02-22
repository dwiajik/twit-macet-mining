import random
import re
import nltk
import nltk.classify
from sklearn.svm import LinearSVC

import json
import os
import sys
import time
import datetime

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener


consumer_key = "u4BIhj4UJRcgJ7MZCoE3ipgrQ"
consumer_secret = "C9jBnBloP2UhA6dT92OORWJ4nNzye3vau6SIMDC0lUPCzhlvLS"
access_token = "19142065-bk8MEZxKEk5WQVrPv5gpopLUuKbmWEZ6GMAVtCtcm"
access_secret = "K9cDadiTNwMinexHZaS63Pym73dneaTnhsYko8fuQiKj8"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

class Classifier:
	def clean_tweet(self, tweet):
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

	def tweet_features(self, tweet):
		features = {}
		tweet = self.clean_tweet(tweet)

		for word in open('feature_word_list.txt'):
			word = word.rstrip('\n').rstrip('\r')
			features["count({})".format(word)] = tweet.count(word)

		return features

	def __init__(self):
		labeled_tweets = ([(line, 'traffic') for line in open('corpus/traffic_tweets_combined.txt')] + [(line, 'non_traffic') for line in open('corpus/random_tweets.txt')])
		random.shuffle(labeled_tweets)
		feature_sets = [(self.tweet_features(tweet), category) for (tweet, category) in labeled_tweets]
		train_set, test_set = feature_sets[:15000], feature_sets[15000:]
		self.naive_bayes_classifier = nltk.NaiveBayesClassifier.train(train_set)
		self.svm_classifier = nltk.classify.SklearnClassifier(LinearSVC()).train(train_set)
		self.decision_tree_classifier = nltk.DecisionTreeClassifier.train(train_set)
		#self.maxent_classifier = nltk.MaxentClassifier.train(train_set)
		#self.conditional_exponential_classifier = nltk.ConditionalExponentialClassifier.train(train_set)
		#self.weka_classifier = nltk.WekaClassifier.train(train_set)
		print('Naive Bayes Classifier accuracy:', str(round(nltk.classify.accuracy(self.naive_bayes_classifier, test_set) * 100, 2)) + '%')
		print('SVM Classifier accuracy:', str(round(nltk.classify.accuracy(self.svm_classifier, test_set) * 100, 2)) + '%')
		print('Decision Tree Classifier accuracy:', str(round(nltk.classify.accuracy(self.decision_tree_classifier, test_set) * 100, 2)) + '%')
		with open(os.path.dirname(__file__) + 'classified_tweets.txt', 'a') as f:
			f.write('Naive Bayes Classifier accuracy: ' + str(round(nltk.classify.accuracy(self.naive_bayes_classifier, test_set) * 100, 2)) + '%\n')
			f.write('SVM Classifier accuracy: ' + str(round(nltk.classify.accuracy(self.svm_classifier, test_set) * 100, 2)) + '%\n')
			f.write('Decision Tree Classifier accuracy: ' + str(round(nltk.classify.accuracy(self.decision_tree_classifier, test_set) * 100, 2)) + '%\n')
		#print('Maxent Classifier accuracy:', str(round(nltk.classify.accuracy(self.maxent_classifier, test_set) * 100, 2)) + '%')
		#print('Conditional Exponential Classifier accuracy:', str(round(nltk.classify.accuracy(self.conditional_exponential_classifier, test_set) * 100, 2)) + '%')
		#print('Weka Classifier accuracy:', str(round(nltk.classify.accuracy(self.weka_classifier, test_set) * 100, 2)) + '%')

	def naive_bayes_classify(self, tweet):
		return self.naive_bayes_classifier.classify(self.tweet_features(tweet))

	def svm_classify(self, tweet):
		return self.svm_classifier.classify(self.tweet_features(tweet))

	def decision_tree_classify(self, tweet):
		return self.decision_tree_classifier.classify(self.tweet_features(tweet))


class TwitterStreamer(StreamListener):
	def __init__(self):
		super(TwitterStreamer, self).__init__()
		self.classifier = Classifier()
		print('\nTweets:')
		with open(os.path.dirname(__file__) + 'classified_tweets.txt', 'a') as f:
			f.write('\nTweets:')

	def on_data(self, data):
		try:			
			tweet = json.loads(data)['text'].replace('\n', ' ')
			#if self.classifier.naive_bayes_classify(tweet) is 'traffic' or \
			#	self.classifier.svm_classify(tweet) is 'traffic' or \
			#	self.classifier.decision_tree_classify(tweet) is 'traffic':
			print('| ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
				'\t| ' + self.classifier.naive_bayes_classify(tweet), 
				'\t| ' + self.classifier.svm_classify(tweet), 
				'\t| ' + self.classifier.decision_tree_classify(tweet),
				'\t| ' + tweet)
			with open(os.path.dirname(__file__) + 'classified_tweets.txt', 'a') as f:
				f.write('\n| ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
				'\t| ' + self.classifier.naive_bayes_classify(tweet) +
				'\t| ' + self.classifier.svm_classify(tweet) +
				'\t| ' + self.classifier.decision_tree_classify(tweet) +
				'\t| ' + tweet)

		except BaseException as e:
			print("Error on_data: %s" % str(e))
		return True

	def on_error(self, status):
		print(status)
		return True


twitter_stream = Stream(auth, TwitterStreamer())
keywords = [line.rstrip('\n') for line in open(os.path.dirname(__file__) + 'name_list.txt')]
twitter_stream.filter(track=keywords, follow=['250022672', '187397386', '1118238337', '4675666764', '128175561', '537556372', '106780531', '62327666', '454564576', '223476605'])
