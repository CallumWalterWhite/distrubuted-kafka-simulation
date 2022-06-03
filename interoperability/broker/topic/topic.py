import array
from uuid import UUID, uuid4
from topic.partition.partition import Partition


class Topic():
    id: UUID
    name: str
    __partition: Partition

    def __init__(self, id: UUID, name: str):
        self.id = id
        self.name = name
        self.__partition = Partition(uuid4())
    
    def add_message(self, body):
        self.__partition.add_message(body)

    def get_partition_size(self):
        return self.__partition.size() 

    def get_messages(self, offset):
        return self.__partition.get_messages(offset, self.get_partition_size())

    def to_object(self):
        return {
            'id': str(self.id),
            'name': self.name
        }