#!/usr/bin/python

import sys,nltk,re,math

filenameAFINN = 'dictionary/AFINN-111.txt'
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


def parse_line(line):
	#for line in sys.stdin:
	nouns = []
	verbs =[]
	adjectives =[]
	adverbs = []
	rest = []
		
	tokens = nltk.word_tokenize(line)
	tags = nltk.pos_tag(tokens)
	for (word,tag)  in tags:
		if re.match("NN*", tag):
			nouns.append(word)
		elif re.match("JJ*", tag):
			adjectives.append(word)
		elif re.match("RB*", tag):
			adverbs.append(word)
		elif re.match("VB*", tag):
			verbs.append(word)
		else:
			rest.append(word)
					
	#print "------------------------------------------------------------------------------------"
	#print "nouns " + str(nouns)
	#print "verbs " + str(verbs)
	#print "adjectives " + str(adjectives)
	#print "adverbs " + str(adverbs)
	#print "rest " + str(rest)
	#print("%6.2f" % (sentiment(adjectives+adverbs)))
	#print "------------------------------------------------------------------------------------"

	return (noun,verbs,adjectives,adverbs,rest,sentiment)

#		print tags
#		ne  =  nltk.ne_chunk(tags, binary=True)
#		print ne
#		for (word_tag, entity) in ne.pos():
		#	print word_tag
		#	print entity
#			if entity == "NE":
#				print word_tag[0]
			#	for (word,tag) in word_tag:
			#		print word

if __name__ == "__main__":
    parse_line(sys.argv)
