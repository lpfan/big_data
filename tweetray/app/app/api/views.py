from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response

from bson.objectid import ObjectId
from pymongo import MongoClient

from app.api.renderers import MongodbUJSONRenderer


class TweetViewSet(viewsets.ViewSet):

    renderer_classes = (MongodbUJSONRenderer,)

    def get_raw_tweets_collection(self):
        client = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
        db = client[settings.TWITTER_DB]
        return db[settings.TWITTER_RAW_COLLECTION]

    def list(self, request):
        raw_tweets_coll = self.get_raw_tweets_collection()
        return Response({'total_tweet_count': raw_tweets_coll.count()})

    def retrieve(self, request, pk=None):
        raw_tweets_coll = self.get_raw_tweets_collection()
        return Response(raw_tweets_coll.find_one({'_id': ObjectId(pk)}))


class TweetLocationViewSet(viewsets.ViewSet):
    renderer_classes = (MongodbUJSONRenderer,)

    def get_raw_tweets_collection(self):
        client = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
        db = client[settings.TWITTER_DB]
        return db[settings.TWITTER_RAW_COLLECTION]

    def list(self, request):
        raw_tweets_coll = self.get_raw_tweets_collection()
        tweets_with_user_location = raw_tweets_coll.find(
            {'user.location': {'$ne': None}}
        )
        return Response(tweets_with_user_location)
