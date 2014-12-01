

class FakeSession(object):

    url = None
    headers = None
    data = None
    json = None

    def __init__(self):
        self.headers = {}

    def post(self, url, data=None, json=None, **kwargs):
        self.url = url
        self.data = data
        self.json = json
        return True
