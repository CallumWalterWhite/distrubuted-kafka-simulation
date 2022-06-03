from uuid import UUID
from config import WARDEN_PORT, WARDEN_ADDRESS, DEFAULT_PORT, BUFFER_SIZE
import socket, json
from core import Message, REGISTER_BROKER

class WardenRegister():
    def register(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((WARDEN_ADDRESS, WARDEN_PORT))
            message : Message = Message(REGISTER_BROKER, {
                "port": port,
                "address": DEFAULT_PORT
            })
            s.sendall(message.toJSON().encode())
            data = s.recv(BUFFER_SIZE)
            json_data = str(data.decode("utf-8"))
            message = json.loads(json_data)
            return UUID(message["id"])