from src.api import *
from src.spacebase import *
import tkinter as tk
from tkinter import ttk
import folium
from branca.element import Figure


IMG_SIZE = 256

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

        self.geometry('600x300')
        self.title('Toplevel Window')
        self.configure(bg='#141414')

        #ttk.Button(self, text='Close', command=self.destroy).grid(column=1, row=0)
        

class ShipsWindow(Window):
    def __init__(self,parent):
        super().__init__(parent)
        self.myData = get_ships()
        self.title('Ships')
        self.resizable(0,0)

class LocationWindow(Window):
    def __init__(self,parent, location_id = 'OE-PM'):
        super().__init__(parent)
        self.myData = get_location_data(location_id)
        self.title(location_id)
        self.resizable(0,0)
        
        self.python_image = tk.PhotoImage(file=f'data/img/locations/{location_id}.png')
        ttk.Label(self, image=self.python_image).pack(padx=(300-256)/2,side='left')
        tk.Label(self, text=nice_location_name(self.myData), bg='#141414', fg='white', width=300, pady=20).pack()
        #tk.Label(self, text = )
        #ttk.Label(self, text = location_id)




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
        window = LocationWindow(self, 'OE-PM') ## TODO: This is temporary to test the planet window.

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
            widget.grid(padx=5,pady=5)
        return frame

if __name__ == "__main__":
    app = RootMenu()
    app.mainloop()



class StarMap():
  def __init__(self, starchart):
    self.starfield_url="http://paulbourke.net/miscellaneous/astronomy/8192x4096.png"
    self.figure_size=800
    self.icon_ids = {'PLANET':'fa-globe', 'MOON':'fa-moon-o', 'ASTEROID':'fa-cog', 'GAS_GIANT':'fa-circle-o', 'WORMHOLE':'fa-recycle'}
    self.icon_colors = {'PLANET':'lightblue', 'MOON':'beige', 'ASTEROID':'gray', 'GAS_GIANT':'lightgreen', 'WORMHOLE':'pink'}
  
    self.starchart = starchart
   
    self.oas = self.getOffsetAndScale()
    self.fig = Figure(width=self.figure_size,height=self.figure_size)

  # functions to normalize coordinates for displaying with the star map function
  def getOffsetAndScale(self):
    coords=self.starchart.getCoords()
    x_max = max([coord[0] for coord in coords])
    x_min = min([coord[0] for coord in coords])
    y_max = max([coord[1] for coord in coords])
    y_min = min([coord[1] for coord in coords])
    x_offset = (x_max+x_min)/2 
    y_offset = (y_max+y_min)/2

    x_distance = abs(x_max-x_min)
    y_distance = abs(y_max-y_min)
    scale=(.25*self.figure_size)/max([x_distance, y_distance])

    return[x_offset,y_offset,scale]
  
  def normalizeCoord(self, coord):
    x_offset = self.oas[0]
    y_offset = self.oas[1]
    scale = self.oas[2]
    x = (coord[0]-x_offset)*scale
    y = (coord[1]-y_offset)*scale
    return [x,y]

  def generate_starmap_label(self, location):
    location_details=f'''{location.getType().title()} {location.getId()}: "{location.getName()}" '''
    trait_details = '<br>'.join([" ".join(trait.split('_')).title() for trait in location.getTraits()])
    if location.hasMarketData():
      market_data = location.getMarketData()
      goods_string = "<br>".join([f"""{' '.join(good['symbol'].split('_')).title()}:<br>&emsp;{good['quantityAvailable']} Available<br> &emsp;p/s price: {good['purchasePricePerUnit']}/{good['sellPricePerUnit']}<br>""" for good in market_data])
      market_details = f"<br><center>Market Report:</center><br>{goods_string}"
    else:
      market_details = ""
    return f'<center>{location_details}<br>{trait_details}</center>{market_details}'

  def draw_starmap(self):
    m= folium.Map(crs='Simple', zoom_control=False, tiles=None)
    
    for location in self.starchart.getLocationsList():
      html = self.generate_starmap_label(location)
      html_lines = html.count("<br>")
      frame_height = 30+(20*(html_lines))
      iframe = folium.IFrame(html,height=frame_height,width=275)

      popup = folium.Popup(iframe, max_width=700)

      coord=self.normalizeCoord(location.getXY())
      icon = self.icon_ids[location.getType()]
      icon_color = self.icon_colors[location.getType()]
 
      folium.Marker(coord,
                    tooltip=location.getName(), 
                    popup=popup,
                    icon=folium.Icon(color='black', icon_color=icon_color, icon=icon, prefix='fa')
                    ).add_to(m)

    overlay_size = self.figure_size

    starmap_overlay = folium.raster_layers.ImageOverlay(bounds=[[-overlay_size,-overlay_size],[overlay_size,overlay_size]],
                                                        image=self.starfield_url).add_to(m)
    self.fig.add_child(m)
    return m