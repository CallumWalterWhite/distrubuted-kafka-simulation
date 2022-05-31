from packages.tkinter import *
from ..helper import *

class HomeView():
    def view(self, window):
        clear_window(window)
        window.title("Account Login") 

        Label(text="Welcome to the library system", width="300", height="2", font=("Calibri", 13)).pack() 
        default_blank_space(window)
        
        def loginTest():
            self.__controller.LoginMenuRedirect(window)
        
        Button(text="Login", height="2", width="30", command=loginTest).pack() 
        default_blank_space(window)
 

