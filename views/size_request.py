SIZES = [
    { "id": 1, "carats": 0.5, "price": 405 },
    { "id": 2, "carats": 0.75, "price": 782 },
    { "id": 3, "carats": 1, "price": 1470 },
    { "id": 4, "carats": 1.5, "price": 1997 },
    { "id": 5, "carats": 2, "price": 3638 }
]

def get_all_sizes():
    return SIZES

def get_single_size(id):
    # Variable to hold the found size, if it exists
    requested_size = None

    # Iterate the sizeS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for size in SIZES:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if size["id"] == id:
            requested_size = size

    return requested_size