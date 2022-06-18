from uuid import uuid4
from interoperability.core import Message, ADD_TOPIC, ADD_PARTITION, Sender, GET_ALL_MEESAGES
from .persistence.repository import Repository
from config import DEFAULT_REPLICATION_FACTOR

## Service class.
#  @author  Callum White
#  @version 1.0
#  @date    01/06/2022
#  @bug     No known bugs.
#  
#  @details This class is used to create a service object for the warden.
class Service():
    # repository variable
    __repo: Repository

    ## __init__ method.
    # @param self The object pointer.
    # @param repo The repository object.
    # @return None.
    def __init__(self, repo: Repository):
        self.__repo = repo

    ## add_broker method.
    # @param self The object pointer.
    # @param id The id of the broker.
    # @param address The address of the broker.
    # @param port The port of the broker.
    # @return None.
    def add_broker(self, id, address, port):
        self.__repo.add_broker(id, address, port)
    
    ## list_brokers method.
    # @param self The object pointer.
    # @return brokers The list of brokers.
    def list_brokers(self):
        return self.__repo.list_brokers()
    
    ## list_consumer_groups method.
    # @param self The object pointer.
    # @return consumer_groups The list of consumer groups.
    def list_consumer_groups(self):
        return self.__repo.list_consumer_groups()
        
    ## list_topics method.
    # @param self The object pointer.
    # @return topics The list of topics.
    def list_topics(self):
        return self.__repo.list_topics()

    ## delete_all_brokers method.
    # @param self The object pointer.
    # @return None.
    # @details This method is used to delete all brokers.
    def delete_all_brokers(self):
        self.__repo.delete_all_brokers()

    ## create_partition method.
    # @param self The object pointer.
    # @param topic_id The id of the topic.
    # @return partition_id The id of the partition.
    # @details This method is used to create a partition.
    def create_partition(self, topic_id):
        partition_id = uuid4()
        self.__repo.add_partition(partition_id, topic_id)
        return partition_id
    
    ## add_topic method.
    # @param self The object pointer.
    # @param topic_name The name of the topic.
    # @param number_of_partitions The number of partitions.
    # @param replication_factor The replication factor.
    # @return list of partition added to brokers.
    # @details This method is used to add a topic to the cluster with the given number of partitions and replication factor.
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

    ## get_partition_offset_by_consumer_group method.
    # @param self The object pointer.
    # @param partition_id The id of the partition.
    # @param broker_id The id of the broker.
    # @param consumer_group_id The id of the consumer group.
    # @return offset The offset of the partition by the consumer group.
    def get_partition_offset_by_consumer_group(self, partition_id, broker_id, consumer_group_id):
        partition = self.__repo.get_partition(partition_id)
        consumer_group = self.__repo.get_consumer_group(consumer_group_id)
        offset = self.__repo.get_consumer_group_offset(partition[0], consumer_group[0])
        if offset is None:
            self.__repo.add_offset(0, partition[0], consumer_group[0])
            offset = self.__repo.get_consumer_group_offset(partition[0], consumer_group[0])
        return offset[2]

    ## set_partition_offset_by_consumer_group method.
    # @param self The object pointer.
    # @param partition_id The id of the partition.
    # @param broker_id The id of the broker.
    # @param consumer_group_id The id of the consumer group.
    # @param offset The offset of the partition by the consumer group.
    # @return None.
    # @details This method is used to set the offset of the partition by the consumer group.
    def set_partition_offset_by_consumer_group(self, partition_id, broker_id, consumer_group_id, offset):
        partition = self.__repo.get_partition(partition_id)
        consumer_group = self.__repo.get_consumer_group(consumer_group_id)
        self.__repo.update_offset(offset, partition[0], consumer_group[0])
        return offset

    ## add_consumer_group method.
    # @param self The object pointer.
    # @param consumer_group_name The name of the consumer group.
    # @return consumer_group_id The id of the consumer group.
    # @details This method is used to add a consumer group to the cluster.
    def add_consumer_group(self, consumer_group_name):
        consumer_group = self.__repo.get_consumer_group_by_name(consumer_group_name)
        if consumer_group is None:
            consumer_group_id = uuid4()
            self.__repo.add_consumer_group(consumer_group_id, consumer_group_name)
            return consumer_group_id
        return consumer_group[0]

    ## cluster_info method.
    # @param self The object pointer.
    # @return cluster_info The cluster information.
    # @details This method is used to get the cluster information.
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

    ## get_topic_messages method.
    # @param self The object pointer.
    # @param topic_broker_id The id of the topic brokers.
    # @return messages The messages of the topic brokers.
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
    
    