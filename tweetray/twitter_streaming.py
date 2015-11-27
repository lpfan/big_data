import sys
import time

import pika
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import config
import utils


class TweerayListener(StreamListener):

    def __init__(self):
        super(TweerayListener, self).__init__()
        self.recieved_tweets = 0
        self.temp_files = []
        self.current_temp_file = utils.generate_temp_file_path()
        self.total_processed_tweets = 0

    def on_data(self, data):

        with open(self.current_temp_file, 'a') as file:
            file.write(data)

        self.recieved_tweets += 1

        if self.recieved_tweets == config.BUFFERED_TWEETS_COUNT:
            self.temp_files.append(self.current_temp_file)
            self.recieved_tweets = 0

            if len(self.temp_files) == config.BUFFERED_TWEETS_FILES_COUNT:
                rabbit_mq_conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
                rabbit_mq_channel = rabbit_mq_conn.channel()
                rabbit_mq_channel.queue_declare(queue=config.TWEET_QUEUE_NAME)
                for f in self.temp_files:
                    rabbit_mq_channel.basic_publish(exchange='', routing_key='tweets', body=f)
                self.temp_files = []

            self.current_temp_file = utils.generate_temp_file_path()

        self.total_processed_tweets += 1
        print '[x] Total processed tweets {0}'.format(self.total_processed_tweets)

    def on_error(self, status):
        print status
        return False

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        time.sleep(60)
        return


def main():
    listener = TweerayListener()
    auth = OAuthHandler(config.TWITTER_CONSUMER_KEY,
                        config.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_SECRET)
    stream = Stream(auth, listener)

    try:
        stream.filter(track=config.TRACK_WORDS)
    except:
        print 'error!'
        stream.disconnect()

if __name__ == '__main__':
    main()
