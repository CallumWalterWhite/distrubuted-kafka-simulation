import sqlite3
import os

from interoperability.persistence.repository import Repository

class PersistenceProvider:
    def getRepo(id):
        try:
            conn = sqlite3.connect(f'db/{id}.db')
        except sqlite3.OperationalError:
            os.mkdir('db')
        finally:
            conn = sqlite3.connect(f'db/{id}.db')
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
            
    def create_topic_table(conn):
        try:   
            conn.execute('''CREATE TABLE TOPIC
                    (ID INT PRIMARY KEY     NOT NULL,
                    ADDRESS           TEXT    NOT NULL,
                    PORT        INT NOT NULL);''')
            conn.commit()
        except:
            print('Table already exist... \n')
