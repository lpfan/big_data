import json
import sys
import time

import happybase
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import config


class TweerayListener(StreamListener):

    def __init__(self, api=None, tweets_table=None):
        super(TweerayListener, self).__init__(api=api)
        self.tweets_table = tweets_table

    def on_data(self, data):
        tweet = json.loads(data)
        self.tweets_table.put(tweet['id'], {
            'cf:text': tweet['text'],
            'cf:user_name': tweet['user']['name'],
            'cf:user_location': tweet['user']['location']
        })

    def on_error(self, status):
        print status
        return False

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        time.sleep(60)
        return


def main():
    track = ['buzzfeed','cnnpolitics', 'hromadsketv', 'espresotv']
    hbase_conn = happybase.Connection('localhost')
    tweets_table = hbase_conn.table('tweets')
    listener = TweerayListener(tweets_table=tweets_table)
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
