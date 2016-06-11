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

tnt_pos_tagger = tnt.TnT()
tnt_pos_tagger.train(train_data)
grammar = r"""
  LOC: {(<PRFX>*<B-LOC><I-LOC>*)}
"""
cp = nltk.RegexpParser(grammar)
tweet = sys.argv[1]
tagged_chunked_tweet = cp.parse(tnt_pos_tagger.tag(nltk.word_tokenize(tweet)))
print(tagged_chunked_tweet)
result = ''
for subtree in tagged_chunked_tweet.subtrees():
    if subtree.label() == 'LOC': 
        for leave in subtree.leaves():
            result += leave[0] + ' '
        result = result[:-1]
        result += ','

result = result[:-1]
print(result)
