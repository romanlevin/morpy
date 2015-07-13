"""
Cooridinate system is x, y - going from the top left corner to the bottom
right.
"""

import itertools
import textwrap
from collections import namedtuple

KING, QUEEN, BISHOP, KNIGHT, ROOK = '♔♕♗♘♖'
PIECES = {
    KING: 'rules',
    QUEEN: 'rules',
    BISHOP: 'rules',
    KNIGHT: 'rules',
    ROOK: 'rules',
}

Coordinate = namedtuple('Coordinate', ['x', 'y'])
Dimensions = namedtuple('Dimensions', ['x', 'y'])
Position = namedtuple('Position', ['board', 'dimensions'])
PlacedPiece = namedtuple('PlacedPiece', ['type', 'coordinate', 'board_dimensions'])


def get_coordinates(dimensions):
    d_x, d_y = dimensions
    return (Coordinate(x=x, y=y) for x, y in
            itertools.product(range(d_x), range(d_y)))


def get_positions(dimensions, pieces_to_place):
    coordinates = get_coordinates(dimensions)
    position_coords = itertools.permutations(coordinates, len(pieces_to_place))
    for coords in position_coords:
        board = dict(zip(coords, pieces_to_place))
        yield Position(board=board, dimensions=dimensions)


def draw_position(position):
    board = position.board
    dimensions = position.dimensions
    array = ''.join(
        board.get(coordinate, '□') for coordinate in
        get_coordinates(dimensions))
    print(textwrap.fill(array, dimensions.x, drop_whitespace=False))


X, Y, PIECES = 2, 2, QUEEN + ROOK
for position in get_positions(Dimensions(X, Y), PIECES):
    draw_position(position)
    print('-' * X)
