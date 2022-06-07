import sys, os
from tkinter import *
sys.path.append(f"{os.getcwd()}/interoperability")
from core import *

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

def check_cluster_status():
    try:
        sender: Sender = Sender('127.0.0.1', 2500)
        response = sender.send(Message(HEALTH_CHECK, {
            }))
        if response.status == 'OK':
            return True
    except:
        return False
    return False