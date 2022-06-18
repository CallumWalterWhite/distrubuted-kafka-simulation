import array
from uuid import UUID


## Partition class.
#  @author  Callum White
#  @version 1.0
#  @date    01/06/2022
#  @bug     No known bugs.
#  
#  @details This class is the Partition within a topic instance. 
class Partition():
    # id variable
    id: UUID
    # leader variable
    __leader: bool
    # queue variable
    __queue: array
    ## __init__ method.
    # @param self The object pointer.
    # @param id The id of the partition.
    # @param leader The leader of the partition.
    def __init__(self, id: UUID, leader: bool):
        self.id = id
        self.__leader = leader
        self.__queue = []
    
    ## set_leader method.
    # @param self The object pointer.
    # @param leader The leader of the partition.
    def set_leader(self, lead):
        self.__leader = lead

    ## add_message method.
    # @param self The object pointer.
    # @param body The body of the message.
    # @return None.
    # @details This method is used to add a message to the partition.
    def add_message(self, body):
        self.__queue.append(body)

    ## get_messages method.
    # @param self The object pointer.
    # @param inital_offset first index to get.
    # @param final_offset last index to get.
    # @return messages The messages in the partition.
    def get_messages(self, inital_offset, final_offset):
        return self.__queue[inital_offset:final_offset]

    ## size method.
    # @param self The object pointer.
    # @return size The size of the partition.
    def size(self):
        return len(self.__queue)