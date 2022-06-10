import sys, os
from tkinter import *
sys.path.append(f"{os.getcwd()}/interoperability")
from core import *

def default_blank_space(root):
    Label(root, text="", background='lightblue').pack()

def clear_root(root):
    _list = root.winfo_children()
    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())
    for item in _list:
        item.pack_forget()
    reset_root(root)

def reset_root(root):
    root.configure(background='lightblue')

def check_cluster_status():
    try:
        sender: Sender = Sender('127.0.0.1', 2500)
        response = sender.send(Message(HEALTH_CHECK, {
            }))
        if response['status'] == 'ok':
            return True
    except:
        return False
    return False