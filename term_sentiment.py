#Author: Mike Situ	
#Date: 5/13/13
#File: term_sentiment.py
#Purpose: computes sentiment for terms not included in the sentiment file. Output is <term:string sentiment:float>
#Usage: $ python term_sentiment.py <sentiment_file> <tweet_file>

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

# get_tweet_sent_unmatched_lists: (listof listof str) (dict: string int) ----->
#		(tuple: (listof listof str) (dict: str int) (listof str)
# gives each tweet a corresponding sentiment score, based on the given sentiment dict. 
# if a word is not in the dict, it is saved to an unmatched-word list. The original 
# tweet list, corresponding sentiment list, and unmatched word list are returned as a 
# tuple.
def get_tweet_sent_unmatched_lists(t_list, s_dict):
	sent_list = []
	unmatched_words = []
	for tweet in t_list:
		sent_count = 0
		for word in tweet:
			if word in s_dict:
				sent_count += s_dict[word]
			else:
				unmatched_words.append(word)
		sent_list.append(sent_count)
	return {'tweet_list' : t_list, 'sent_list' : sent_list, 'unmatched_words' : unmatched_words}

# add_sent_word: (listof listof str), (listof num), str -> Stdout
# calculates the sentiment value of an unmatched word, and prints it out.
# Formula: (sum of sentiment scores with the unmatched word)/(num of tweets)
def add_sent_word(t_list, s_list, unmatch):
	avg = 0.0
	for i in range(len(t_list)):
		if unmatch in t_list[i]:
			avg += s_list[i]
	avg /= len(t_list)
	print unmatch, avg

# give_sent_to_unmatched: (tuple: (listof listof str) (dict: str int) (listof str) -> stdout
# calculates the sentiment score for each unmatched word in the twitter stream
def give_sent_to_unmatched(tweet_sent_list):
	tlist = tweet_sent_list['tweet_list']
	slist = tweet_sent_list['sent_list']
	ulist = tweet_sent_list['unmatched_words']
	for u in ulist:
		add_sent_word(tlist, slist, u)
	
def main():
	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])
	scores = build_dict(sent_file) 
	tweet_list = build_tweets_list(tweet_file)
	tweet_sent_list = get_tweet_sent_unmatched_lists(tweet_list, scores)
	give_sent_to_unmatched(tweet_sent_list)

if __name__ == '__main__':
    main()
