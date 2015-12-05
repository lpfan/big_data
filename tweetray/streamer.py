#!/usr/bin/env python
import logging
import os
import sys
import time
import ujson

import pika
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import config


logging.basicConfig(filename=os.path.join(config.LOGS_PATH, 'streamer.log'), level=logging.ERROR)
logger = logging.getLogger(__name__)


class TweerayListener(StreamListener):

    def __init__(self):
        super(TweerayListener, self).__init__()
        self.recieved_tweets = ()
        self.total_processed_tweets = 0

    def on_data(self, data):

        tweet = ujson.loads(data)
        self.recieved_tweets += (tweet,)

        if len(self.recieved_tweets) == config.BUFFERED_TWEETS_COUNT:
            rabbit_mq_conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            rabbit_mq_channel = rabbit_mq_conn.channel()
            rabbit_mq_channel.queue_declare(queue=config.TWEET_QUEUE_NAME)
            rabbit_mq_channel.basic_publish(exchange='', routing_key='tweets', body=self.recieved_tweets)
            self.recieved_tweets = ()

        self.total_processed_tweets += 1
        print ('[x] Total processed tweets {0}'.format(self.total_processed_tweets))

    def on_error(self, status):
        print(status)
        return False

    def on_timeout(self):
        print('Timeout...', file=sys.stderr)
        time.sleep(60)
        return


def main():
    listener = TweerayListener()
    try:
        auth = OAuthHandler(config.TWITTER_CONSUMER_KEY,
                            config.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_SECRET)
        stream = Stream(auth, listener)
        stream.filter(track=config.TRACK_WORDS)
    except KeyboardInterrupt:
        stream.disconnect()
        print('[x] Exiting ...')
    except:
        print('error!')
        logger.exception('Stream error occured')

if __name__ == '__main__':
    main()
