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
        PersistenceProvider.initailzeRepo(repo)

    def initailzeRepo(repo: Repository):
        pass
        
