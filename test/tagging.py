import random
import re
import nltk
import nltk.classify
import json
import os
import sys
import time
import datetime
from nltk.tag import tnt
f = open('tagged_name_list.txt', 'r')
train_data = []
for line in f:
    train_data.append([nltk.tag.str2tuple(t) for t in line.split()])

tnt_pos_tagger = tnt.TnT(unk=)
tnt_pos_tagger.train(train_data)
tweet = sys.argv[1]
tagged_tweets = tnt_pos_tagger.tag(nltk.word_tokenize(tweet))
#print(tagged_tweets)
for tagged_tweet in tagged_tweets:
    print(tagged_tweet[0] + "/" + tagged_tweet[1] + " ", end="")

