from uuid import uuid4, UUID
from broker import Broker
from topic.topic import Topic
from topic.partition.partition import Partition
from config import WARDEN_PORT, WARDEN_ADDRESS
from core import *

## BrokerService class.
#  @author  Callum White
#  @version 1.0
#  @date    01/06/2022
#  @bug     No known bugs.
#  
#  @details This class is used to create a broker service.
class BrokerService():
    # broker variable
    __broker: Broker

    ## __init__ method.
    # @param broker Broker
    def __init__(self, broker: Broker):
        self.__broker = broker
        
    ## get_topic method.
    # @param id UUID
    # @return Topic
    def get_topic(self, id):
        return self.__get_topic(id)
        
    ## get_messages method.
    # @param id UUID
    # @return List[Message]
    def get_messages(self, id, consumer_group_id):
        return self.__get_topic_messages(id, consumer_group_id)
    
    ## get_all_messages method.
    # @param id UUID
    # @return List[Message]
    def get_all_messages(self, id):
        return self.__get_all_topic_messages(id)

    ## add_message method.
    # @param topic_id UUID
    # @param partition_id UUID
    # @param message Message
    # @return Boolean
    def add_message(self, topic_id, partition_id, message):
        topic: Topic = self.__broker.get_topic(topic_id)
        partition: Partition = topic.get_partition(partition_id)
        partition.add_message(message)
        return True

    ## add_topic method.
    # @param id UUID
    # @param name String
    # @return Topic
    # @details This method is used to add a topic to the broker.
    def add_topic(self, id, name):
        topic: Topic = self.__broker.get_topic(id)
        if topic is None:
            topic: Topic = Topic(id, name)
            self.__broker.add_topic(topic)
        return True
    
    ## add_partition method.
    # @param topic_id UUID
    # @param id UUID
    # @param leader boolean
    # @return Partition
    # @details This method is used to add a partition to the broker.
    def add_partition(self, topic_id, id, leader):
        topic: Topic = self.__broker.get_topic(topic_id)
        if topic is None:
            raise("Topic not found")
        topic.add_partition(id, leader)
        return True

    ## __get_topic method.
    # @param id UUID
    # @return Topic
    def __get_topic(self, id: UUID):
        topic: Topic = self.__broker.get_topic(id)
        return topic.to_object()
        
    ## __get_topic_messages method.
    # @param id UUID
    # @param consumer_group_id UUID
    # @return List[Message]
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
    
    ## __get_all_topic_messages method.
    # @param id UUID
    # @return List[Message]
    def __get_all_topic_messages(self, id: UUID):
        aggregate_messages = []
        topic: Topic = self.__broker.get_topic(id)
        for partition in topic.partitions:
            partition_size = partition.size()
            messages = partition.get_messages(0, partition_size)
            aggregate_messages = aggregate_messages + messages
        return aggregate_messages

    ## __get_consumer_group_offsets method.
    # @param partition_id UUID
    # @param consumer_group_id UUID
    # @return offset Integer
    # @details This method is used to get the offset of a consumer group.
    def __get_consumer_group_offsets(self, partition_id, consumer_group_id):
        sender: Sender = Sender(WARDEN_ADDRESS, WARDEN_PORT)
        response = sender.send(Message(GET_CONSUMER_GROUP_OFFSET, {
                "partition_id": str(partition_id),
                "broker_id": str(self.__broker.id),
                "consumer_group_id": str(consumer_group_id),
            }))
        return int(response['offset'])
        
    ## __set_consumer_group_offset method.
    # @param partition_id UUID
    # @param consumer_group_id UUID
    # @param offset Integer
    # @details This method is used to set the offset of a consumer group.
    def __set_consumer_group_offset(self, partition_id, consumer_group_id, offset):
        sender: Sender = Sender(WARDEN_ADDRESS, WARDEN_PORT)
        return sender.send(Message(SET_CONSUMER_GROUP_OFFSET, {
                "partition_id": str(partition_id),
                "broker_id": str(self.__broker.id),
                "consumer_group_id": str(consumer_group_id),
                "offset": offset,
            }))