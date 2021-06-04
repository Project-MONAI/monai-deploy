class StateService:
    _instance = None
   
    @staticmethod 
    def get_instance():
      """ Static access method. """
      if StateService._instance == None:
         StateService()
      return StateService._instance
    
    def __init__(self):
      """ Virtually private constructor. """
      if StateService._instance != None:
        raise Exception("This class is a singleton!")
      else:
        StateService._instance = self
        StateService._instance.storage = {}

    
    def store(self, key, val):
        self.storage[key] = val

    def retrieve(self, key):
        return self.storage[key]
    