from packages.tkinter import *
from ..helper import *

class HomeView():
    def view(self, window):
        clear_window(window)
        window.title("Message broker test app") 

        Label(text="Welcome to message broker test application", width="300", height="2", font=("Calibri", 13)).pack() 
        default_blank_space(window)
        
        def loginTest():
            self.__controller.LoginMenuRedirect(window)
        
        default_blank_space(window)
        
        window.mainloop() 

