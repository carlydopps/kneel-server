class Order():

    # Class initializer. It has 5 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, metalId, sizeId, styleId, typeId, timestamp):
        self.id = id
        self.metalId = metalId
        self.sizeId = sizeId
        self.styleId = styleId
        self.typeId = typeId
        self.timestamp = timestamp