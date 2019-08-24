import pickle

class Buffer:
    filetosave = "buffer"
    buffer = {}


    def __init__(self):
        self.upload()


    def save(self):
        with open(self.filetosave, 'wb') as file:
            pickle.dump(self.buffer, file)
    
    
    def upload(self):
        try:
            with open(self.filetosave, 'rb') as file:
                self.buffer = pickle.load(file)
        except FileNotFoundError:
            self.buffer = {}
    

    def __del__(self):
        self.save()