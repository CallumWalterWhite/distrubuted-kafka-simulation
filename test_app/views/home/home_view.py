from tkinter import *
from tkinter import messagebox
from ..helper import *
from ..settings.setting_view import SettingView
from ..stresser.stresser_view import StresserView

class HomeView():
    def view(self, window):
        clear_window(window)
        window.title("Message broker test app") 

        Label(text="Welcome to message broker test application", width="300", height="2", font=("Calibri", 13)).pack() 
        default_blank_space(window)
        
        def __createMenuOption(window, text, callback):
            Button(window, text=text, width=20, height=5, command=callback).pack()

        def __go_settins():
            SettingView().view(window)
            
        def __go_stresser():
            StresserView().view(window)
            
        def __check_cluster_status():
            msg = 'Cluster is running' if check_cluster_status() else 'Cluster is not running'
            messagebox.showinfo(title='Status', message=msg)

        __createMenuOption(window, "Settings", __go_settins)
        __createMenuOption(window, "Stress tool", __go_stresser)
        __createMenuOption(window, "Check cluster", __check_cluster_status)
        
        default_blank_space(window)
        
        window.mainloop() 

