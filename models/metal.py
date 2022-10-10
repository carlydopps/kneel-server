class Metal():

    # Class initializer. It has 5 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, metal, price):
        self.id = id
        self.metal = metal
        self.price = price