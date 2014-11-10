# based on http://badhessian.org/2012/10/collecting-real-time-twitter-data-with-the-streaming-api/
# with modifications by http://github.com/marciw
# requires Tweepy https://github.com/tweepy/tweepy

from tweepy import StreamListener
import nltk
import json, time, sys,random

sys.path.insert(0, '/home/shreyas/Projects/PDS/src')
import sentiment_parser
sentiment_parser.filenameAFINN = '../dictionary/AFINN-111.txt'

class TWaiter(StreamListener):

    # see Tweepy for more info

    def __init__(self, api = None, label = 'default_collection'):
        self.api = api or API()
        self.counter = 0
        self.label = label
        self.output  = open(label + '.' + time.strftime('%b%d-%H%M') + '.txt', 'w')
        self.deleted  = open('deleted_tweets.txt', 'a')

    def on_data(self, data):
        # The presence of 'in_reply_to_status' indicates a "normal" tweet.
        # The presence of 'delete' indicates a tweet that was deleted after posting.
        if  'in_reply_to_status' in data:
            self.on_status(data)
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False


    def on_status(self, status):
	proc_tweet ={}
        # Get only the text of the tweet and its ID.
#	if "obama" in str(json.dumps(json.loads(status)['text'])).lower():
       	text = str(json.dumps(json.loads(status)['text']))
       	id_str = str(json.dumps(json.loads(status)['id_str']))
	loc = str(json.dumps(json.loads(status)['user']['location']))
	co = str(json.dumps(json.loads(status)['coordinates']))
	proc_tweet['text'] = text
	proc_tweet['id_str'] = id_str
	proc_tweet['loc'] = loc
	proc_tweet['co'] = co
	(entities,nouns,verbs,adjectives,adverbs,rest,sentiment) = sentiment_parser.parse_line(text)
#	proc_text = nltk.tag.pos_tag(text.split())
#	self.output.write(json.dumps(proc_tweet))


	#print "entities: " + str(nouns+verbs+adjectives+adverbs) + " sentiment: " + str(sentiment)
	print "entities: " + str(entities) +" action: "+str(verbs)+" description: "+str(adverbs+adjectives)+" sentiment: " + str(sentiment)


#	print(json.dumps(proc_tweet))
#	self.output.write(id_str[1:-1]+", "+text[1:-1]+", "+str(random.randint(0, 10)) +", "+loc +", "+co+"\n")
      	#self.output.write(id[1:-1]+"\t"+str(proc_text[1:-1]) +"\n")
       	self.counter += 1

        # For tutorial purposes, only 500 tweets are collected.
        # Increase this number to get bigger data!
        if self.counter >= 1000:
            self.output.close()
            print "Finished collecting tweets."
            sys.exit()
        return

    def on_delete(self, status_id, user_id):
        self.deleted.write(str(status_id) + "\n")
        return

    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False
