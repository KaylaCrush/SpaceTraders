from src.api import *
from src.models import System
#from src.display.flaskinterface import app
from multiprocessing import Process, Value
import src.orm as orm
import src.db as db

system = get_system_data('OE')
classy_system = orm.build_from_record(System, system)

#store = Store()
breakpoint()
#app.run(debug=True)