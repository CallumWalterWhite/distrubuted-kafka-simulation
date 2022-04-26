from threading import Thread
import asyncio

from interoperability.broker.controller.controllerService import ControllerService
from .handler.httpHandler import HTTPHandler

def start():
    httpHandler1 = HTTPHandler(2700)
    httpHandler2 = HTTPHandler(2701)