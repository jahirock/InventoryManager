class Product(object):
    def __init__(self, name:str, price:float, stock:int = 0):
        self.name = name
        self.price = price
        self.stock = stock
    name: str
    price: float
    stock: int = 0