#!/usr/bin/python

import math
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

stopwords = []
with open('stopwords') as f:
	stopwords = f.read().splitlines()

filenameAFINN = 'Dictionary/AFINN-111.txt'
afinn = dict(map(lambda (w, s): (w, int(s)), [ws.strip().split('\t') for ws in open(filenameAFINN) ]))
 
# Word splitter pattern
#pattern_split = re.compile(r"\W+")

def sentiment(words):
	"""
	Returns a float for sentiment strength based on the input text.
	Positive values are positive valence, negative value are negative valence.
	"""
	sentiments = map(lambda word: afinn.get(word, 0), words)
	if sentiments:
		# How should you weight the individual word sentiments?
		# You could do N, sqrt(N) or 1 for example. Here I use sqrt(N)
		sentiment = float(sum(sentiments))/math.sqrt(len(sentiments))
	else:
		sentiment = 0
	return sentiment


def main(argv):
	for line in sys.stdin:
		word_tokens = line.rstrip().split()
		filtered_words = [w for w in word_tokens if not w in stopwords]
		print("%6.2f %s" % (sentiment(filtered_words), line.rstrip()))

if __name__ == "__main__":
    main(sys.argv)
