#Author: Mike Situ	
#Date: 5/13/13
#File: top_ten.py
#Purpose: computes the ten most frequently occurring hash tags from the data
#Usage: $ python top_ten.py <tweet_file>

import sys
import json
import re

# build_tweets: file -> (dict: string int)
# finds all valid hashtags, and adds them to tag_list. each hashtag 
# occurence is then tallied in a dictionary.
def build_tweets(t_file):
	tag_list = []
	hash_dict = {}
	for line in t_file:
		if 'hashtag' in line:
			temp = json.loads(line)
			#print temp['entities']['hashtags'] # list of dictionary
			for tag in temp['entities']['hashtags']:
				tag_list.append(tag['text'].lower())

	for tag in tag_list:
		if tag in hash_dict:
			hash_dict[tag] += 1
		else:
			hash_dict[tag] = 1.0

	return hash_dict

# print_first_10: (sorted dict: string int) -> stdout
# print the top 10 highest occurring hashtags
def print_first_10(d):
	if len(d) < 10:
		r = range(len(d))
	else:
		r = range(10)
	for i in r:
		print d[i][0], d[i][1]

def main():
	tweet_file = open(sys.argv[1])
	hash_dict = build_tweets(tweet_file)
	sorted_hash_list = sorted(hash_dict.items(), reverse = True, key=lambda x: x[1]) #convert dict to sorted list
	print_first_10(sorted_hash_list)
	#print hash_dict
	#print sorted_hash_list
	#print sorted_hash_dict
	#hash_dict = build_hash_dict(tweet_list)
	#print hash_dict

if __name__ == '__main__':
    main()
