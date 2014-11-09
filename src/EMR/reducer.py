
#!/usr/bin/env python

import sys

last_polarity = None
running_tweets = ""

for input_line in sys.stdin:
	input_line = input_line.strip()
        #print input_line.split(" ")
	this_polarity, tweet = input_line.split("\t")

	if last_polarity == this_polarity:
		running_tweets +=  "," + tweet
	else:
		if last_polarity:
			print( "%s\t%s" % (last_polarity, running_tweets) )
		running_tweets = tweet
		last_polarity = this_polarity

if last_polarity == this_polarity:
	print( "%s\t%s" % (last_polarity, running_tweets) )

