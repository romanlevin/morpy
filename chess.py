import itertools

PIECES = {
    'K': 'rules',
    'Q': 'rules',
    'B': 'rules',
    'N': 'rules',
    'R': 'rules',
}


def get_coordinates(x, y):
    return itertools.product(range(x), range(y))


def get_positions(x, y, pieces):
    coordinates = get_coordinates(x, y)
    return itertools.permutations(coordinates, pieces)

# print(tuple(get_coordinates(2, 2)))
print(tuple(get_positions(2, 2, 1)))
