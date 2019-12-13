from kapi.api_resources.abstract.api_resource import APIResource, APIRequest

import logging

logger = logging.getLogger(__name__)


def parseResult(cls, result):
    # Lists of documents become lists of objects
    if isinstance(result, list):
        return [cls(x) for x in result]

    # else we just obtained a single document to splat into an object
    return cls(result)


class Listable(APIResource):
    @classmethod
    def list(cls, key=None, **kwargs):
        req = APIRequest(key=key)
        url = cls.genURL(**kwargs)
        got = req.get(url)

        return parseResult(cls, got.json())


class Fetchable(APIResource):
    @classmethod
    def fetch(cls, key=None, **kwargs):
        req = APIRequest(key=key)
        url = cls.genURL(**kwargs)
        got = req.get(url)
#        code = got.status_code

        return parseResult(cls, got.json())


class Updateable(APIResource):
    @classmethod
    def upload(cls, key=None, body=None, **kwargs):
        req = APIRequest(key=key)
        url = cls.genURL(**kwargs)
        #        print("sending to url:", url)
        got = req.post(url, data=body)
        return parseResult(cls, got.json())


class Deleteable(APIResource):
    ...


class Createable(APIResource):
    ...
