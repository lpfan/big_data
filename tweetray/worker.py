import json
import multiprocessing

import happybase
import pika

import config


RECIEVED_TWEET_COUNT = 0

def tweet_collector(ch, method, properties, tweet_file):
    hbase_conn = happybase.Connection('localhost')
    tweets_table = hbase_conn.table('tweets')
    print 'start collector'
    print tweet_file

    # with(tweet_file, 'r') as file:
    #     tweets = file.readlines()

    #for line in tweets:
    #    tweet = json.loads(line)
    #    text = tweet.get('text', '')
    #    row_key = tweet.get('id_str', '')
    #    user = tweet.get('user')
    #    user_name = ''
    #    location = ''
    #    if user is not None:
    #        user_name = user['name']
    #        location = user.get('user_location', '')
    #    try:
    #        tweets_table.put(row_key, {
    #            'cf:text': text,
    #            'cf:user_name': user_name,
    #            'cf:user_location': location,
    #            'cf:timestam_ms': tweet['timestamp_ms']
    #        })
    #        print "[x] tweet %s stored" % row_key
    #    except Exception:
    #        pass

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
