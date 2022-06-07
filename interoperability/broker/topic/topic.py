import array
from uuid import UUID, uuid4
from topic.partition.partition import Partition


class Topic():
    id: UUID
    name: str
    partitions: array

    def __init__(self, id: UUID, name: str):
        self.id = id
        self.name = name
        self.partitions = []

    def add_partition(self, id, leader):
        self.partitions.append(Partition(id, leader))
    
    def get_partition(self, id):
        partitions = [x for x in self.partitions if x.id == id]
        if len(partitions) == 0:
            return None
        return partitions[0]

    def to_object(self):
        return {
            'id': str(self.id),
            'name': self.name
        }