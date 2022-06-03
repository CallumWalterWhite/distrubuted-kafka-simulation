from uuid import uuid4, UUID
from broker import Broker
from topic.topic import Topic
from persistence import Repository
import socket
from config import WARDEN_PORT, WARDEN_ADDRESS, BUFFER_SIZE
from core import Message, GET_CONSUMER_GROUP_OFFSET, SET_CONSUMER_GROUP_OFFSET
import json

class BrokerService():
    __repo: Repository
    __broker: Broker

    def __init__(self, repo: Repository, broker: Broker):
        self.__repo = repo
        self.__broker = broker

    def add_topic(self, name):
        id = uuid4()
        topic: Topic = Topic(id, name) 
        self.__broker.add_topic(topic)
        return self.__get_topic(id)
        
    def get_topic(self, id):
        return self.__get_topic(id)
        
    def get_messages(self, id, consumer_group_name):
        return self.__get_topic_messages(id, consumer_group_name)

    def add_message(self, id, message):
        topic: Topic = self.__broker.get_topic(id)
        topic.add_message(message)
        return {
            'isDone': True
        }

    def add_topic(self, id, name):
        topic: Topic = Topic(id, name)
        self.__broker.add_topic(topic)

    def __get_topic(self, id: UUID):
        topic: Topic = self.__broker.get_topic(id)
        return topic.to_object()
        
    def __get_topic_messages(self, id: UUID, consumer_group_name):
        topic: Topic = self.__broker.get_topic(id)
        offset = self.__get_consumer_group_offset(id, consumer_group_name)
        self.__set_consumer_group_offset(id, consumer_group_name, topic.get_partition_size())
        return {
            'messages': topic.get_messages(offset)
        }

    def __get_consumer_group_offset(self, topic_id, consumer_group_name):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((WARDEN_ADDRESS, WARDEN_PORT))
            message : Message = Message(GET_CONSUMER_GROUP_OFFSET, {
                "topic_id": str(topic_id),
                "broker_id": str(self.__broker.id),
                "consumer_group_name": consumer_group_name,
            })
            json_data = message.toJSON().encode()
            s.sendall(json_data)
            data = s.recv(BUFFER_SIZE)
            json_data = str(data.decode("utf-8"))
            message = json.loads(json_data)
            return int(message['offset'])
        
    def __set_consumer_group_offset(self, topic_id, consumer_group_name, offset):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((WARDEN_ADDRESS, WARDEN_PORT))
            message : Message = Message(SET_CONSUMER_GROUP_OFFSET, {
                "topic_id": str(topic_id),
                "broker_id": str(self.__broker.id),
                "consumer_group_name": consumer_group_name,
                "offset": offset,
            })
            json_data = message.toJSON().encode()
            s.sendall(json_data)
            data = s.recv(BUFFER_SIZE)
            json_data = str(data.decode("utf-8"))
            message = json.loads(json_data)
            return int(message['offset'])