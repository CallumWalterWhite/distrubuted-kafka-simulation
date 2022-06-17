from interoperability.broker.bootstrap import BrokerBootstrap

"""@package Broker
Start broker.
 @author  Callum White
 @version 1.0
 @date    01/06/2022
 @bug     No known bugs.
 @todo    Add replication for partitions.
 
 @detail - starts up a broker instance
"""
def main():
    try:
        BrokerBootstrap.start_broker()
    except Exception as ex:
        print('Caught this error: ' + repr(ex))
        print('Error has occured on broker thread, instance is stopping....')

if __name__ == "__main__":
    main()