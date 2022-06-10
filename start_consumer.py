from interoperability.client.consumer.consumer import Consumer

def main():
    try:
        consumer = Consumer.bootstrap_consumer()
        input("Press any key to close consumer...")
        consumer.stop()
    except Exception as ex:
        print('Caught this error: ' + repr(ex))
        print('Error has occured on consumer thread, instance is stopping....')

if __name__ == "__main__":
    main()