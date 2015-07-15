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


def cache_attack_map(f):
    cache = {}

    def wrapper(piece):
        result = cache.get(piece.coordinate)
        if not result:
            result = f(piece)
            cache[piece.coordinate] = result
        return result

    return wrapper


def get_coordinates(dimensions):
    """
    A generator of all possible coordinates in a `dimensions`-sized board.
    """
    d_x, d_y = dimensions
    yield from (Coordinate(x=x, y=y) for x, y in
                itertools.product(range(d_x), range(d_y)))


def get_positions_iter(dimensions, pieces_to_place):
    """
    Iteratively generate all valid positions for `dimensions` and `pieces_to_place`.
    """
    # Populate intial valid positions by placing the first piece at each of the coordinates
    coordinates = tuple(get_coordinates(dimensions))
    last_pass = {
        Position(board=frozendict({coords: pieces_to_place[1]}), dimensions=dimensions) for coords in coordinates
    }
    current_pass = set()

    for piece in pieces_to_place[1:]:
        # For each valid position already found, find all valid position that also include `piece`.
        for position in last_pass:
            attacked_in_position = attacked_coordinates_in_position(position)
            for coords in coordinates:
                if coords in position.board or coords in attacked_in_position:
                    continue
                placed_piece = PlacedPiece(piece, coords, dimensions)
                attacked_by_piece = get_attacked_coordinates(placed_piece)
                if set(attacked_by_piece) & set(position.board.keys()):
                    continue
                board = {coords: piece}
                board.update(position.board)
                frozen_board = frozendict(board)
                new_position = Position(frozen_board, dimensions)
                current_pass.add(new_position)
        last_pass, current_pass = current_pass, set()
    return last_pass


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


def rank_and_file_iter(piece):
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


@cache_attack_map
def rank_and_file(piece):
    return set(rank_and_file_iter(piece))


def diagonals_iter(piece):
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


@cache_attack_map
def diagonals(piece):
    return set(diagonals_iter(piece))


@cache_attack_map
def knight_moves(piece):
    coord = piece.coordinate
    dimensions = piece.board_dimensions
    potential_attacked = (
        Coordinate(x=coord.x + s_x * d_x, y=coord.y + s_y * d_y)
        for s_x, s_y in itertools.product((-1, 1), repeat=2)
        for d_x, d_y in ((1, 2), (2, 1))
        )
    return set(filter_coordinates(potential_attacked, dimensions))


@cache_attack_map
def king_moves(piece):
    coord = piece.coordinate
    dimensions = piece.board_dimensions
    potential_attacked = (
        Coordinate(x=coord.x + d_x, y=coord.y + d_y)
        for d_x, d_y in itertools.product((-1, 0, 1), repeat=2)
        if not (d_x == 0 and d_y == 0))
    return set(filter_coordinates(potential_attacked, dimensions))


@cache_attack_map
def queen_moves(piece):
    return diagonals(piece) | rank_and_file(piece)


def get_attacked_coordinates(piece):
    """
    Takes a PlacedPiece object and returns a set of all positions it attacks.
    """
    piece_type = piece.type

    if piece_type == KING:
        attacked = king_moves(piece)

    elif piece_type == QUEEN:
        attacked = queen_moves(piece)

    elif piece_type == BISHOP:
        attacked = diagonals(piece)

    elif piece_type == KNIGHT:
        attacked = knight_moves(piece)

    elif piece_type == ROOK:
        attacked = rank_and_file(piece)

    return attacked


def attacked_coordinates_in_position(position):
    placed_pieces = (
        PlacedPiece(piece_type, coords, position.dimensions)
        for coords, piece_type in position.board.items())
    attacked_coordinates = {coords for piece in placed_pieces for coords in get_attacked_coordinates(piece)}
    return attacked_coordinates


def is_position_valid(position):
    """
    Are all pieces in `position` independent?
    """
    attacked_coordinates = attacked_coordinates_in_position(position)
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

    # X, Y, PIECES = 5, 5, 2 * KING + 1 * QUEEN + 1 * BISHOP
    X, Y, PIECES = 7, 7, 2 * KING + 2 * QUEEN + 2 * BISHOP + KNIGHT
    # X, Y, PIECES = 6, 6, 2 * ROOK + 4 * KNIGHT
    # print(len(tuple(get_valid_positions(Dimensions(X, Y), PIECES))))
    print(len(tuple(get_positions_iter(Dimensions(X, Y), PIECES))))
