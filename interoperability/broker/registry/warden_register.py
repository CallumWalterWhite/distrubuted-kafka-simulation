from uuid import UUID
from config import WARDEN_PORT, WARDEN_ADDRESS, DEFAULT_PORT, BUFFER_SIZE
from core import Message, REGISTER_BROKER, Sender

## WardenRegister class.
#  @author  Callum White
#  @version 1.0
#  @date    01/06/2022
#  @bug     No known bugs.
#  
#  @details This class register the broker to warden if broker was started isolated.
class WardenRegister():
    def register(port):
        sender: Sender = Sender(WARDEN_ADDRESS, WARDEN_PORT, BUFFER_SIZE)
        response = sender.send(Message(REGISTER_BROKER, {
               "port": port,
                "address": DEFAULT_PORT
            }))
        return UUID(response["id"])