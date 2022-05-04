import json

class Message:
    message_type: str
    body: object

    def __init__(self, message_type, body):
        self.message_type = message_type
        self.body = body

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)