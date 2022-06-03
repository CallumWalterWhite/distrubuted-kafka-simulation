from sqlite3 import Connection
import sqlite3
import os

class OffsetRepository():
    __conn: Connection
    def __init__(self):
        id='WARDEN'
        try:
            self.__conn = sqlite3.connect(f'db/{id}.db', check_same_thread=False)
        except sqlite3.OperationalError:
            os.mkdir('db')
        finally:
            self.__conn = sqlite3.connect(f'db/{id}.db', check_same_thread=False)
        self.__create_offset_table()
        self.__create_consumer_group_table()
        
    def __create_offset_table(self):
        try:   
            self.__conn.execute('''CREATE TABLE OFFSET
                    (PARTITION_ID INT NOT NULL,
                    CONSUMER_GROUP_ID INT NOT NULL,
                    POSITION INT NOT NULL);''')
            self.__conn.commit()
        except:
            print('Table already exist... \n')
    
    def __create_consumer_group_table(self):
        try:   
            self.__conn.execute('''CREATE TABLE CONSUMER_GROUP
                    (ID INT PRIMARY KEY     NOT NULL,
                    NAME NVARCHAR(255) NOT NULL);''')
            self.__conn.commit()
        except:
            print('Table already exist... \n')
    
    def get_consumer_group_by_name(self, consumer_group_name):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM CONSUMER_GROUP WHERE NAME=?", (consumer_group_name,))
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
        
