from uuid import uuid4
from config import WARDEN_PORT, WARDEN_ADDRESS
import socket, json

class WardenRegister():
    def register():
        BUFFER_SIZE = 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(f"{WARDEN_ADDRESS}:{WARDEN_PORT}")
        message = ''
        s.send(message)
        input(".... waiting for response")
        return uuid4()