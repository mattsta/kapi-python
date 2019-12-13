import requests
import kapi

from kapi import error


class APIRequest:
    OBJECT_NAME = "undefined"

    def __init__(self, key=None, base=None):
        self.key = key or kapi.key
        self.base = base or kapi.api_base
        self.session = requests.Session()

        self.session.auth = (self.key, "")
        self.current = None  # current reply

    def checkStatus(self):
        code = self.current.status_code
        #        print(self.current.text)

        if code == 200:
            return self.current

        if code == 500:
            raise error.APIServerError(http_status=code, message=self.current.text)

        msg = self.current.json()["detail"]
        if code == 404:
            raise error.APIErrorNotFound(http_status=code, message=msg)

        if code == 403:
            raise error.InvalidRequestError(
                http_status=code, message=msg, param=self.current.text
            )

        raise error.APIError(http_status=code, message=msg)

    def get(self, url):
        self.current = self.session.get(url, timeout=(5, 5))
        return self.checkStatus()

    def post(self, url, data=None, json=None):
        headers = {"Content-Type": "application/json", "Accept": "text/plain"}
        self.current = self.session.post(
            url, json=json, data=data, headers=headers, timeout=(5, 5)
        )
        return self.checkStatus()


# Paths are somewhat like:
# /api/resume/:personality/:resumeName/{edit,acl,visibility}
# /api/avail/:name/{edit,acl,visibility}

# /api/resume/me/name
# /api/resume/me/name/edit
# /api/resume/me/name/acl
# /api/resume/me/name/visibility
# /api/avail/name
# /api/contacts/
# /api/messages/
# /api/profile/
class APIResource(APIRequest):
    @classmethod
    def genURL(cls, *args, **kwargs):
        """ Generate a url by appending '*args' to formatted '**kwargs' """

        # We rely on the fact Python 3.6+ preserves insert order of dict keys.
        # Also we're using a hacky way of not appending 'None' values to the url
        start = "/".join([f"{a}{'/' + b if b else ''}" for a, b in kwargs.items()])
        end = "/".join(args)
        whole = "/".join([x for x in [kapi.api_base, cls.OBJECT_NAME, start, end] if x])
        return whole
