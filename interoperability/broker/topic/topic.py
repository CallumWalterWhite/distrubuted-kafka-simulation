import array
from uuid import UUID, uuid4

from numpy import partition

from interoperability.broker.topic.partition.partition import Partition


class Topic():
    id: UUID
    name: str
    __partitions: array

    def __init__(self, id: UUID, name: str):
        self.id = id
        self.name = name
        self.__partitions = []
        #DEFAULT PARTITION
        partition: Partition = Partition(uuid4())
        self.add_partition(partition)
        
    def add_partition(self, partition: Partition):
        self.__partitions.append(partition)

    def add_message(self, body):
        pass
        
    def to_object(self):
        return {
            'id': str(self.id),
            'name': self.name
        }