import random
import re
import nltk
import nltk.classify
from nltk.metrics import scores
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
import collections
import json
import os
import sys
import time
import datetime
tweet = sys.argv[1]
regex = re.compile('RT\s')
tweet = regex.sub(' ', tweet)
tweet = tweet.lower()
regex = re.compile('https?(:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})?')
tweet = regex.sub(' ', tweet)
regex = re.compile('@[a-zA-Z0-9_]+')
tweet = regex.sub(' ', tweet)
regex = re.compile('[^a-zA-Z0-9]')
tweet = regex.sub(' ', tweet)
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
print(tweet)
