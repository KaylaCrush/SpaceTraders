from src.models.generic import Generic
from src.api import get_my_status
from settings import USERNAME

class User():
    def __init__(self, data = None, username = USERNAME, store = None):
        self.id = username
        self.data_function = get_my_status
        self.update_function = self.data_function
        self.store = store
        if data: self.update_from_data(data)
        else: self.update_from_api()

    def my_data(self): ## essentially a version of __dict__ that excludes the store and data functions, for saving purposes
        return {key:value for key, value in self.__dict__.items() if key not in ['store', 'data_function', 'update_function']}

    def locator(self): #returns whatever you feed into the data function to complete the api call
        return self.id  # this is the default behavior for most classes

    def update_from_api(self): # updates the object from the api
        self.__dict__.update(self.update_function(self.locator())) 
        return self.__dict__

    def update_from_data(self, data): # updates the object from a dictionary of data
        self.__dict__.update(data)
        return self.__dict__
