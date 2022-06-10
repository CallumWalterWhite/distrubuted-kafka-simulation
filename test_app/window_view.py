from tkinter import *
from tkinter import messagebox
from core.protocol.model.message_type import *
from core.protocol.tcp.sender import Sender

class WindowViewer():
    def __init__(self):
        self.root = Tk()
        self.root.geometry("1920x1080")
        self.root.title("Test Application")
        self.root.configure(background='lightblue')
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind('<Escape>', self.on_closing)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

    def home(self):
        self.clear()
        Label(text="Welcome to message broker test application", width="300", height="2", font=("Calibri", 13)).pack() 
        self.default_blank_space()
        def __createMenuOption(text, callback):
            Button(self.root, text=text, width=20, height=5, command=callback).pack()
        def __go_stresser():
            self.stresser()
        def __go_settings():
            self.settings()
        def __check_cluster_status():
            msg = 'Cluster is running' if self.check_cluster_status() else 'Cluster is not running'
            messagebox.showinfo(title='Status', message=msg)
        __createMenuOption("Stress tool", __go_stresser)
        self.default_blank_space()
        __createMenuOption("Settings", __go_settings)
        self.default_blank_space()
        __createMenuOption("Check cluster", __check_cluster_status)
        self.default_blank_space()
        self.root.mainloop()
    
    def settings(self):
        self.clear()
        Label(text="Test app consumer settings", width="300", height="2", font=("Calibri", 13)).pack() 

        def __go_home():
            self.home()

        top_widget_frame = Frame(self.root)
        top_widget_frame.pack(side='left', anchor=NW)
        Button(top_widget_frame, text='Back', command=__go_home).pack()
        
        self.default_blank_space()
        Label(consumer_frame,text="Add Consumer - ", width=20,font=("bold",10)).pack()
        consumer_frame = Frame(self.root)
        consumer_frame.pack(side="top")
        Label(consumer_frame,text="Consumer group name", width=20,font=("bold",10)).pack()
        consumer_group_name_entry=Entry(consumer_frame)
        consumer_group_name_entry.pack()
        
        
        self.default_blank_space()
        consumer_frame_list = Frame(self.root)
        consumer_frame_list.pack(side="top")
        Label(consumer_frame_list,text="Consumers - ", width=20,font=("bold",10)).pack()
        consumers_listbox = Listbox(consumer_frame_list)
        consumers_listbox.insert(1, "Python")
        consumers_listbox.pack()

        self.default_blank_space()
        self.root.mainloop()
    
    def stresser(self):
        self.clear()
        Label(text="Test app stresser tool", width="300", height="2", font=("Calibri", 13)).pack() 

        def __go_home():
            self.home()

        top_widget_frame = Frame(self.root)
        top_widget_frame.pack(side='left', anchor=NW)
        Button(top_widget_frame, text='Back', command=__go_home).pack()
        
        self.default_blank_space()

        frame = Frame(self.root)
        frame.pack(side="top")
        cluster_info = self.get_cluster_info()
        topics = self.get_topics(cluster_info)
        Label(frame,text="Topic",width=20,font=("bold",10)).pack()
        print(topics)
        list_of_country=[ 'India' ,'US' , 'UK' ,'Germany' ,'Austria']
        c=StringVar()
        droplist=OptionMenu(frame,c, *list_of_country)
        droplist.config(width=15)
        c.set('Choose a topic...')
        droplist.pack()

        label_0 =Label(frame,text="Stress tool", width=20,font=("bold",20)).pack()
        label_1 =Label(frame,text="FullName", width=20,font=("bold",10)).pack()
        entry_1=Entry(frame).pack()
        label_3 =Label(frame,text="Email", width=20,font=("bold",10)).pack()
        entry_3=Entry(frame).pack()
        label_4 =Label(frame,text="Gender", width=20,font=("bold",10)).pack()
        var=IntVar()
        Radiobutton(frame,text="Male",padx= 5, variable= var, value=1).pack()
        Radiobutton(frame,text="Female",padx= 20, variable= var, value=2).pack()
        label_5=Label(frame,text="Country",width=20,font=("bold",10)).pack()
        label_6=Label(frame,text="Language",width=20,font=('bold',10)).pack()
        var1=IntVar()
        Checkbutton(frame,text="English", variable=var1).pack()


        var2=IntVar()
        Checkbutton(frame,text="German", variable=var2).pack()

        Button(frame, text='Submit' , width=20,bg="black",fg='white').pack()
        self.default_blank_space()
        
        self.root.mainloop() 

    def default_blank_space(self):
        Label(self.root, text="", background='lightblue').pack()

    def clear(self):
        _list = self.root.winfo_children()
        for item in _list:
            if item.winfo_children():
                _list.extend(item.winfo_children())
        for item in _list:
            item.pack_forget()
        self.reset()

    def reset(self):
        self.root.configure(background='lightblue')

    def check_cluster_status(self):
        try:
            sender: Sender = Sender('127.0.0.1', 2500)
            response = sender.send(Message(HEALTH_CHECK, {
                }))
            if response['status'] == 'ok':
                return True
        except:
            return False
        return False

    def get_cluster_info(self):
        cluster_info = None
        try:
            sender: Sender = Sender('127.0.0.1', 2500)
            response = sender.send(Message(GET_CLUSTER_INFO, {
                }))
            cluster_info = response
        except Exception as e:
            print(e)
        return cluster_info

    def get_topics(self, cluster_info):
        topics = [x["topic_id"] for x in cluster_info]
        unique_topics = []
        for topic in list(set(topics)):
            unique_topics.append([x for x in cluster_info if x["topic_id"] == topic][0])
        return unique_topics