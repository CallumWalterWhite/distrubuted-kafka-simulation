from sqlite3 import Connection

class Repository:
    __conn: Connection

    def __init__(self, conn: Connection):
        self.__conn = conn

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
        
    def get_partition_by_broker_and_topic(self, broker_id, topic_id):
        return self.__conn.execute(f"SELECT PARTITION.* FROM PARTITION \
            JOIN PARTITION_BROKER ON PARTITION.ID = PARTITION_BROKER.PARTITION_ID WHERE PARTITION_BROKER.BROKER_ID = '{broker_id}' AND TOPIC_ID = '{topic_id}'").fetchone()

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
