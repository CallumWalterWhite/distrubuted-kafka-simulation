import json
import socket
from uuid import uuid4
from interoperability.core import Message, ADD_TOPIC
from interoperability.persistence.repository import Repository

class Service():
    __repo: Repository

    def __init__(self, repo: Repository):
        self.__repo = repo

    def add_broker(self, id, address, port):
        self.__repo.add_broker(id, address, port)
        print("broker added...")
        
    def list_brokers(self):
        return self.__repo.list_brokers()

    def delete_all_brokers(self):
        self.__repo.delete_all_brokers()
    
    def add_broker_topic(self, broker, topic_name):
        topic_id = uuid4()
        print(topic_id)
        address = broker[1]
        port = broker[2]
        BUFFER_SIZE=1024
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((address, port))
            message : Message = Message(ADD_TOPIC, {
                "id": str(topic_id),
                "name": topic_name
            })
            json_data = message.toJSON().encode()
            print(json_data)
            s.sendall(json_data)
            data = s.recv(BUFFER_SIZE)
            json_data = str(data.decode("utf-8"))
            message = json.loads(json_data)
            return bool(message["isDone"])

        
        