import array
from uuid import UUID


class Partition():
    id: UUID
    __leader: bool
    __queue: array
    def __init__(self, id: UUID):
        self.id = id
        self.__leader = False
        self.__queue = []

    def set_leader(self, lead):
        self.__leader = lead

    def add_message(self, body):
        self.__queue.append(body)

    def get_messages(self, inital_offset, final_offset):
        return self.__queue[inital_offset:final_offset]

    def size(self):
        return len(self.__queue)