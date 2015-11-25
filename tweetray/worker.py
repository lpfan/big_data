import json
import multiprocessing
import os

import pika

import config


RECIEVED_TWEET_COUNT = 0

def tweet_collector(ch, method, properties, tweet):
    tweet = json.loads(tweet)
    print 'recieved tweet %s' % tweet['id']
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consume():
    rabbit_mq_conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    rabbit_mq_channel = rabbit_mq_conn.channel()
    rabbit_mq_channel.queue_declare(queue=config.TWEET_QUEUE_NAME)
    rabbit_mq_channel.basic_consume(tweet_collector,
                                    queue=config.TWEET_QUEUE_NAME)
    try:
        rabbit_mq_channel.start_consuming()
    except KeyboardInterrupt:
        pass

worker_pool = multiprocessing.Pool(processes=config.WORKER_COUNT)

for i in xrange(0, config.WORKER_COUNT):
    worker_pool.apply_async(consume)

try:
    while True:
        continue
except KeyboardInterrupt:
    print ' [*] Exiting...'
    worker_pool.terminate()
    worker_pool.join()
