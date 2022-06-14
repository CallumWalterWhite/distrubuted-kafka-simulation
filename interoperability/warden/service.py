from uuid import uuid4
from interoperability.core import Message, ADD_TOPIC, ADD_PARTITION, Sender, GET_ALL_MEESAGES
from .persistence.repository import Repository
from config import DEFAULT_REPLICATION_FACTOR

class Service():
    __repo: Repository

    def __init__(self, repo: Repository):
        self.__repo = repo

    def add_broker(self, id, address, port):
        self.__repo.add_broker(id, address, port)
        
    def list_brokers(self):
        return self.__repo.list_brokers()
    
    def list_consumer_groups(self):
        return self.__repo.list_consumer_groups()
        
    def list_topics(self):
        return self.__repo.list_topics()

    def delete_all_brokers(self):
        self.__repo.delete_all_brokers()

    def create_partition(self, topic_id):
        partition_id = uuid4()
        self.__repo.add_partition(partition_id, topic_id)
        return partition_id
    
    def add_topic(self, topic_name, number_of_partitions, replication_factor):
        topic_id = uuid4()
        brokers = self.list_brokers()
        leader = True
        if replication_factor == -1:
            replication_factor = DEFAULT_REPLICATION_FACTOR
        self.__repo.add_topic(topic_id, topic_name)
        partition_ids = []
        add_partition_response = []
        broker_index = 0
        for num in range(0, number_of_partitions):
            partition_id = self.create_partition(topic_id)
            partition_ids.append(partition_id)
            if broker_index >= len(brokers):
                broker_index = 0
            broker = brokers[broker_index]
            broker_index += 1
            broker_id = broker[0]
            address = broker[1]
            port = broker[2]
            self.__repo.add_partition_broker(partition_id, broker_id, leader)
            sender: Sender = Sender(address, port)
            response = sender.send(Message(ADD_TOPIC, {
                    "id": str(topic_id),
                    "name": topic_name
                }))
            if bool(response["isDone"]):
                    response = sender.send(Message(ADD_PARTITION, {
                            "id": str(partition_id),
                            "topic_id": str(topic_id),
                            "leader": leader
                        }))
                    add_partition_response.append((broker_id, bool(response["isDone"])))
        return add_partition_response 

    def get_partition_offset_by_consumer_group(self, partition_id, broker_id, consumer_group_id):
        partition = self.__repo.get_partition(partition_id)
        consumer_group = self.__repo.get_consumer_group(consumer_group_id)
        offset = self.__repo.get_consumer_group_offset(partition[0], consumer_group[0])
        if offset is None:
            self.__repo.add_offset(0, partition[0], consumer_group[0])
            offset = self.__repo.get_consumer_group_offset(partition[0], consumer_group[0])
        return offset[2]

    def set_partition_offset_by_consumer_group(self, partition_id, broker_id, consumer_group_id, offset):
        partition = self.__repo.get_partition(partition_id)
        consumer_group = self.__repo.get_consumer_group(consumer_group_id)
        self.__repo.update_offset(offset, partition[0], consumer_group[0])
        return offset

    def add_consumer_group(self, consumer_group_name):
        consumer_group = self.__repo.get_consumer_group_by_name(consumer_group_name)
        if consumer_group is None:
            consumer_group_id = uuid4()
            self.__repo.add_consumer_group(consumer_group_id, consumer_group_name)
            return consumer_group_id
        return consumer_group[0]

    def cluster_info(self):
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
                                        "partition_id": partition[0],
                                        "partition_leader": brokers_partition[2],
                                        "broker_id": broker[0],
                                        "broker_address": broker[1], 
                                        "broker_port": broker[2]
                                    })
        return result

    def get_topic_messages(self, topic_brokers):
        topic_id = topic_brokers[0]["topic_id"]
        brokers = self.__repo.list_brokers()
        messages = []
        print(brokers)
        for broker in list({v['broker_id']:v for v in topic_brokers}.values()):
            broker = list(filter(lambda x: x[0] == broker['broker_id'], brokers))[0]
            address = broker[1]
            port = broker[2]
            sender: Sender = Sender(address, port)
            response = sender.send(Message(GET_ALL_MEESAGES, {
                    "id": str(topic_id)
                }))
            messages += response["messages"]
        return messages 
    
    