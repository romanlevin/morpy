"""
Cooridinate system is x, y - going from the top left corner to the bottom
right.
"""

import itertools
import textwrap
from collections import namedtuple
from frozendict import frozendict

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
    """
    A generator of all possible coordinates in a `dimensions`-sized board.
    """
    d_x, d_y = dimensions
    yield from (Coordinate(x=x, y=y) for x, y in
                itertools.product(range(d_x), range(d_y)))


def get_positions(dimensions, pieces_to_place):
    """
    A generator of all possible positions given `dimensions` and `pieces_to_place`.

    `pieces_to_place` is a string of piece types - eg '♔♔♖' will place two kings and
    a rook on the board.
    """
    checked_boards = set()
    coordinates = get_coordinates(dimensions)
    position_coords = itertools.permutations(coordinates, len(pieces_to_place))
    for coords in position_coords:
        board = frozendict(zip(coords, pieces_to_place))
        if board in checked_boards:
            continue
        checked_boards.add(board)
        yield Position(board=board, dimensions=dimensions)


def draw_position(position):
    """
    Prints a graphical representation of `position`.
    """
    board = position.board
    dimensions = position.dimensions
    array = ''.join(
        board.get(coordinate, '□') for coordinate in
        get_coordinates(dimensions))
    print(textwrap.fill(array, dimensions.x, drop_whitespace=False))


def filter_coordinates(coordinates, dimensions):
    """
    Filters iterable `coordinates` from all members who are outisde of `dimensions`.
    """
    return filter(lambda coord: 0 <= coord.x < dimensions.x and 0 <= coord.y < dimensions.y, coordinates)


def rank_and_file(piece):
    """
    Generates all squares on the same rank and file as `piece`.
    """
    dimensions = piece.board_dimensions
    coord = piece.coordinate
    yield from (
        Coordinate(x=x, y=y)
        for x, y in itertools.chain(
            ((coord.x, y) for y in range(dimensions.y) if y != coord.y),
            ((x, coord.y) for x in range(dimensions.x) if x != coord.x),
        ))


def diagonals(piece):
    """
    Generates all squares on the same diagonals as `piece`.
    """
    dimensions = piece.board_dimensions
    coord = piece.coordinate
    directions = itertools.product((1, -1), repeat=2)
    for d_x, d_y in directions:
        new_coord = Coordinate(coord.x + d_x, coord.y + d_y)
        while 0 <= new_coord.x < dimensions.x and 0 <= new_coord.y < dimensions.y:
            yield new_coord
            new_coord = Coordinate(x=new_coord.x + d_x, y=new_coord.y + d_y)


def get_attacked_coordinates(piece):
    """
    Takes a PlacedPiece object and returns a set of all positions it attacks.
    """
    dimensions = piece.board_dimensions
    coord = piece.coordinate
    piece_type = piece.type

    if piece_type == KING:
        potential_attacked = (
            Coordinate(x=coord.x + d_x, y=coord.y + d_y)
            for d_x, d_y in itertools.product((-1, 0, 1), repeat=2)
            if not (d_x == 0 and d_y == 0))
        attacked = set(filter_coordinates(potential_attacked, dimensions))

    elif piece_type == QUEEN:
        attacked = set(itertools.chain(diagonals(piece), rank_and_file(piece)))

    elif piece_type == BISHOP:
        attacked = set(diagonals(piece))

    elif piece_type == KNIGHT:
        potential_attacked = (
            Coordinate(x=coord.x + s_x * d_x, y=coord.y + s_y * d_y)
            for s_x, s_y in itertools.product((-1, 1), repeat=2)
            for d_x, d_y in ((1, 2), (2, 1))
            )
        attacked = set(filter_coordinates(potential_attacked, dimensions))

    elif piece_type == ROOK:
        attacked = set(rank_and_file(piece))

    return attacked


def is_position_valid(position):
    """
    Are all pieces in `position` independent?
    """
    placed_pieces = (
        PlacedPiece(piece_type, coords, position.dimensions)
        for coords, piece_type in position.board.items())
    attacked_coordinates = {coords for piece in placed_pieces for coords in get_attacked_coordinates(piece)}
    return not any(coord in position.board for coord in attacked_coordinates)


def get_valid_positions(dimensions, pieces):
    for position in get_positions(dimensions, pieces):
        if is_position_valid(position):
            yield position


if __name__ == '__main__':
    # X, Y, PIECES = 3, 3, 2 * KING + ROOK
    # for position in get_valid_positions(Dimensions(X, Y), PIECES):
    #     draw_position(position)
    #     print('-' * X)

    X, Y, PIECES = 7, 7, 2 * KING + 2 * QUEEN + 2 * BISHOP + KNIGHT
    print(len(tuple(get_valid_positions(Dimensions(X, Y), PIECES))))
