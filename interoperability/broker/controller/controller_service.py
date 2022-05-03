from uuid import uuid4, UUID
from interoperability.broker.broker import Broker
from interoperability.broker.topic.topic import Topic
from interoperability.persistence.repository import Repository
import json


class ControllerService():
    __id: str
    __repo: Repository
    __broker: Broker

    def __init__(self, id, repo: Repository, broker: Broker):
        self.__id = id
        self.__repo = repo
        self.__broker = broker

    def add_topic(self, body):
        data = json.loads(body[1:-1])
        name = data['name']
        id = uuid4()
        topic: Topic = Topic(id, name) 
        self.__broker.add_topic(topic)
        return self.__get_topic(id)
        
    def get_topic(self, id):
        return self.__get_topic(UUID(id))

    def __get_topic(self, id: UUID):
        topic: Topic = self.__broker.get_topic(id)
        return topic.to_object()