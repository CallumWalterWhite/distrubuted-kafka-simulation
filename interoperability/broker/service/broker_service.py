from uuid import uuid4, UUID
from broker import Broker
from topic.topic import Topic
from topic.partition.partition import Partition
import socket
from config import WARDEN_PORT, WARDEN_ADDRESS, BUFFER_SIZE
from core import *
import json

class BrokerService():
    __broker: Broker

    def __init__(self, broker: Broker):
        self.__broker = broker

    def add_topic(self, name):
        id = uuid4()
        topic: Topic = Topic(id, name) 
        self.__broker.add_topic(topic)
        return self.__get_topic(id)
        
    def get_topic(self, id):
        return self.__get_topic(id)
        
    def get_messages(self, id, consumer_group_id):
        return self.__get_topic_messages(id, consumer_group_id)

    def add_message(self, topic_id, partition_id, message):
        topic: Topic = self.__broker.get_topic(topic_id)
        partition: Partition = topic.get_partition(partition_id)
        partition.add_message(message)
        return True

    def add_topic(self, id, name):
        topic: Topic = self.__broker.get_topic(id)
        if topic is None:
            topic: Topic = Topic(id, name)
            self.__broker.add_topic(topic)
        return True
    
    def add_partition(self, topic_id, id, leader):
        topic: Topic = self.__broker.get_topic(topic_id)
        if topic is None:
            raise("Topic not found")
        topic.add_partition(id, leader)
        return True

    def __get_topic(self, id: UUID):
        topic: Topic = self.__broker.get_topic(id)
        return topic.to_object()
        
    def __get_topic_messages(self, id: UUID, consumer_group_id):
        aggregate_messages = []
        topic: Topic = self.__broker.get_topic(id)
        for partition in topic.partitions:
            offset = self.__get_consumer_group_offsets(partition.id, consumer_group_id)
            partition_size = partition.size()
            messages = partition.get_messages(offset, partition_size)
            aggregate_messages = aggregate_messages + messages
            self.__set_consumer_group_offset(partition.id, consumer_group_id, partition_size)
        return aggregate_messages

    def __get_consumer_group_offsets(self, partition_id, consumer_group_id):
        sender: Sender = Sender(WARDEN_ADDRESS, WARDEN_PORT)
        response = sender.send(Message(GET_CONSUMER_GROUP_OFFSET, {
                "partition_id": str(partition_id),
                "broker_id": str(self.__broker.id),
                "consumer_group_id": str(consumer_group_id),
            }))
        return int(response['offset'])
        
    def __set_consumer_group_offset(self, partition_id, consumer_group_id, offset):
        sender: Sender = Sender(WARDEN_ADDRESS, WARDEN_PORT)
        return sender.send(Message(SET_CONSUMER_GROUP_OFFSET, {
                "partition_id": str(partition_id),
                "broker_id": str(self.__broker.id),
                "consumer_group_id": str(consumer_group_id),
                "offset": offset,
            }))