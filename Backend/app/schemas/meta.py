from pydantic import BaseModel

class Meta(BaseModel):
    result:str
    message:str

    def __init__(self, message:str, result:str="OK"):
        super().__init__(message=message, result=result)
        self.result = result
        self.message = message
    
    