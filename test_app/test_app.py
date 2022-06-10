import os, sys
sys.path.append(f"{os.getcwd()}/interoperability")
from tkinter import *
from .window_view import WindowViewer

class TestApp():
    def __init__(self):
        WindowViewer().home()
