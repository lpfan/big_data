#!/usr/bin/env python
import logging
import multiprocessing
import os

import pika
from pymongo import MongoClient

import config


logging.basicConfig(filename=os.path.join(config.LOGS_PATH, 'workers.log'), level=logging.DEBUG)
logger = logging.getLogger(__name__)


def tweet_collector(ch, method, properties, tweet_tuple):
    client = MongoClient(config.MONGO_HOST, config.MONGO_PORT)
    try:
        db = client[config.TWITTER_DB]
        collection = db[config.RAW_TWEETS_COLLECTION]
        for tweet in tweet_tuple:
            collection.insert(tweet)
    except Exception:
        logger.exception('Exception occured')
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consume():
    print('prepear consuming')
    rabbit_mq_conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    rabbit_mq_channel = rabbit_mq_conn.channel()
    rabbit_mq_channel.queue_declare(queue=config.TWEET_QUEUE_NAME)
    rabbit_mq_channel.basic_consume(tweet_collector,
                                    queue=config.TWEET_QUEUE_NAME)
    print('ready for consuming')
    try:
        rabbit_mq_channel.start_consuming()
    except KeyboardInterrupt:
        pass

with multiprocessing.Pool(processes=config.WORKER_COUNT) as worker_pool:
    worker_pool.apply_async(consume)
    try:
        while True:
            continue
    except KeyboardInterrupt:
        print(' [*] Exiting...')
        worker_pool.terminate()
        worker_pool.join()
