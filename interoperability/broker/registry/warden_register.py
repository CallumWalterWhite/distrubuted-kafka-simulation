from uuid import UUID
from config import WARDEN_PORT, WARDEN_ADDRESS, DEFAULT_PORT, BUFFER_SIZE
import socket, json
from core import Message, REGISTER_BROKER, Sender

class WardenRegister():
    def register(port):
        sender: Sender = Sender(WARDEN_ADDRESS, WARDEN_PORT, BUFFER_SIZE)
        response = sender.send(Message(REGISTER_BROKER, {
               "port": port,
                "address": DEFAULT_PORT
            }))
        return UUID(response["id"])