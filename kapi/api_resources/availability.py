from kapi.api_resources.abstract.obj import KAPIObject
from kapi.api_resources.abstract.ability import Listable, Fetchable, Updateable


class Availability(KAPIObject, Listable, Fetchable, Updateable):
    OBJECT_NAME = "avail"

    @classmethod
    def list(cls, *, key=None):
        return super().list(key=key)

    @classmethod
    def fetch(cls, *, key=None, avail):
        return super().fetch(key=key, **{avail: None})

    @classmethod
    def upload(cls, *, key=None, avail, src):
        return super().upload(key=key, body=src, **{avail: None})
