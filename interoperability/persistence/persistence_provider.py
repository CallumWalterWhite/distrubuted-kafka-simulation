import sqlite3
import os
from repository import Repository

class PersistenceProvider:
    def getRepo(id):
        try:
            conn = sqlite3.connect(f'db/{id}.db', check_same_thread=False)
        except sqlite3.OperationalError:
            os.mkdir('db')
        finally:
            conn = sqlite3.connect(f'db/{id}.db', check_same_thread=False)
        repo = Repository(conn)
        PersistenceProvider.initailzeRepo(conn, repo)
        return repo

    def initailzeRepo(conn, repo: Repository):
        PersistenceProvider.create_broker_table(conn)
        
    def create_broker_table(conn):
        try:   
            conn.execute('''CREATE TABLE BROKER
                    (ID INT PRIMARY KEY     NOT NULL,
                    ADDRESS           TEXT    NOT NULL,
                    PORT        INT NOT NULL);''')
            conn.commit()
        except:
            print('Table already exist... \n')
            PersistenceProvider.delete_broker_table(conn)

    def delete_broker_table(conn):
            conn.execute('DELETE FROM BROKER')
            conn.commit()
            
    def create_topic_table(conn):
        try:   
            conn.execute('''CREATE TABLE TOPIC
                    (ID INT PRIMARY KEY     NOT NULL,
                    ADDRESS           TEXT    NOT NULL,
                    PORT        INT NOT NULL);''')
            conn.commit()
        except:
            print('Table already exist... \n')
