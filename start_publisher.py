from interoperability.client.publisher.publisher import Publisher

def main():
    try:
        Publisher.bootstrap_publisher()
    except Exception as ex:
        print('Caught this error: ' + repr(ex))
        print('Error has occured on publisher thread, instance is stopping....')

if __name__ == "__main__":
    main()