from sqlite3 import Connection
from .bootstrap import Bootstrap

## Warden Bootstrap class.
#  @author  Callum White
#  @version 1.0
#  @date    01/06/2022
#  @bug     No known bugs.
#  
#  @details This class is used to send queries to the database.
class Repository():
    # sqlite3 connection variable.
    __conn: Connection
    ## __init__ method.
    # @param self The object pointer.
    def __init__(self):
        self.__conn = Bootstrap().get_connection()
    
    ## get_consumer_group_by_name method.
    #  @param self The object pointer.
    #  @param consumer_group_name The name of the consumer group.
    #  @return The consumer group.
    def get_consumer_group_by_name(self, consumer_group_name):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM CONSUMER_GROUP WHERE NAME=?", (consumer_group_name,))
        return cur.fetchone()
        
    ## get_consumer_group method.
    #  @param self The object pointer.
    #  @param consumer_group_id The id of the consumer group.
    #  @return The consumer group.
    def get_consumer_group(self, id):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM CONSUMER_GROUP WHERE ID=?", (id,))
        return cur.fetchone()
    
    ## add_consumer_group method.
    #  @param self The object pointer.
    #  @param id The id of the consumer group.
    #  @param name The name of the consumer group.
    def add_consumer_group(self, id, name):
        self.__conn.execute(f"INSERT INTO CONSUMER_GROUP (ID,NAME) \
            VALUES ('{id}', '{name}')")
        self.__conn.commit()

    ## add_offset method.
    #  @param self The object pointer.
    #  @param position The position of the offset.
    #  @param partition_id The id of the partition.
    #  @param consumer_group_id The id of the consumer group.
    def add_offset(self, position, partition_id, consumer_group_id):
        self.__conn.execute(f"INSERT INTO OFFSET (POSITION, PARTITION_ID, CONSUMER_GROUP_ID) \
            VALUES ({position}, '{partition_id}', '{consumer_group_id}')")
        self.__conn.commit()
    
    ## update_offset method.
    #  @param self The object pointer.
    #  @param position The position of the offset.
    #  @param partition_id The id of the partition.
    #  @param consumer_group_id The id of the consumer group.
    def update_offset(self, position, partition_id, consumer_group_id):
        self.__conn.execute(f"UPDATE OFFSET SET POSITION = {position} WHERE CONSUMER_GROUP_ID = '{consumer_group_id}' AND PARTITION_ID = '{partition_id}'")
        self.__conn.commit()
    
    ## get_consumer_group_offset method.
    #  @param self The object pointer.
    #  @param partition_id The id of the partition.
    #  @param consumer_group_id The id of the consumer group.
    #  @return The offset.
    def get_consumer_group_offset(self, partition_id, consumer_group_id):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM OFFSET WHERE CONSUMER_GROUP_ID = ? AND PARTITION_ID = ?", (consumer_group_id, partition_id,))
        return cur.fetchone()
        
    ## add_broker method.
    #  @param self The object pointer.
    #  @param id The id of the broker.
    #  @param address The address of the broker.
    #  @param port The port of the broker.
    def add_broker(self, id, address, port):
        self.__conn.execute(f"INSERT INTO BROKER (ID,ADDRESS,PORT) \
            VALUES ('{id}', '{address}', {port})")
        self.__conn.commit()
        
    ## delete_all_brokers method.
    #  @param self The object pointer.
    def delete_all_brokers(self):
        self.__conn.execute(f"DELETE FROM BROKER")
        self.__conn.commit()
        
    ## list_brokers method.
    #  @param self The object pointer.
    def list_brokers(self):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM BROKER")
        return cur.fetchall()
        
    ## list_topics method.
    #  @param self The object pointer.
    def list_topics(self):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM TOPIC")
        return cur.fetchall()
    
    ## list_consumer_groups method.
    #  @param self The object pointer.
    def list_consumer_groups(self):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM CONSUMER_GROUP")
        return cur.fetchall()

    ## list_partitions method.
    #  @param self The object pointer.
    def list_partitions(self):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM PARTITION")
        return cur.fetchall()
    
    ## list_topics method.
    #  @param self The object pointer.
    def list_topics(self):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM TOPIC")
        return cur.fetchall()

    ## list_brokers_partitions method.
    #  @param self The object pointer.
    def list_brokers_partitions(self):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM PARTITION_BROKER")
        return cur.fetchall()
    
    ## get_broker method.
    #  @param self The object pointer.
    #  @param id The id of the broker.
    def get_broker(self, id):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM BROKER WHERE ID = '?'")
        return cur.fetchone((id))
        
    ## get_partition method.
    #  @param self The object pointer.
    #  @param id The id of the broker.
    def get_partition(self, id):
        return self.__conn.execute(f"SELECT * FROM PARTITION \
            WHERE ID = '{id}'").fetchone()

    ## add_partition method.
    #  @param self The object pointer.
    #  @param id The id of the partition.
    #  @param topic_id The id of the topic.
    def add_partition(self, id, topic_id):
        self.__conn.execute(f"INSERT INTO PARTITION (ID,TOPIC_ID) \
            VALUES ('{id}', '{topic_id}')")
        self.__conn.commit()
        
    ## add_topic method.
    #  @param self The object pointer.
    #  @param id The id of the topic.
    #  @param name The name of the topic.
    def add_topic(self, id, name):
        self.__conn.execute(f"INSERT INTO TOPIC (ID,NAME) \
            VALUES ('{id}', '{name}')")
        self.__conn.commit()
    
    ## add_partition_broker method.
    #  @param self The object pointer.
    #  @param partition_id The id of the partition.
    #  @param broker_id The id of the broker.
    #  @param leader True if the partition is the leader.
    def add_partition_broker(self, partition_id, broker_id, leader):
        self.__conn.execute(f"INSERT INTO PARTITION_BROKER (PARTITION_ID,BROKER_ID,LEADER) \
            VALUES ('{partition_id}', '{broker_id}', {leader})")
        self.__conn.commit()
