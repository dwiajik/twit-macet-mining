import random
import re
import json
import os
import sys
import time
import datetime
tweet = sys.argv[1]
features = {}
for word in open('feature_word_list.txt'):
    word = word.rstrip('\n').rstrip('\r')
    features["{}".format(word)] = tweet.count(word)

print(features)
