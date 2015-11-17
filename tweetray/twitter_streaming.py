import sys
import time

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import config


class TweerayListener(StreamListener):

    def on_data(self, data):
        print data

    def on_error(self, status):
        print status
        return False

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        time.sleep(60)
        return


def main():
    track = ['buzzfeed']
    listener = TweerayListener()
    auth = OAuthHandler(config.TWITTER_CONSUMER_KEY,
                        config.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_SECRET)
    stream = Stream(auth, listener)

    try:
        stream.filter(track=track)
    except:
        print 'error!'
        stream.disconnect()

if __name__ == '__main__':
    main()
