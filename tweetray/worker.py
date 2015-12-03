#!/usr/bin/env python
import codecs
import logging
import multiprocessing
import os

import pika
import ujson
from pymongo import MongoClient

import config


logging.basicConfig(filename=os.path.join(config.LOGS_PATH, 'workers.log'), level=logging.DEBUG)
logger = logging.getLogger(__name__)


def tweet_collector(ch, method, properties, tweet_file):
    try:
        f = codecs.open(tweet_file, 'r', encoding='utf-8')
        client = MongoClient(config.MONGO_HOST, config.MONGO_PORT)
        db = client[config.TWITTER_DB]
        collection = db[config.RAW_TWEETS_COLLECTION]
        tweets = f.readlines()
        for tweet in tweets:
            collection.insert(ujson.loads(tweet))
        f.close()
    except Exception:
        logger.exception('Exception occured')
    os.remove(tweet_file)
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
    print(' [*] Exiting...')
    worker_pool.terminate()
    worker_pool.join()
