# Author: Mike Situ
# Date: 5/13/13
# File: tweet_sentiment.py
# Purpose: returns a list of the integer sentiments of each tweet in a twitter-stream 
# Usage:  $ python tweet_sentiment.py <sentiment_file> <tweet_file>
import sys
import json
import re

def lines(fp):
	print str(len(fp.readlines()))

# build_dict: file -> dict
# given a file formatted as (str '\t' num), build_dict returns a dict object
# of the sentiment scores
def build_dict(afinnfile):
	scores = {} # initialize empty dictionary
	for line in afinnfile:
		term, score = line.split("\t") # split by tabs
		scores[term] = int(score) # convert score to int
	return scores

# build_tweets: file -> (listof listof lower-case strings)
# returns the contents of the 'text' field in a listof-listof-strings, 
# whenever there is a 'text' field in the file input.
def build_tweets_list(t_file):
	tweets = []
	for line in t_file:
		if 'text' in line:
			lowered = json.loads(line)['text'].lower()
			tweets.append(re.split('[\. \, \? ! @ # \$ % ^ & \* ( ) \+ - ; : < > |]', lowered))
	return tweets

# gen_sent_list: (listof listof str) (dict: string int) -> (listof num)
# generates the sentiment scores for each word that is in the sentiment dict.
def gen_sent_list(t_list, s_dict):
	sent_list = []
	for line in t_list:
		sent_count = 0
		for word in line:
			if word in s_dict:
				sent_count += s_dict[word]
		sent_list.append(sent_count)
	return sent_list

# print_list: (listof X) -> stdout
def print_list(X):
	for item in X:
		print item

def main():
	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])
	scores = build_dict(sent_file) 
	tweet_list = build_tweets_list(tweet_file)
	sent_list = gen_sent_list(tweet_list, scores)
	print_list(sent_list)

if __name__ == '__main__':
    main()
