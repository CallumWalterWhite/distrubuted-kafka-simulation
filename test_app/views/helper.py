from packages.tkinter import *

def default_blank_space(window):
    Label(window, text="", background='lightblue').pack()

def clear_window(window):
    _list = window.winfo_children()
    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())
    for item in _list:
        item.pack_forget()
    reset_window(window)

def reset_window(window):
    window.configure(background='lightblue')