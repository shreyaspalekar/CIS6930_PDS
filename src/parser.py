#!/usr/bin/python

#import cPickle as pickle
#import nltk.classify.util
#from nltk.classify import NaiveBayesClassifier
#from nltk.tokenize import word_tokenize
#import sys
import math
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#sys.stderr.write("Started mapper.\n");
stopwords = []
with open('stopwords') as f:
	stopwords = f.read().splitlines()

filenameAFINN = 'Dictionary/AFINN-111.txt'
afinn = dict(map(lambda (w, s): (w, int(s)), [ws.strip().split('\t') for ws in open(filenameAFINN) ]))
 
# Word splitter pattern
#pattern_split = re.compile(r"\W+")

#def word_feats(words):
#    return dict([(word, True) for word in words])


#def subj(subjLine):
#    subjgen = subjLine.lower()
#    # Replace term1 with your subject term
#    subj1 = "obama"
#    if subjgen.find(subj1) != -1:
#        subject = subj1
#        return subject
#    else:
#        subject = "No match"
#        return subject

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
	# Single sentence example:
#	text = "Finn is stupid and idiotic"
#	word_tokens = text.rstrip().split(" ")
#	filtered_words = [w for w in word_tokens if not w in stopwords]
#	print("%6.2f %s" % (sentiment(filtered_words), filtered_words))
	# No negation and booster words handled in this approach
#	text = "Finn is only a tiny bit stupid and not idiotic"
#	word_tokens = text.rstrip().split(" ")
#	filtered_words = [w for w in word_tokens if not w in stopwords]
#	print("%6.2f %s" % (sentiment(filtered_words), filtered_words))

#    classifier = pickle.load(open("classifier.p", "rb"))
#    for line in sys.stdin:
#        tolk_posset = word_tokenize(line.rstrip())
#        d = word_feats(tolk_posset)
	#print d
#        subjectFull = subj(line)
        #if subjectFull == "No match":
         #   print "LongValueSum:" + " " + subjectFull + ": " + "\t" + "1"
        #else:
         #   print "LongValueSum:" + " " + subjectFull + ": " + classifier.classify(d) + "\t" + "1"
 #       print classifier.classify(d)+ "\t\"" +  line.rstrip() +"\""


if __name__ == "__main__":
    main(sys.argv)
