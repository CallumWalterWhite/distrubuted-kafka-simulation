from tkinter import *
from .window_view import WindowViewer

class TestApp():
    def __init__(self):
        self.root = Tk()
        self.root.geometry("1920x1080")
        WindowViewer().home(self.root)
