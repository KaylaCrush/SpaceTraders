from src.api import *
from src.store import *
from src.models import *
from src.display.flaskinterface import app
from multiprocessing import Process, Value

store = Store()
#breakpoint()
app.run(debug=True)