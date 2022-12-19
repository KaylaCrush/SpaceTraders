class Generic:
    def __init__(self, 
    first_id:str = None, 
    second_id:str = None, 
    data:dict = None, 
    store = None,
    data_function = None, 
    update_function = None):

        # data_function is called when opject is initalized with no data
        # update_function is called when object is updated
        self.data_function = data_function if data_function else None
        self.update_function = update_function if update_function else data_function

        # if data is provided, populate self from the data
        if data: self.__dict__.update(data)

        # if no data is provided, call the data_function to get the data, if it exists
        elif self.data_function:
            if first_id:
                if second_id:
                    self.__dict__.update(data_function(first_id, second_id))
                else:
                    self.__dict__.update(data_function(first_id))
        else:
            raise Exception('No data or data_function provided')

        # if store is provided, add self to the store
        if store:
            self.store = store
            if self.__class__.__name__ == 'User':
                self.store.__dict__['user'] = self
            else:
                self.store.__dict__[self.__class__.__name__.lower() + 's'].append(self) # fancy way to get the class name

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
