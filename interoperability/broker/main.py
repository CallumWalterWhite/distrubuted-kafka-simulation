from .handler.httpHandler import startHttp
from threading import Thread
import asyncio

def start():
    _thread1 = Thread(target=asyncio.run, args=(startHttp(7809),))
    _thread1.start()
    _thread2 = Thread(target=asyncio.run, args=(startHttp(7807),))
    _thread2.start()