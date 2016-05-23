import random
import re
import json
import os
import sys
import time
import datetime
tweet = sys.argv[1]
features = {}
for word in tweet.split():
    features["{}".format(word)] = tweet.count(word)

print(features)
