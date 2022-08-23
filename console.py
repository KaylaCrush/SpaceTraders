from src.api import *
from src.store import *
from src.models import *
from src.display.flaskinterface import app

store = Store()
app.run(debug=True)