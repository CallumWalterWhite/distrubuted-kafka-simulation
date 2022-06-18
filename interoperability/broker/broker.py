import array, sys, os
sys.path.append(f"{os.getcwd()}/interoperability/broker")
sys.path.append(f"{os.getcwd()}/interoperability/core")
sys.path.append(f"{os.getcwd()}/interoperability")
from uuid import UUID
from registry.warden_register import WardenRegister
from registry.port_factory import PortFactory
from topic.topic import Topic
from core import TCPServe

## Warden Broker class.
#  @author  Callum White
#  @version 1.0
#  @date    01/06/2022
#  @bug     No known bugs.
#  
#  @details This class is the broker. 
#  It holds the topics.
class Broker():
    # topics variable
    topics: array
    # id variable
    id: UUID
    # port variable
    port: int
    # __tcpServe variable
    __tcpServe: TCPServe
    ## __init__ method.
    # @param self The object pointer.
    # @param id The id of the broker.
    def __init__(self, id=None):
        self.port = PortFactory.get_first_available_port()
        if id is None:
            id = WardenRegister.register(self.port)
        self.id = id
        self.topics = []

    ## close method.
    # @param self The object pointer.
    # @details This method is used to close the broker.
    def close(self):
        self.__tcpServe.close()

    ## assign_handler method.
    # @param self The object pointer.
    # @param controller The controller object.
    # @details This method is used to assign a handler to the broker.
    def assign_handler(self, controller):
        self.__tcpServe = TCPServe(self.port, controller)

    ## add_topic method.
    # @param self The object pointer.
    # @param topic The topic object.
    # @details This method is used to add a topic to the broker.
    def add_topic(self, topic: Topic):
        self.topics.append(topic)

    ## get_topic method.
    # @param self The object pointer.
    # @param topic_id The id of the topic.
    # @details This method is used to get a topic from the broker.
    # @return topic The topic object.
    def get_topic(self, id):
        topics = [x for x in self.topics if x.id == id]
        if len(topics) == 0:
            return None
        return topics[0]