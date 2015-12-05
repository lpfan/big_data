from rest_framework import viewsets
from rest_framework.response import Response


class TweetViewSet(viewsets.ViewSet):

    def list(self, request):
        return Response({'total_tweet_count': 0})
