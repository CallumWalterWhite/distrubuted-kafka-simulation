class QueueService():
    __id: int

    def __init__(self, id):
        self.__id = id

    def request(self, source):
        print(f"{self.__id} \n {source}")