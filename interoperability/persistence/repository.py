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
    
    def get_broker(self, id):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM BROKER WHERE ID = '{id}'")
        return cur.fetchall()[0]
