from branca.element import Figure
import folium
from src.store import Store

class StarMap():
  def __init__(self, store):
    self.starfield_url="http://paulbourke.net/miscellaneous/astronomy/8192x4096.png"
    self.figure_size=800
    self.icon_ids = {'PLANET':'fa-globe', 'MOON':'fa-moon-o', 'ASTEROID':'fa-cog', 'GAS_GIANT':'fa-circle-o', 'WORMHOLE':'fa-recycle'}
    self.icon_colors = {'PLANET':'lightblue', 'MOON':'beige', 'ASTEROID':'gray', 'GAS_GIANT':'lightgreen', 'WORMHOLE':'pink'}
  
    self.store = store
   
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