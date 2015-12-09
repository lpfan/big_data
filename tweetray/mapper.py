#!/usr/bin/env python

from pymongo_hadoop import BSONMApper


def mapper(documents):
    for doc in documents:
        try:
            location = doc['user']['location'].strip()
        except KeyError:
            continue
        yield {'tweet_id': doc['id_str'], 'location': location}

BSONMApper(mapper)
