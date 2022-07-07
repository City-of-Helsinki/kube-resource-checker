import json

class Session:
    def __init__(self, session, host):
        self.session = session
        self.host = host


    def runQuery(self, postdata):
        response = self.session.post(self.host, data=postdata)
        parsed = json.loads(response.content)
        return parsed