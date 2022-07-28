from src.spacebase import *
from test.test_data import *

def test_nice_location_name():
    assert nice_location_name(sample_location) == """ Planet PL-II: "Planet II" """
