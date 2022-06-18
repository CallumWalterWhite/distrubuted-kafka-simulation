import os, sys
sys.path.append(f"{os.getcwd()}/interoperability/broker")
sys.path.append(f"{os.getcwd()}/interoperability/core")
sys.path.append(f"{os.getcwd()}/interoperability")
from service.broker_service import BrokerService
from broker import Broker
from controller.broker_controller import BrokerController

## Warden Broker class.
#  @author  Callum White
#  @version 1.0
#  @date    01/06/2022
#  @bug     No known bugs.
#  
#  @details This class is used to create a broker.
class BrokerBootstrap():
    def start_broker():
        broker = Broker()
        service = BrokerService(broker)
        controller = BrokerController(service)
        broker.assign_handler(controller)
        input("Press any key to close broker...")
        broker.close()