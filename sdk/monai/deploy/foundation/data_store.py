class DataStore:
    _instance = None
   
    @staticmethod 
    def get_instance():
      """ Static access method. """
      if DataStore._instance == None:
         DataStore()
      return DataStore._instance
    
    def __init__(self):
      """ Virtually private constructor. """
      if DataStore._instance != None:
        raise Exception("This class is a singleton!")
      else:
        DataStore._instance = self
        DataStore._instance.storage = {}

    
    def store(self, key, val):
        self.storage[key] = val

    def retrieve(self, key):
        return self.storage[key]
    