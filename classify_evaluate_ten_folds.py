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

def f_measure(precision, recall):
    return 2*((precision * recall) / (precision + recall))

traffic_tweets = [(line, 'traffic') for line in open('tweets_corpus/traffic_tweets_combined.txt')]
non_traffic_tweets = [(line, 'non_traffic') for line in open('tweets_corpus/random_tweets.txt')] + \
    [(line, 'non_traffic') for line in open('tweets_corpus/non_traffic_tweets.txt')]
random.shuffle(traffic_tweets)
random.shuffle(non_traffic_tweets)

if sys.argv[1] == "balance":
    traffic_tweets = traffic_tweets[:min([len(traffic_tweets), len(non_traffic_tweets)])]
    non_traffic_tweets = non_traffic_tweets[:min([len(traffic_tweets), len(non_traffic_tweets)])]

labeled_tweets = (traffic_tweets + non_traffic_tweets)
random.shuffle(labeled_tweets)

naive_bayes_times = []
naive_bayes_true_positives = []
naive_bayes_true_negatives = []
naive_bayes_false_positives = []
naive_bayes_false_negatives = []
naive_bayes_accuracies = []
naive_bayes_precisions = []
naive_bayes_recalls = []
naive_bayes_f_measures = []

svm_times = []
svm_true_positives = []
svm_true_negatives = []
svm_false_positives = []
svm_false_negatives = []
svm_accuracies = []
svm_precisions = []
svm_recalls = []
svm_f_measures = []

decision_tree_times = []
decision_tree_true_positives = []
decision_tree_true_negatives = []
decision_tree_false_positives = []
decision_tree_false_negatives = []
decision_tree_accuracies = []
decision_tree_precisions = []
decision_tree_recalls = []
decision_tree_f_measures = []

print('Start analysis with total:', len(labeled_tweets), 'data')
print('Traffic tweets:', len(traffic_tweets),'data')
print('Non traffic tweets:', len(non_traffic_tweets),'data')

fold = 10

for i in range(fold):
    train_set = [(tweet_features(tweet), category) for (tweet, category) in labeled_tweets[0:i*int(len(labeled_tweets)/fold)]] + \
        [(tweet_features(tweet), category) for (tweet, category) in labeled_tweets[(i+1)*int(len(labeled_tweets)/fold):len(labeled_tweets)]]
    test_set = [(tweet_features(tweet), category) for (tweet, category) in labeled_tweets[i*int(len(labeled_tweets)/fold):(i+1)*int(len(labeled_tweets)/fold)]]

    print('\nIteration', (i+1))
    print('Training data:', len(train_set), 'data')
    print('Test data:', len(test_set), 'data')

    # Naive Bayes
    start_time = time.time()
    #naive_bayes_classifier = nltk.NaiveBayesClassifier.train(train_set)
    naive_bayes_classifier = nltk.classify.SklearnClassifier(BernoulliNB()).train(train_set)
    naive_bayes_time = round(time.time() - start_time, 2)
    naive_bayes_accuracy = nltk.classify.accuracy(naive_bayes_classifier, test_set)
     
    naive_bayes_true_positive = 0
    naive_bayes_true_negative = 0
    naive_bayes_false_positive = 0
    naive_bayes_false_negative = 0
    for i, (feature, label) in enumerate(test_set):
        observed = naive_bayes_classifier.classify(feature)
        if label == 'traffic' and observed == 'traffic':
            naive_bayes_true_positive += 1
        if label == 'non_traffic' and observed == 'non_traffic':
            naive_bayes_true_negative += 1
        if label == 'traffic' and observed == 'non_traffic':
            naive_bayes_false_positive += 1
        if label == 'non_traffic' and observed == 'traffic':
            naive_bayes_false_negative += 1

    naive_bayes_precision = naive_bayes_true_positive / (naive_bayes_true_positive + naive_bayes_false_positive)
    naive_bayes_recall = naive_bayes_true_positive / (naive_bayes_true_positive + naive_bayes_false_negative)
    naive_bayes_f_measure = f_measure(naive_bayes_precision, naive_bayes_recall)

    naive_bayes_times.append(naive_bayes_time)
    naive_bayes_true_positives.append(naive_bayes_true_positive)
    naive_bayes_true_negatives.append(naive_bayes_true_negative)
    naive_bayes_false_positives.append(naive_bayes_false_positive)
    naive_bayes_false_negatives.append(naive_bayes_false_negative)
    naive_bayes_accuracies.append(naive_bayes_accuracy)
    naive_bayes_precisions.append(naive_bayes_precision)
    naive_bayes_recalls.append(naive_bayes_recall)
    naive_bayes_f_measures.append(naive_bayes_f_measure)

    print('Naive Bayes Classifier:')
    print('\t', 'Training time:', naive_bayes_time)    
    print('\t', 'True positive:', naive_bayes_true_positive)
    print('\t', 'True negative:', naive_bayes_true_negative)
    print('\t', 'False positive:', naive_bayes_false_positive)
    print('\t', 'False negative:', naive_bayes_false_negative)
    print('\t', 'Accuracy:', naive_bayes_accuracy)
    print('\t', 'Precision:', naive_bayes_precision)
    print('\t', 'Recall:', naive_bayes_recall)
    print('\t', 'F-Measure:', naive_bayes_f_measure)

    # SVM
    start_time = time.time()
    svm_classifier = nltk.classify.SklearnClassifier(LinearSVC()).train(train_set)
    svm_time = round(time.time() - start_time, 2)
    svm_accuracy = nltk.classify.accuracy(svm_classifier, test_set)
     
    svm_true_positive = 0
    svm_true_negative = 0
    svm_false_positive = 0
    svm_false_negative = 0
    for i, (feature, label) in enumerate(test_set):
        observed = svm_classifier.classify(feature)
        if label == 'traffic' and observed == 'traffic':
            svm_true_positive += 1
        if label == 'non_traffic' and observed == 'non_traffic':
            svm_true_negative += 1
        if label == 'traffic' and observed == 'non_traffic':
            svm_false_positive += 1
        if label == 'non_traffic' and observed == 'traffic':
            svm_false_negative += 1

    svm_precision = svm_true_positive / (svm_true_positive + svm_false_positive)
    svm_recall = svm_true_positive / (svm_true_positive + svm_false_negative)
    svm_f_measure = f_measure(svm_precision, svm_recall)

    svm_times.append(svm_time)
    svm_true_positives.append(svm_true_positive)
    svm_true_negatives.append(svm_true_negative)
    svm_false_positives.append(svm_false_positive)
    svm_false_negatives.append(svm_false_negative)
    svm_accuracies.append(svm_accuracy)
    svm_precisions.append(svm_precision)
    svm_recalls.append(svm_recall)
    svm_f_measures.append(svm_f_measure)

    print('SVM Classifier:')
    print('\t', 'Training time:', svm_time)    
    print('\t', 'True positive:', svm_true_positive)
    print('\t', 'True negative:', svm_true_negative)
    print('\t', 'False positive:', svm_false_positive)
    print('\t', 'False negative:', svm_false_negative)
    print('\t', 'Accuracy:', svm_accuracy)
    print('\t', 'Precision:', svm_precision)
    print('\t', 'Recall:', svm_recall)
    print('\t', 'F-Measure:', svm_f_measure)

    # Decision Tree
    start_time = time.time()
    decision_tree_classifier = nltk.classify.SklearnClassifier(DecisionTreeClassifier()).train(train_set)
    #decision_tree_classifier = nltk.DecisionTreeClassifier.train(train_set)
    decision_tree_time = round(time.time() - start_time, 2)
    decision_tree_accuracy = nltk.classify.accuracy(decision_tree_classifier, test_set)
     
    decision_tree_true_positive = 0
    decision_tree_true_negative = 0
    decision_tree_false_positive = 0
    decision_tree_false_negative = 0
    for i, (feature, label) in enumerate(test_set):
        observed = decision_tree_classifier.classify(feature)
        if label == 'traffic' and observed == 'traffic':
            decision_tree_true_positive += 1
        if label == 'non_traffic' and observed == 'non_traffic':
            decision_tree_true_negative += 1
        if label == 'traffic' and observed == 'non_traffic':
            decision_tree_false_positive += 1
        if label == 'non_traffic' and observed == 'traffic':
            decision_tree_false_negative += 1

    decision_tree_precision = decision_tree_true_positive / (decision_tree_true_positive + decision_tree_false_positive)
    decision_tree_recall = decision_tree_true_positive / (decision_tree_true_positive + decision_tree_false_negative)
    decision_tree_f_measure = f_measure(decision_tree_precision, decision_tree_recall)

    decision_tree_times.append(decision_tree_time)
    decision_tree_true_positives.append(decision_tree_true_positive)
    decision_tree_true_negatives.append(decision_tree_true_negative)
    decision_tree_false_positives.append(decision_tree_false_positive)
    decision_tree_false_negatives.append(decision_tree_false_negative)
    decision_tree_accuracies.append(decision_tree_accuracy)
    decision_tree_precisions.append(decision_tree_precision)
    decision_tree_recalls.append(decision_tree_recall)
    decision_tree_f_measures.append(decision_tree_f_measure)

    print('Decision Tree Classifier:')
    print('\t', 'Training time:', decision_tree_time)
    print('\t', 'True positive:', decision_tree_true_positive)
    print('\t', 'True negative:', decision_tree_true_negative)
    print('\t', 'False positive:', decision_tree_false_positive)
    print('\t', 'False negative:', decision_tree_false_negative)
    print('\t', 'Accuracy:', decision_tree_accuracy)
    print('\t', 'Precision:', decision_tree_precision)
    print('\t', 'Recall:', decision_tree_recall)
    print('\t', 'F-Measure:', decision_tree_f_measure)

print('\nNaive Bayes Classifier:')
print('\tAverage training time:', sum(naive_bayes_times) / len(naive_bayes_times))
print('\tAverage true positive:', sum(naive_bayes_true_positives) / len(naive_bayes_true_positives))
print('\tAverage true negative:', sum(naive_bayes_true_negatives) / len(naive_bayes_true_negatives))
print('\tAverage false positives:', sum(naive_bayes_false_positives) / len(naive_bayes_false_positives))
print('\tAverage false negatives:', sum(naive_bayes_false_negatives) / len(naive_bayes_false_negatives))
print('\tAverage accuracy:', sum(naive_bayes_accuracies) / len(naive_bayes_accuracies))
print('\tAverage precision:', sum(naive_bayes_precisions) / len(naive_bayes_precisions))
print('\tAverage recall:', sum(naive_bayes_recalls) / len(naive_bayes_recalls))
print('\tAverage F-Measure:', sum(naive_bayes_f_measures) / len(naive_bayes_f_measures))

print('\nSVM Classifier:')
print('\tAverage training time:', sum(svm_times) / len(svm_times))
print('\tAverage true positive:', sum(svm_true_positives) / len(svm_true_positives))
print('\tAverage true negative:', sum(svm_true_negatives) / len(svm_true_negatives))
print('\tAverage false positives:', sum(svm_false_positives) / len(svm_false_positives))
print('\tAverage false negatives:', sum(svm_false_negatives) / len(svm_false_negatives))
print('\tAverage accuracy:', sum(svm_accuracies) / len(svm_accuracies))
print('\tAverage precision:', sum(svm_precisions) / len(svm_precisions))
print('\tAverage recall:', sum(svm_recalls) / len(svm_recalls))
print('\tAverage F-Measure:', sum(svm_f_measures) / len(svm_f_measures))

print('\nDecision Tree Classifier:')
print('\tAverage training time:', sum(decision_tree_times) / len(decision_tree_times))
print('\tAverage true positive:', sum(decision_tree_true_positives) / len(decision_tree_true_positives))
print('\tAverage true negative:', sum(decision_tree_true_negatives) / len(decision_tree_true_negatives))
print('\tAverage false positives:', sum(decision_tree_false_positives) / len(decision_tree_false_positives))
print('\tAverage false negatives:', sum(decision_tree_false_negatives) / len(decision_tree_false_negatives))
print('\tAverage accuracy:', sum(decision_tree_accuracies) / len(decision_tree_accuracies))
print('\tAverage precision:', sum(decision_tree_precisions) / len(decision_tree_precisions))
print('\tAverage recall:', sum(decision_tree_recalls) / len(decision_tree_recalls))
print('\tAverage F-Measure:', sum(decision_tree_f_measures) / len(decision_tree_f_measures))
