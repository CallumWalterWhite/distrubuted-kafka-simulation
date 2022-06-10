from interoperability.broker.bootstrap import BrokerBootstrap

def main():
    try:
        BrokerBootstrap.start_broker()
    except Exception as ex:
        print('Caught this error: ' + repr(ex))
        print('Error has occured on broker thread, instance is stopping....')

if __name__ == "__main__":
    main()