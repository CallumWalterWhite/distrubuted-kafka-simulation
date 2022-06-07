from tkinter import *
from views import *

def main():
    _window = Tk()
    _window.geometry("500x500")
    HomeView().view(_window)

if __name__ == '__main__':
    main()
