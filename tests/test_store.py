from src.store import *
from tests.test_data import *

def test_new_store():
    store = Store(load_from_file=False)
    assert type(store) == Store

def test_load_store():
    store = Store(load_from_file=True)
    assert type(store) == Store

