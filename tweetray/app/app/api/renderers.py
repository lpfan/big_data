import ujson
from rest_framework.compat import six
from drf_ujson import renderers
from bson import json_util


class MongodbUJSONRenderer(renderers.UJSONRenderer):

    media_type = 'application/json'
    format = 'json'
    ensure_ascii = True
    charset = None

    def render(self, data, *args, **kwargs):
        if data is None:
            return bytes()
        try:
            ret = ujson.dumps(data, ensure_ascii=self.ensure_ascii)
        except (UnicodeDecodeError, OverflowError):
            ret = json_util.dumps(data)

        # force return value to unicode
        if isinstance(ret, six.text_type):
            return bytes(ret.encode('utf-8'))
        return ret
