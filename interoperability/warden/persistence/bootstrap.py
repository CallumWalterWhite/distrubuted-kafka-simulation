from sqlite3 import Connection
import sqlite3
import os

class Bootstrap():
    def __init__(self):
        try:
            self.__conn = sqlite3.connect(f'db/WARDEN.db', check_same_thread=False)
        except sqlite3.OperationalError:
            os.mkdir('db')
        finally:
            self.__conn = sqlite3.connect(f'db/WARDEN.db', check_same_thread=False)
        self.__inflate()

    def get_connection(self):
        return self.__conn
    
    def __inflate(self):
        self.__create_broker_table()
        self.__create_topic_table()
        self.__create_partition_table()
        self.__create_partition_broker_table()
        self.__create_offset_table()
        self.__create_consumer_group_table()

    def __create_broker_table(self):
        try:   
            self.__conn.execute('''CREATE TABLE BROKER
                    (ID INT PRIMARY KEY     NOT NULL,
                    ADDRESS           TEXT    NOT NULL,
                    PORT        INT NOT NULL);''')
            self.__conn.commit()
        except:
            self.__conn.execute('DELETE FROM BROKER')
            self.__conn.commit()
    
    def __create_topic_table(self):
        try:   
            self.__conn.execute('''CREATE TABLE TOPIC
                    (ID INT PRIMARY KEY     NOT NULL,
                    NAME NVARCHAR(255) NOT NULL);''')
            self.__conn.commit()
        except:
            self.__conn.execute('DELETE FROM TOPIC')
            self.__conn.commit()

    def __create_partition_table(self):
        try:   
            self.__conn.execute('''CREATE TABLE PARTITION
                    (ID INT PRIMARY KEY     NOT NULL,
                    TOPIC_ID INT NOT NULL);''')
            self.__conn.commit()
        except:
            self.__conn.execute('DELETE FROM PARTITION')
            self.__conn.commit()
            
    def __create_partition_broker_table(self):
        try:   
            self.__conn.execute('''CREATE TABLE PARTITION_BROKER
                    (PARTITION_ID INT NOT NULL,
                    BROKER_ID INT NOT NULL,
                    LEADER BIT NOT NULL);''')
            self.__conn.commit()
        except:
            self.__conn.execute('DELETE FROM PARTITION_BROKER')
            self.__conn.commit()

        
    def __create_offset_table(self):
        try:   
            self.__conn.execute('''CREATE TABLE OFFSET
                    (PARTITION_ID INT NOT NULL,
                    CONSUMER_GROUP_ID INT NOT NULL,
                    POSITION INT NOT NULL);''')
            self.__conn.commit()
        except:
            self.__conn.execute('DELETE FROM OFFSET')
            self.__conn.commit()
    
    def __create_consumer_group_table(self):
        try:   
            self.__conn.execute('''CREATE TABLE CONSUMER_GROUP
                    (ID INT PRIMARY KEY     NOT NULL,
                    NAME NVARCHAR(255) NOT NULL);''')
            self.__conn.commit()
        except:
            self.__conn.execute('DELETE FROM CONSUMER_GROUP')
            self.__conn.commit()