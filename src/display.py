from api import *
import tkinter as tk
from tkinter import ttk

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class Window(tk.Toplevel):
    
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('300x100')
        self.title('Toplevel Window')

        ttk.Button(self,
                text='Close',
                command=self.destroy).grid(column=0, row=0)
        

class ShipsWindow(Window):
    def __init__(self,parent):
        super().__init__(parent)
        self.myData = get_ships()
        self.title('Ships')
        self.resizable(0,0)


class RootMenu(tk.Tk):
    def __init__(self):
        super().__init__()

        #self.geometry('300x200')
        self.title('Space Traders')
        self.resizable(0,0)

        # place a button on the root window
        # ttk.Button(self,
        #         text='Open a window',
        #         command=self.open_window).pack(expand=True)

        input_frame = self.create_button_frame(self)
        input_frame.grid(column=0, row=0)



    def open_window(self):
        window = Window(self)
        #window.grab_set()

    def open_ships_window(self):
        window = ShipsWindow(self)

    def open_locations_window(self):
        pass

    def open_markets_window(self):
        pass

    def open_market_window(self):
        pass

    def create_button_frame(self, container):
        frame = ttk.Frame(container, padding=10)
        #frame.columnconfigure(0, weight = 1)
        #frame.columnconfigure(0, weight = 1)

        ttk.Button(frame, text='Ships', command=self.open_ships_window).grid(column=0, row=0)
        ttk.Button(frame, text='Locations', command=self.open_ships_window).grid(column=1, row=0)
        ttk.Button(frame, text='Markets', command=self.open_ships_window).grid(column=0, row=1)
        ttk.Button(frame, text='Quit', command=self.destroy).grid(column=1, row=1)

        for widget in frame.winfo_children():
            widget.grid(padx=5,pady=5)
        return frame

if __name__ == "__main__":
    app = RootMenu()
    app.mainloop()