import random
import re
import nltk
import nltk.classify
from sklearn.svm import LinearSVC
from nltk.tag import tnt

import json
import os
import sys
import time
import datetime

import mysql.connector
from mysql.connector import Error

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

os.environ['TZ'] = 'Asia/Jakarta'

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
        labeled_tweets = (
            [(line, 'traffic') for line in open('tweets_corpus/traffic_tweets_combined.txt')] +
            [(line, 'non_traffic') for line in open('tweets_corpus/random_tweets.txt')] +
            [(line, 'non_traffic') for line in open('tweets_corpus/non_traffic_tweets.txt')]
        )
        random.shuffle(labeled_tweets)
        train_set = [(self.tweet_features(tweet), category) for (tweet, category) in labeled_tweets]
        print('Using', len(train_set), 'training data.')

        start_time = time.time()
        self.naive_bayes_classifier = nltk.NaiveBayesClassifier.train(train_set)
        naive_bayes_time = round(time.time() - start_time, 2)
        print('Naive Bayes Classifier training time:', naive_bayes_time, 'seconds')

        start_time = time.time()
        self.svm_classifier = nltk.classify.SklearnClassifier(LinearSVC()).train(train_set)
        svm_time = round(time.time() - start_time, 2)
        print('SVM Classifier training time:', svm_time, 'seconds')

        start_time = time.time()
        self.decision_tree_classifier = nltk.DecisionTreeClassifier.train(train_set)
        decision_tree_time = round(time.time() - start_time, 2)
        print('Decision Tree Classifier training time:', decision_tree_time, 'seconds')

        # self.maxent_classifier = nltk.MaxentClassifier.train(train_set)
        # self.conditional_exponential_classifier = nltk.ConditionalExponentialClassifier.train(train_set)
        # self.weka_classifier = nltk.WekaClassifier.train(train_set)

        # print('Maxent Classifier accuracy:', str(round(nltk.classify.accuracy(self.maxent_classifier, test_set) * 100, 2)) + '%')
        # print('Conditional Exponential Classifier accuracy:', str(round(nltk.classify.accuracy(self.conditional_exponential_classifier, test_set) * 100, 2)) + '%')
        # print('Weka Classifier accuracy:', str(round(nltk.classify.accuracy(self.weka_classifier, test_set) * 100, 2)) + '%')

    def naive_bayes_classify(self, tweet):
        return self.naive_bayes_classifier.classify(self.tweet_features(tweet))

    def svm_classify(self, tweet):
        return self.svm_classifier.classify(self.tweet_features(tweet))

    def decision_tree_classify(self, tweet):
        return self.decision_tree_classifier.classify(self.tweet_features(tweet))


class Location:
    def clean_tweet(self, tweet):
        tweet = tweet.lower()

        # remove non alphabetic character
        regex = re.compile('\shttp.+\s')
        tweet = regex.sub(' ', tweet)
        regex = re.compile('@[a-zA-Z0-9_]+')
        tweet = regex.sub(' ', tweet)
        regex = re.compile('RT\s')
        tweet = regex.sub(' ', tweet)
        regex = re.compile('[^a-zA-Z0-9]')
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

    def __init__(self):
        f = open('tagged_name_list.txt', 'r')

        train_data = []
        for line in f:
            train_data.append([nltk.tag.str2tuple(t) for t in line.split()])

        self.tnt_pos_tagger = tnt.TnT()
        self.tnt_pos_tagger.train(train_data)

        grammar = r"""
          LOC: {(<PRFX><PRFX>*<B-LOC><I-LOC>*)|(<B-LOC><I-LOC>*)}
        """
        self.cp = nltk.RegexpParser(grammar)

    def find_locations(self, tweet):
        tweet = self.clean_tweet(tweet)

        tagged_chunked_tweet = self.cp.parse(self.tnt_pos_tagger.tag(nltk.word_tokenize(tweet)))

        result = ''
        for subtree in tagged_chunked_tweet.subtrees():
            if subtree.label() == 'LOC': 
                for leave in subtree.leaves():
                    result += leave[0] + ' '
                result = result[:-1]
                result += ','

        result = result[:-1]
        return result

class TwitterStreamer(StreamListener):
    def __init__(self):
        super(TwitterStreamer, self).__init__()
        self.classifier = Classifier()
        self.location = Location()
        print('\nTweets:')
        with open(os.path.dirname(__file__) + 'classified_tweets.txt', 'a') as f:
            f.write('\nTweets:')

    def on_data(self, data):
        try:
            tweet = json.loads(data)['text'].replace('\n', ' ')
            # if self.classifier.naive_bayes_classify(tweet) is 'traffic' or \
            # self.classifier.svm_classify(tweet) is 'traffic' or \
            # self.classifier.decision_tree_classify(tweet) is 'traffic':
            if sys.argv[1] == "dev":
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
                with open(os.path.dirname(__file__) + 'classified_tweets.csv', 'a') as f:
                    f.write('"' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                            '","' + self.classifier.naive_bayes_classify(tweet) +
                            '","' + self.classifier.svm_classify(tweet) +
                            '","' + self.classifier.decision_tree_classify(tweet) +
                            '","' + tweet + '"\n')

            ts = datetime.datetime.strftime(datetime.datetime.strptime(json.loads(data)['created_at'], 
                '%a %b %d %H:%M:%S +0000 %Y') + datetime.timedelta(hours=7), '%Y-%m-%d %H:%M:%S')

            con = mysql.connector.connect(host='localhost', database='twitmacet', user='root', password='')
            cur = con.cursor()
            add_tweet = (
            "INSERT INTO tweets(date_time, user_id, raw_tweet, naive_bayes, svm, decision_tree, detected_locations, created_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)")
            tweet_data = (
                ts, 
                json.loads(data)['user']['id_str'],
                tweet, 
                str(self.classifier.naive_bayes_classify(tweet)), 
                str(self.classifier.svm_classify(tweet)),
                str(self.classifier.decision_tree_classify(tweet)), 
                str(self.location.find_locations(tweet)),
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            cur.execute(add_tweet, tweet_data)
            con.commit()

            cur.close()

        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


twitter_stream = Stream(auth, TwitterStreamer())
# keywords = [line.rstrip('\n') for line in open(os.path.dirname(__file__) + 'name_list.txt')]
users = ['250022672', '187397386', '1118238337', '4675666764', '128175561', '537556372', '106780531', '62327666',
         '454564576', '223476605', '201720189']
keywords = ['Yogyakarta', 'Jogjakarta', 'Jogja', 'Yogya', 'Adisutjipto', 'Adi Sutjipto', 'lalinjogja', 'RTMC_Jogja',
            'ATCS_DIY', 'jogjaupdate', 'jogja24jam', 'infojogja', 'yogyakartacity', 'jogjamedia', 'tribunjogja', 'unisifmyk', 
            'UGM', 'UII', 'UNY', 'UMY', 'lalinyk']
twitter_stream.filter(track=keywords, follow=users)
