DATABASE = {
    "metals": [
        {
        "id": 1,
        "metal": "Sterling Silver",
        "price": 12.42
        },
        {
        "id": 2,
        "metal": "14K Gold",
        "price": 736.4
        },
        {
        "id": 3,
        "metal": "24K Gold",
        "price": 1258.9
        },
        {
        "id": 4,
        "metal": "Platinum",
        "price": 795.45
        },
        {
        "id": 5,
        "metal": "Palladium",
        "price": 1241
        }
    ],
    "orders": [
        {
            "id": 1,
            "metalId": 3,
            "sizeId": 2,
            "styleId": 3,
            "timestamp": 1614659931693
        },
        {
            "id": 2,
            "metalId": 2,
            "sizeId": 2,
            "styleId": 2,
            "timestamp": 1614659931694
        }
    ],
    "sizes": [
        {
            "id": 1, 
            "carats": 0.5, 
            "price": 405 
        },
        {
            "id": 2, 
            "carats": 0.75, 
            "price": 782 
        },
        {
            "id": 3, 
            "carats": 1, 
            "price": 1470 
        },
        {
            "id": 4, 
            "carats": 1.5, 
            "price": 1997 
        },
        {
            "id": 5, 
            "carats": 2, 
            "price": 3638 
        }
    ],
    "styles": [
        {
            "id": 1,
            "style": "Classic",
            "price": 500 
        },
        {
            "id": 2,
            "style": "Modern",
            "price": 710 
        },
        {
            "id": 3,
            "style": "Vintage",
            "price": 965 
        }
    ]
 }

def expand(key, data):
    resource = key[:-2]+"s"
    matching_data = retrieve(resource, data[key], "")
    new_key = key[:-2]
    data[new_key] = matching_data
    del data[key]

def addPrice(data, foreign_keys):
    total = 0
    # for key in ["metal", "size", "style"]:
    #     total += data[key]["price"]

    for key in foreign_keys:
        resource = key[:-2]+"s"
        matching_data = retrieve(resource, data[key], "")
        total += matching_data["price"]
        
    data["price"] = round(total, 2)

def all(resource):
    """For GET requests to collection"""
    return DATABASE[resource]

def retrieve(resource, id, query_params):
    """For GET requests to a single resource"""
    requested_data = None

    for data in DATABASE[resource]:
        if data["id"] == id:
            requested_data = data

            if resource == "orders":
                foreign_keys = ["metalId", "sizeId", "styleId"]

                addPrice(requested_data, foreign_keys)

                if "expand" in query_params:
                    for key in foreign_keys:
                        expand(key, requested_data)

    return requested_data

def create(resource, new_data):
    """For POST requests to a collection"""
    max_id = DATABASE[resource][-1]["id"]
    new_id = max_id + 1
    new_data["id"] = new_id
    DATABASE[resource].append(new_data)
    return new_data

def update(resource, id, edited_data):
    """For PUT requests to a single resource"""
    for index, data in enumerate(DATABASE[resource]):
        if data["id"] == id:
            DATABASE[resource][index] = edited_data
            break

def delete(resource, id):
    """For DELETE requests to a single resource"""
    data_index = -1

    for index, data in enumerate(DATABASE[resource]):
        if data["id"] == id:
            data_index = index

        if data_index >= 0:
            DATABASE[resource].pop(data_index)