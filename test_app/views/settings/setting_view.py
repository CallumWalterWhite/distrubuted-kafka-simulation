from tkinter import *
from ..helper import *

class SettingView():
    def view(self, window):
        clear_window(window)
        window.title("Message broker test app") 

        Label(text="Settings", width="300", height="2", font=("Calibri", 13)).pack() 
        default_blank_space(window)
        
        default_blank_space(window)
        
        window.mainloop() 

