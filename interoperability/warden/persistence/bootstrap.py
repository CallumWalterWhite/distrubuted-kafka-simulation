from sqlite3 import Connection
import sqlite3
import os

## Warden Bootstrap class.
#  @author  Callum White
#  @version 1.0
#  @date    01/06/2022
#  @bug     No known bugs.
#  
#  @details This class is used to bootstrap the Warden database.
class Bootstrap():
    ## __init__ method.
    #  @param self The object pointer.
    #  @details This method connects to the Warden database and creates the warden table.
    def __init__(self):
        try:
            self.__conn = sqlite3.connect(f'db/WARDEN.db', check_same_thread=False)
        except sqlite3.OperationalError:
            os.mkdir('db')
        finally:
            self.__conn = sqlite3.connect(f'db/WARDEN.db', check_same_thread=False)
        self.__inflate()

    ## get_connection method.
    #  @param self The object pointer.
    #  @return The connection to the database.
    def get_connection(self):
        return self.__conn
    
    ## __inflate method.
    #  @param self The object pointer.
    #  @details This method will inflate the database.
    def __inflate(self):
        self.__create_broker_table()
        self.__create_topic_table()
        self.__create_partition_table()
        self.__create_partition_broker_table()
        self.__create_offset_table()
        self.__create_consumer_group_table()

    ## __create_broker_table method.
    #  @param self The object pointer.
    #  @details This method will create the broker table.
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
    
    ## __create_topic_table method.
    #  @param self The object pointer.
    #  @details This method will create the topic table.
    def __create_topic_table(self):
        try:   
            self.__conn.execute('''CREATE TABLE TOPIC
                    (ID INT PRIMARY KEY     NOT NULL,
                    NAME NVARCHAR(255) NOT NULL);''')
            self.__conn.commit()
        except:
            self.__conn.execute('DELETE FROM TOPIC')
            self.__conn.commit()

    ## __create_partition_table method.
    #  @param self The object pointer.
    #  @details This method will create the partition table.
    def __create_partition_table(self):
        try:   
            self.__conn.execute('''CREATE TABLE PARTITION
                    (ID INT PRIMARY KEY     NOT NULL,
                    TOPIC_ID INT NOT NULL);''')
            self.__conn.commit()
        except:
            self.__conn.execute('DELETE FROM PARTITION')
            self.__conn.commit()
            
    ## __create_partition_broker_table method.
    #  @param self The object pointer.
    #  @details This method will create the partition broker table.
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

    ## __create_offset_table method.
    #  @param self The object pointer.
    #  @details This method will create the offset table.
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
    
    ## __create_consumer_group_table method.
    #  @param self The object pointer.
    #  @details This method will create the consumer group table.
    def __create_consumer_group_table(self):
        try:   
            self.__conn.execute('''CREATE TABLE CONSUMER_GROUP
                    (ID INT PRIMARY KEY     NOT NULL,
                    NAME NVARCHAR(255) NOT NULL);''')
            self.__conn.commit()
        except:
            self.__conn.execute('DELETE FROM CONSUMER_GROUP')
            self.__conn.commit()