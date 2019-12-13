from dotmap import DotMap
import json


class KAPIObject(DotMap):
    """ KAPI obects are just dot-addressable dicts with easy serialization
        to/from JSON """

    def json(self):
        return json.dumps(self.toDict(), sort_keys=True)

    def jsonPretty(self):
        return json.dumps(self.toDict(), indent=4, sort_keys=True)

    def dict(self):
        return dict(**self.toDict())

    def debug(self, pformat="dict"):
        return self.pprint(pformat=pformat)

    def debugJSON(self):
        return self.debug("json")
