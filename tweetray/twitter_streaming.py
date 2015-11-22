import json
import sys
import time

import pika
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import config

rabbit_mq_conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
rabbit_mq_channel = rabbit_mq_conn.channel()
rabbit_mq_channel.queue_declare(queue='tweets')


class TweerayListener(StreamListener):

    def on_data(self, data):
        rabbit_mq_channel.basic_publish(exchange='', routing_key='tweets', body=data)
        print " [x] Sent tweet %s to queue" % data
        # tweet = json.loads(data)

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
