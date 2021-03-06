#!/usr/bin/python

import cPickle as pickle
import sys,nltk,re,math
from nltk.corpus import conll2000
from nltk.tag.stanford import NERTagger

filenameAFINN = 'dictionary/AFINN-111.txt'
afinn = dict(map(lambda (w, s): (w, int(s)), [ws.strip().split('\t') for ws in open(filenameAFINN) ]))
classifier = pickle.load(open("classifier/classifier.p", "rb"))
word_features = pickle.load(open("classifier/word_features.p", "rb"))
st = NERTagger('/usr/share/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz','/usr/share/stanford-ner/stanford-ner.jar') 
#print word_features
#test_sents = conll2000.chunked_sents('test.txt',chunk_types=['NP'])
#train_sents = conll2000.chunked_sents('train.txt',chunk_types=['NP'])
#chunker = nltk.data.load("chunkers/maxent_ne_chunker/english_ace_multiclass.pickle")
#chunker = nltk.data.load("chunkers/maxent_ne_chunker/english_ace_binary.pickle")
# Word splitter pattern
#pattern_split = re.compile(r"\W+")
#class UnigramChunker(nltk.ChunkParserI):
#    def __init__(self, train_sents):
#        train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)]
#                      for sent in train_sents]
#        self.tagger = nltk.UnigramTagger(train_data)
#
#    def parse(self, sentence):
#        pos_tags = [pos for (word,pos) in sentence]
#        tagged_pos_tags = self.tagger.tag(pos_tags)
#        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
#        conlltags = [(word, pos, chunktag) for ((word,pos),chunktag) in zip(sentence, chunktags)]
#
#        return nltk.chunk.conlltags2tree(conlltags)

#chunker = UnigramChunker(train_sents)
def extract_features(tweet):
    global word_features
#    print tweet
    document_words = set(tweet)
#    print document_words
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


def sentiment(words):
        """
        Returns a float for sentiment strength based on the input text.
        Positive values are positive valence, negative value are negative valence.
        """
        sentiments = map(lambda word: afinn.get(word, 0), words)
#	print sentiments
        if sentiments:
                # How should you weight the individual word sentiments?
                # You could do N, sqrt(N) or 1 for example. Here I use sqrt(N)
                sentiment = float(sum(sentiments))/math.sqrt(len(sentiments))
        else:
                sentiment = 0
        return sentiment

def word_feats(words):
    return dict([(word, True) for word in words])

def c_sentiment(words):
	return classifier.classify(words)

def parse_line(line):
	#for line in sys.stdin:
	nouns = []
	verbs =[]
	adjectives =[]
	adverbs = []
	rest = []
	entities =[]
		
	tokens = nltk.word_tokenize(line)
	tags = nltk.pos_tag(tokens)

	t = nltk.ne_chunk(tags, binary=True)
	for (word_tag,entity) in t.pos():
		if str(entity) == "NE":
			entities.append(word_tag[0])
#			print word_tag
#	tree = chunker.parse(tags)
#	for s in t.subtrees(lambda t: t.height() == 2):
#		print(s)


#	t = st.tag(line[1].split())
#	print t
#	for (word_tag,entity) in t:
#		if str(entity) != "O":
#			entities.append(word_tag)
	print entities

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
#	print("%6.2f" % (sentiment(adjectives+adverbs)))
	#print "------------------------------------------------------------------------------------"
#	print str(adjectives+adverbs+verbs)
#	print sentiment(extract_features(adjectives+adverbs+verbs))
#	print c_sentiment(extract_features(line[1]))

	return (entities,nouns,verbs,adjectives,adverbs,rest,sentiment(adjectives+adverbs+verbs))

	print entities

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
#	print("%6.2f" % (sentiment(adjectives+adverbs)))
	#print "------------------------------------------------------------------------------------"

	return (entities,nouns,verbs,adjectives,adverbs,rest,c_sentiment(word_feats(adjectives+adverbs+verbs)))

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
