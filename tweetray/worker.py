#!/usr/bin/env python
import codecs
import json
import logging
import multiprocessing
import os
import time

import happybase
import pika

import config


logging.basicConfig(filename=os.path.join(config.LOGS_PATH, 'workers.log'), level=logging.DEBUG)
logger = logging.getLogger(__name__)


def tweet_collector(ch, method, properties, tweet_file):
    try:
        hbase_conn = happybase.Connection('localhost')
        tweets_table = hbase_conn.table('tweets')
        f = codecs.open(tweet_file, 'r', encoding='utf-8')
        tweets = f.readlines()
        f.close()
        for line in tweets:
            tweet = json.loads(line)
            text = tweet.get('text', '').encode('utf-8')
            row_key = tweet.get('id_str', '')
            user = tweet.get('user')
            user_name = ''
            location = ''
            if user is not None:
                user_name = user['name'].encode('utf-8')
                location = user.get('user_location', '').encode('utf-8')
            try:
                tweets_table.put(row_key, {
                    'cf:text': text,
                    'cf:user_name': user_name,
                    'cf:user_location': location,
                    'cf:timestam_ms': tweet.get('timestamp_ms', str(time.time()))
                })
            except Exception as e:
                logger.exception('Error while trying to put tweet {0} into hbase'.format(line))
                continue
            logging.info('Tweet {0} processed successfully'.format(text))
    except Exception as e:
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
    print ' [*] Exiting...'
    worker_pool.terminate()
    worker_pool.join()
