from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import config


class StdOutLIstener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':
    listener = StdOutLIstener()
    auth = OAuthHandler(config.TWITTER_CONSUMER_KEY,
                        config.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_SECRET)
    stream = Stream(auth, listener)
    stream.filter(track=['bwm', 'audi'])
