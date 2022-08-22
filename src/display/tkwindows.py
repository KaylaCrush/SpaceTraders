
import tkinter as tk
from tkinter import ttk
from src.store import Store
from src.api import get_location_data

IMG_SIZE = 256
TEXT_HEIGHT = 20

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

# this window displays detailed information about something. is passed either a dictionary or list of dictionaries
class Window(tk.Toplevel):
  def __init__(self, parent, data:dict|list[dict], title:str = '', width = 600, image:str = None):
    super().__init__(parent)
    self.data = data
    #text_height = max(len(data)*TEXT_HEIGHT + TEXT_HEIGHT, 300)
    #self.geometry(f'{width}x{text_height}')
    self.title(title)
    self.image(image) if image else None
    self.configure(bg='#141414')
    self.resizable(0,0)
    #ttk.Button(self, text='Close', command=self.destroy).grid(column=1, row=0)
    

    #ttk.Button(self, text='Close', command=self.destroy).grid(column=1, row=0)
        

class ShipsWindow(Window):
  def __init__(self,parent, store:Store):
    data = store.ships
    super().__init__(parent, data, title='Ships', width=800)
  

class LocationWindow(Window):
  def __init__(self,parent, store:Store, location_id = 'OE-PM'):
    data = [location for location in store.locations if location.symbol == location_id][0]
    super().__init__(parent, data = data, title=location_id, width=800)
    self.myData = get_location_data(location_id)
    self.title(location_id)
    self.resizable(0,0)
    
    self.python_image = tk.PhotoImage(file=f'data/img/locations/{location_id}.png')
    ttk.Label(self, image=self.python_image).pack(padx=(300-256)/2,side='left')
    #tk.Label(self, text=nice_location_name(self.myData), bg='#141414', fg='white', width=300, pady=20).pack()
    #tk.Label(self, text = )
    #ttk.Label(self, text = location_id)




class RootMenu(tk.Tk):
    def __init__(self, store):
        super().__init__()
        self.store = store

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
        window = Window(self, store=self.store)
        #window.grab_set()

    def open_ships_window(self):
        window = ShipsWindow(self, store=self.store)

    def open_locations_window(self):
        window = LocationWindow(self, store=self.store, location_id='OE-PM') ## TODO: This is temporary to test the planet window.

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
        ttk.Button(frame, text='OE-PM', command=self.open_locations_window).grid(column=0, row=2)
        
        ttk.Button(frame, text='Quit', command=self.destroy).grid(column=1, row=2)

        for widget in frame.winfo_children():
            widget.grid(padx=10,pady=10)
        return frame

if __name__ == "__main__":
    app = RootMenu()
    app.mainloop()
