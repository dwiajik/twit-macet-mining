# sys.argv[1] => tweets count

import json
import os
import sys
import time

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

consumer_key = "u4BIhj4UJRcgJ7MZCoE3ipgrQ"
consumer_secret = "C9jBnBloP2UhA6dT92OORWJ4nNzye3vau6SIMDC0lUPCzhlvLS"
access_token = "19142065-bk8MEZxKEk5WQVrPv5gpopLUuKbmWEZ6GMAVtCtcm"
access_secret = "K9cDadiTNwMinexHZaS63Pym73dneaTnhsYko8fuQiKj8"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

class TwitterStreamer(StreamListener):
	def __init__(self, api=None):
		super(TwitterStreamer, self).__init__()
		self.tweet_count = 0

	def on_data(self, data):
		try:
			self.tweet_count += 1
			
			tweet = json.loads(data)['text'].replace('\n', ' ')
			print(tweet)
			with open(os.path.dirname(__file__) + 'random_tweets.txt', 'a') as f:
				f.write(tweet + '\n')

			if self.tweet_count == int(sys.argv[1]):
				return False

		except BaseException as e:
			print("Error on_data: %s" % str(e))
		return True

	def on_error(self, status):
		print(status)
		return True


twitter_stream = Stream(auth, TwitterStreamer())
twitter_stream.filter(track=['aku', 'mending', 'gak', 'nggak', 'ngga', 'oke', 'tapi', 'tidak'])

