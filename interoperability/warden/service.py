import json
import socket
from uuid import uuid4
from interoperability.core import Message, ADD_TOPIC
from interoperability.persistence.repository import Repository
from .offset.offset_repository import OffsetRepository

class Service():
    __repo: Repository
    __offset_repository: OffsetRepository

    def __init__(self, repo: Repository, offset_repository: OffsetRepository):
        self.__repo = repo
        self.__offset_repository = offset_repository

    def add_broker(self, id, address, port):
        self.__repo.add_broker(id, address, port)
        
    def list_brokers(self):
        return self.__repo.list_brokers()

    def delete_all_brokers(self):
        self.__repo.delete_all_brokers()

    def create_partition(self, topic_id):
        partition_id = uuid4()
        self.__repo.add_partition(partition_id, topic_id)
        return partition_id
    
    def add_broker_topic(self, broker, topic_name):
        topic_id = uuid4()
        broker_id = broker[0]
        address = broker[1]
        port = broker[2]
        leader = True #UPDATE TO HAVE REPLICATION
        self.__repo.add_topic(topic_id, topic_name)
        partition_id = self.create_partition(topic_id)
        self.__repo.add_partition_broker(partition_id, broker_id, leader)
        BUFFER_SIZE=128000
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((address, port))
            message : Message = Message(ADD_TOPIC, {
                "id": str(topic_id),
                "leader": leader,
                "name": topic_name
            })
            json_data = message.toJSON().encode()
            s.sendall(json_data)
            data = s.recv(BUFFER_SIZE)
            json_data = str(data.decode("utf-8"))
            message = json.loads(json_data)
            return bool(message["isDone"])

    def get_partition_offset_by_consumer_group(self, topic_id, broker_id, consumer_group_name):
        #TODO: update controllers to only use ids to request
        partition = self.__repo.get_partition_by_broker_and_topic(broker_id, topic_id)
        print(consumer_group_name)
        consumer_group = self.__offset_repository.get_consumer_group_by_name(consumer_group_name)
        print(consumer_group)
        offset = self.__offset_repository.get_consumer_group_offset(consumer_group[0], partition[0])
        print(offset)
        if offset is not None:
            self.__offset_repository.add_offset(0, partition[0], consumer_group[0])
            offset = self.__offset_repository.get_consumer_group_offset(consumer_group[0], partition[0])
        return offset[2]


    def set_partition_offset_by_consumer_group(self, topic_id, broker_id, consumer_group_name, offset):
        #TODO: update controllers to only use ids to request
        self.__offset_repository.update_offset(offset, topic_id, broker_id, consumer_group_name)
        return offset

    def cluster_info(self, consumer_group_name):
        #TODO: update cluster_info to not have empty string check
        if consumer_group_name != "":
            consumer_group = self.__offset_repository.get_consumer_group_by_name(consumer_group_name)
            if consumer_group is None:
                consumer_group_id = uuid4()
                self.__offset_repository.add_consumer_group(consumer_group_id, consumer_group_name)
        topics = self.__repo.list_topics()
        brokers = self.__repo.list_brokers()
        partitions = self.__repo.list_partitions()
        brokers_partitions = self.__repo.list_brokers_partitions()
        result = []
        for topic in topics:
            for partition in partitions:
                if partition[1] == topic[0]:
                    for brokers_partition in brokers_partitions:
                        if brokers_partition[0] == partition[0]:
                            for broker in brokers:
                                if broker[0] == brokers_partition[1]:
                                    result.append({
                                        "topic": topic[1],
                                        "topic_id": topic[0],
                                        "broker_address": broker[1], 
                                        "broker_port": broker[2]
                                    })
        return result

        
        