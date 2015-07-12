import itertools
import textwrap

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


def get_boards(x, y, pieces=''):
    pieces = sorted(pieces)
    positions = get_positions(x, y, len(pieces))
    for position in positions:
        board = {
            coordinate: piece for coordinate, piece in zip(position, pieces)}
        yield board


def draw_board(board, x, y):
    array = ''.join(
        board.get(coordinate, '□') for coordinate in get_coordinates(x, y))
    print(textwrap.fill(array, x, drop_whitespace=False))

# print(tuple(get_coordinates(2, 2)))
# print(tuple(get_positions(2, 2, 1)))
X, Y, PIECES = 2, 2, '♕'
for board in get_boards(X, Y, PIECES):
    draw_board(board, X, Y)
    print('-' * X)
