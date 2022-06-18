import json
## Message class
#  @author  Callum White
#  @version 1.0
#  @date    01/06/2022
#  @bug     No known bugs.
#  
#  @details This class is used to create a message object.
class Message:
    message_type: str
    body: object

    ## __init__ method.
    #  @param self The object pointer.
    #  @param message_type The message type.
    #  @param body The body of the message.
    def __init__(self, message_type, body):
        self.message_type = message_type
        self.body = body
    ## toJSON method.
    #  @param self The object pointer.
    #  @return The message as a JSON string.
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)