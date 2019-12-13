from kapi.api_resources.abstract.obj import KAPIObject
from kapi.api_resources.abstract.ability import Listable, Fetchable, Updateable


class Resume(KAPIObject, Listable, Fetchable, Updateable):
    OBJECT_NAME = "resume"

    @classmethod
    def list(cls, *, key=None):
        return super().list(key=key)

    @classmethod
    def fetch(cls, *, key=None, personality, resume):
        return super().fetch(key=key, **{personality: resume})

    @classmethod
    def upload(cls, *, key=None, personality, resume, src):
        return super().upload(key=key, body=src, **{personality: resume})
