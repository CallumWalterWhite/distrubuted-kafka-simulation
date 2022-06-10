from tkinter import *
from tkinter import messagebox
from .helper import *

class WindowViewer():
    def home(self, root):
        clear_root(root)
        root.title("Message broker test app") 

        Label(text="Welcome to message broker test application", width="300", height="2", font=("Calibri", 13)).pack() 
        default_blank_space(root)
        
        def __createMenuOption(root, text, callback):
            Button(root, text=text, width=20, height=5, command=callback).pack()

        def __go_stresser():
            self.stresser(root)
            
        def __check_cluster_status():
            msg = 'Cluster is running' if check_cluster_status() else 'Cluster is not running'
            messagebox.showinfo(title='Status', message=msg)

        __createMenuOption(root, "Stress tool", __go_stresser)
        __createMenuOption(root, "Check cluster", __check_cluster_status)
        
        default_blank_space(root)
        
        root.mainloop() 
    
    def stresser(self, root):
        clear_root(root)
        root.title("Message broker test app")

        def __go_home():
            self.home(root)

        widget_frame = Frame(root)
        widget_frame.pack(side='left', anchor=NW)
        Button(widget_frame, text='Back', command=__go_home).pack()

        #this creates 'Label' widget for Registration Form and uses place() method.
        label_0 =Label(root,text="Stress tool", width=20,font=("bold",20))
        #place method in tkinter is  geometry manager it is used to organize widgets by placing them in specific position
        label_0.place(x=90,y=60)

        #this creates 'Label' widget for Fullname and uses place() method.
        label_1 =Label(root,text="FullName", width=20,font=("bold",10))
        label_1.place(x=80,y=130)

        #this will accept the input string text from the user.
        entry_1=Entry(root)
        entry_1.place(x=240,y=130)

        #this creates 'Label' widget for Email and uses place() method.
        label_3 =Label(root,text="Email", width=20,font=("bold",10))
        label_3.place(x=68,y=180)

        entry_3=Entry(root)
        entry_3.place(x=240,y=180)

        #this creates 'Label' widget for Gender and uses place() method.
        label_4 =Label(root,text="Gender", width=20,font=("bold",10))
        label_4.place(x=70,y=230)


        #the variable 'var' mentioned here holds Integer Value, by deault 0
        var=IntVar()

        #this creates 'Radio button' widget and uses place() method
        Radiobutton(root,text="Male",padx= 5, variable= var, value=1).place(x=235,y=230)
        Radiobutton(root,text="Female",padx= 20, variable= var, value=2).place(x=290,y=230)


        ##this creates 'Label' widget for country and uses place() method.
        label_5=Label(root,text="Country",width=20,font=("bold",10))
        label_5.place(x=70,y=280)

        #this creates list of countries available in the dropdownlist.
        list_of_country=[ 'India' ,'US' , 'UK' ,'Germany' ,'Austria']

        #the variable 'c' mentioned here holds String Value, by default ""
        c=StringVar()
        droplist=OptionMenu(root,c, *list_of_country)
        droplist.config(width=15)
        c.set('Select your Country')
        droplist.place(x=240,y=280)

        ##this creates 'Label' widget for Language and uses place() method.
        label_6=Label(root,text="Language",width=20,font=('bold',10))
        label_6.place(x=75,y=330)


        #the variable 'var1' mentioned here holds Integer Value, by default 0
        var1=IntVar()
        #this creates Checkbutton widget and uses place() method.
        Checkbutton(root,text="English", variable=var1).place(x=230,y=330)


        #the variable 'var2' mentioned here holds Integer Value, by default 0
        var2=IntVar()
        Checkbutton(root,text="German", variable=var2).place(x=290,y=330)

        #this creates button for submitting the details provides by the user
        Button(root, text='Submit' , width=20,bg="black",fg='white').place(x=180,y=380)
        default_blank_space(root)
        
        root.mainloop() 

