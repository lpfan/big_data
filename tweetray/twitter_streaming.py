import json
import sys

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import config


class StdOutLIstener(StreamListener):

    def on_data(self, data):
        print json.loads(data)
        with open('tweets.json', 'a') as file:
            file.write(data)
        return True

    def on_error(self, status):
        print status
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream
        print "Stream restarted"


if __name__ == '__main__':
    listener = StdOutLIstener()
    auth = OAuthHandler(config.TWITTER_CONSUMER_KEY,
                        config.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_SECRET)
    while True:
        try:
            stream = Stream(auth, listener)
            stream.filter(track=['buzzfeed'])
        except:
            continue
