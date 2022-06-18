import array
from uuid import UUID, uuid4
from topic.partition.partition import Partition

## Topic class.
#  @author  Callum White
#  @version 1.0
#  @date    01/06/2022
#  @bug     No known bugs.
#  
#  @details This class is the Topic within a broker instance. 
#  It holds the partitions.
class Topic():
    # id variable
    id: UUID
    # name of the topic variable
    name: str
    # partitions variable
    partitions: array

    ## __init__ method.
    # @param self The object pointer.
    # @param id The id of the topic.
    # @param name The name of the topic.
    def __init__(self, id: UUID, name: str):
        self.id = id
        self.name = name
        self.partitions = []

    ## add_partition method.
    # @param self The object pointer.
    # @param partition The partition to add.
    # @return None.
    # @details This method is used to add a partition to the topic.
    def add_partition(self, id, leader):
        self.partitions.append(Partition(id, leader))
    
    ## get_partition method.
    # @param self The object pointer.
    # @param id The id of the partition.
    # @details This method is used to get a partition from the topic.
    # @return partition The partition object.
    def get_partition(self, id):
        partitions = [x for x in self.partitions if x.id == id]
        if len(partitions) == 0:
            return None
        return partitions[0]

    ## to_object method.
    # @param self The object pointer.
    # @return object The topic as a JSON object.
    def to_object(self):
        return {
            'id': str(self.id),
            'name': self.name
        }