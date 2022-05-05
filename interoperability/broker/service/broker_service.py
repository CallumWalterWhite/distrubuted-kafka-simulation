from uuid import uuid4, UUID
from broker import Broker
from topic.topic import Topic
from persistence import Repository

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
        
    def get_messages(self, id):
        return self.__get_topic_messages(id)

    def add_message(self, id, message):
        topic: Topic = self.__broker.get_topic(id)
        topic.add_message(message)
        return self.__get_topic_messages(id)

    def add_topic(self, id, name):
        topic: Topic = Topic(id, name)
        self.__broker.add_topic(topic)

    def __get_topic(self, id: UUID):
        topic: Topic = self.__broker.get_topic(id)
        return topic.to_object()
        
    def __get_topic_messages(self, id: UUID):
        topic: Topic = self.__broker.get_topic(id)
        return {
            'messages': topic.get_messages()
        }