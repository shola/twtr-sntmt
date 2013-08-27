# Author: Mike Situ
# Date: 5/13/13
# File: frequency.py
# Purpose: outputs <term:string> <frequency:float> for each term in the tweet file
# Usage: $ python frequency.py <tweet_file>
import sys
import json
import re

# build_tweets: file -> (listof listof lower-case strings)
# returns a list of valid tweets
def build_tweets(t_file):
	tweets = []
	for line in t_file:
		if 'text' in line:
			#lowered = json.loads(line)['text'].lower()
			#tweets.append(re.split('[\. \, \? ! @ # \$ % ^ & \* ( ) \+ - ; : < > |]', lowered))
			lowered = json.loads(line)['text'].lower()
			tweets.append(lowered.split())
	return tweets

# print_hist: (listof listof str)
# prints the tallies the number of times each word is used
def print_hist(t_file):
	tweet_list = build_tweets(t_file)
	tweet_dict = {}
	for tweet in tweet_list:
		for item in tweet:
			if item in tweet_dict:
				tweet_dict[item] += 1
			else:
				tweet_dict[item] = 1.0

	for key, val in tweet_dict.items():
		print key, val

def main():
	tweet_file = open(sys.argv[1])
	print_hist(tweet_file)

if __name__ == '__main__':
    main()
