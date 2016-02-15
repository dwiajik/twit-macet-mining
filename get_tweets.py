# sys.argv[1] => twitter screen name

import tweepy
import os
import sys

from tweepy import OAuthHandler

consumer_key = "u4BIhj4UJRcgJ7MZCoE3ipgrQ"
consumer_secret = "C9jBnBloP2UhA6dT92OORWJ4nNzye3vau6SIMDC0lUPCzhlvLS"
access_token = "19142065-bk8MEZxKEk5WQVrPv5gpopLUuKbmWEZ6GMAVtCtcm"
access_secret = "K9cDadiTNwMinexHZaS63Pym73dneaTnhsYko8fuQiKj8"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

for tweet in tweepy.Cursor(api.user_timeline,id=sys.argv[1]).items():
	with open(os.path.dirname(__file__) + sys.argv[1] + '.txt', 'a') as f:
		f.write(tweet.text.replace('\r', ' ').replace('\n', ' ') + "\r\n")
	print(tweet.text.replace('\r', ' ').replace('\n', ' '))
