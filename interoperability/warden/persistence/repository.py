from sqlite3 import Connection
from .bootstrap import Bootstrap

class Repository():
    __conn: Connection
    def __init__(self):
        self.__conn = Bootstrap().get_connection()
    
    def get_consumer_group_by_name(self, consumer_group_name):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM CONSUMER_GROUP WHERE NAME=?", (consumer_group_name,))
        return cur.fetchone()
        
    def get_consumer_group(self, id):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM CONSUMER_GROUP WHERE ID=?", (id,))
        return cur.fetchone()
    
    def add_consumer_group(self, id, name):
        self.__conn.execute(f"INSERT INTO CONSUMER_GROUP (ID,NAME) \
            VALUES ('{id}', '{name}')")
        self.__conn.commit()

    def add_offset(self, position, partition_id, consumer_group_id):
        self.__conn.execute(f"INSERT INTO OFFSET (POSITION, PARTITION_ID, CONSUMER_GROUP_ID) \
            VALUES ({position}, '{partition_id}', '{consumer_group_id}')")
        self.__conn.commit()
    
    def update_offset(self, position, partition_id, consumer_group_id):
        self.__conn.execute(f"UPDATE OFFSET SET POSITION = {position} WHERE CONSUMER_GROUP_ID = '{consumer_group_id}' AND PARTITION_ID = '{partition_id}'")
        self.__conn.commit()
    
    def get_consumer_group_offset(self, partition_id, consumer_group_id):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM OFFSET WHERE CONSUMER_GROUP_ID = ? AND PARTITION_ID = ?", (consumer_group_id, partition_id,))
        return cur.fetchone()
        
    def add_broker(self, id, address, port):
        self.__conn.execute(f"INSERT INTO BROKER (ID,ADDRESS,PORT) \
            VALUES ('{id}', '{address}', {port})")
        self.__conn.commit()
        
    def delete_all_brokers(self):
        self.__conn.execute(f"DELETE FROM BROKER")
        self.__conn.commit()
        
    def list_brokers(self):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM BROKER")
        return cur.fetchall()
        
    def list_topics(self):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM TOPIC")
        return cur.fetchall()

    def list_partitions(self):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM PARTITION")
        return cur.fetchall()
    
    def list_topics(self):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM TOPIC")
        return cur.fetchall()

    def list_brokers_partitions(self):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM PARTITION_BROKER")
        return cur.fetchall()
    
    def get_broker(self, id):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM BROKER WHERE ID = '?'")
        return cur.fetchone((id))
        
    def get_partition(self, id):
        return self.__conn.execute(f"SELECT * FROM PARTITION \
            WHERE ID = '{id}'").fetchone()

    def add_partition(self, id, topic_id):
        self.__conn.execute(f"INSERT INTO PARTITION (ID,TOPIC_ID) \
            VALUES ('{id}', '{topic_id}')")
        self.__conn.commit()
        
    def add_topic(self, id, name):
        self.__conn.execute(f"INSERT INTO TOPIC (ID,NAME) \
            VALUES ('{id}', '{name}')")
        self.__conn.commit()
    
    def add_partition_broker(self, partition_id, broker_id, leader):
        self.__conn.execute(f"INSERT INTO PARTITION_BROKER (PARTITION_ID,BROKER_ID,LEADER) \
            VALUES ('{partition_id}', '{broker_id}', {leader})")
        self.__conn.commit()
