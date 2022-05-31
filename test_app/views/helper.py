from ..packages.tkinter import *

@staticmethod
def default_blank_space(window):
    Label(window, text="", background='lightblue').pack()

@staticmethod
def clear_window(window):
    _list = window.winfo_children()
    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())
    for item in _list:
        item.pack_forget()
    reset_window(window)

@staticmethod
def reset_window(window):
    window.configure(background='lightblue')