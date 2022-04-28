import sqlite3
from sqlite3 import Connection

class Repository:
    __conn: Connection

    def __init__(self, conn: Connection):
        self.__conn = conn