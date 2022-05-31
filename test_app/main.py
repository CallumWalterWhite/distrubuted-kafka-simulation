from packages.tkinter import *
from views import *

def main():
    _window = Tk()
    _window.geometry("1280x1050")
    HomeView().view(_window)

if __name__ == '__main__':
    main()
