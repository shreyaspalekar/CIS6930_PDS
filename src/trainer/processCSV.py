import sys,csv,pickle
import nltk

tweets = []
pos_tweets = []
neg_tweets = []
neu_tweets = []
word_features = []

def start(filename):
	if len(filename) != 2:
		print "need only one argument"

	with open(str(filename[1]), 'rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			#print row[0] +" "+row[-1]
			if row[0] == 4:
				pos_tweets.append((row[-1],row[0]))
			if row[0] == 0:
				neg_tweets.append((row[-1],row[0]))
			else :
				neu_tweets.append((row[-1],row[0]))

			for (words, sentiment) in pos_tweets + neg_tweets + neu_tweets:
				words_filtered = [e.lower() for e in words.split() if len(e) >= 3 and "http" not in e]
				tweets.append((words_filtered, sentiment))

#		print tweets
		word_features = get_word_features(get_words_in_tweets(tweets))
#		print word_features
		training_set = nltk.classify.apply_features(extract_features, tweets)
		classifier = nltk.NaiveBayesClassifier.train(training_set)
#		tweet = 'Larry is my friend'
#		print classifier.classify(extract_features(tweet.split()))

		with open("classifier.p", 'wb') as infile:
			pickle.dump(classifier, infile)


def extract_features(tweet):
    document_words = set(tweet)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features



def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

if __name__ == '__main__':
    start(sys.argv)
