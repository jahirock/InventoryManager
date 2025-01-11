class Meta(object):
    def __init__(self):
        self.result = "OK"
        self.message = ""
    
    def __init__(self, result:str, message:str):
        self.result = result
        self.message = message
    
    result:str
    message:str