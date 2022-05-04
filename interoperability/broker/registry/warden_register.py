from uuid import UUID
from config import WARDEN_PORT, WARDEN_ADDRESS
import socket, json
from core import Message

class WardenRegister():
    def register(port):
        BUFFER_SIZE=1024
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((WARDEN_ADDRESS, WARDEN_PORT))
            message : Message = Message('register_broker', {
                "port": port,
                "address": "127.0.0.1"
            })
            s.sendall(message.toJSON().encode())
            data = s.recv(BUFFER_SIZE)
            json_data = str(data.decode("utf-8"))
            message = json.loads(json_data)
            return UUID(message["id"])