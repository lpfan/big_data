import json

import happybase
import pika


rabbit_mq_conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
rabbit_mq_channel = rabbit_mq_conn.channel()
rabbit_mq_channel.queue_declare(queue='tweets')

hbase_conn = happybase.Connection('localhost')
tweets_table = hbase_conn.table('tweets')

def save_tweet_to_hbase_callback(ch, method, properties, tweet):
    tweet = json.loads(tweet)
    text = tweet.get('text', '')
    row_key = tweet.get('id_str', '')
    user = tweet.get('user')
    user_name = ''
    location = ''
    if user is not None:
        user_name = user['name']
        location = user.get('user_location', '')
    try:
        tweets_table.put(row_key, {
            'cf:text': text,
            'cf:user_name': user_name,
            'cf:user_location': location
        })
        print "[x] tweet %s stored" % row_key
    except Exception:
        pass

rabbit_mq_channel.basic_consume(save_tweet_to_hbase_callback, queue='tweets', no_ack=True)
rabbit_mq_channel.start_consuming()
