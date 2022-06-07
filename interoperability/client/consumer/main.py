from config import *
from consumer import Consumer

def main():
    consumer_group_name = input('Please enter consumer group name - ')
    consumer = Consumer(CLUSTER_ADDRESS, CLUSTER_WARDEN_PORT, consumer_group_name)
    topics = consumer.get_topics()
    index = 1
    for info in topics:
        print(f'{index}. {info["topic"]}')
        index += 1
    selection = int(input("Please select a topic..."))
    topic_broker = topics[selection - 1]
    consumer.listen_to_cluster(topic_broker['topic_id'])

if __name__ == '__main__':
    main()