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


    def update(self):
        self.upload()
    

    def add_or_change(self, key, value):
        self.buffer[key] = value


    def get(self, item, default=None):
        return self.buffer.get(item, default)


    def clean_for_user(self, user_id):
        if type(user_id) == int:
            user_id = str(user_id)
        for key in self.buffer.copy().keys():
            if key.startswith(user_id):
                self.buffer.pop(key)


    def __setitem__(self, key, value):
        self.buffer[key] = value


    def __getitem__(self, key):
        return self.buffer[key]


    def __del__(self):
        self.save()

    
def clean_buffer(user_id):
    buffer = Buffer()
    for key in buffer.buffer.copy().keys():
        if key.startswith(str(user_id)):
            buffer.buffer.pop(key)


# buffer = Buffer()
