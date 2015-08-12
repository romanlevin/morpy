#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
Cooridinate system is x, y - going from the top left corner to the bottom
right.
"""

from __future__ import print_function, unicode_literals
import itertools
from collections import namedtuple
from .frozendict import frozendict
import argparse

KING, QUEEN, BISHOP, KNIGHT, ROOK = '♔♕♗♘♖'

Coordinate = namedtuple('Coordinate', ['x', 'y'])
Dimensions = namedtuple('Dimensions', ['x', 'y'])
Position = namedtuple('Position', ['board', 'dimensions'])
PlacedPiece = namedtuple('PlacedPiece', ['type', 'coordinate', 'board_dimensions'])


def cache_attack_map(f):
    """
    A decorator that memoizes attack map functions.
    """
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
    Return a tuple of all possible coordinates in a `dimensions`-sized board.
    """
    d_x, d_y = dimensions
    return tuple(Coordinate(x=x, y=y) for x in range(d_x) for y in range(d_y))


def attacked_coordinates_in_position(position):
    """
    Return a set of all `coordinate`s that are attacked in `position`.
    """
    placed_pieces = (
        PlacedPiece(piece_type, coords, position.dimensions)
        for coords, piece_type in position.board.items())
    attacked_coordinates = {coords for piece in placed_pieces for coords in get_attacked_coordinates(piece)}
    return attacked_coordinates


def get_positions_iter(dimensions, pieces_to_place):
    """
    Generate all valid positions for `dimensions` and `pieces_to_place`.
    """
    # Populate intial valid positions by placing the first piece at each of the coordinates
    coordinates = get_coordinates(dimensions)
    last_pass = {
        Position(board=frozendict({coords: pieces_to_place[0]}), dimensions=dimensions) for coords in coordinates
    }
    current_pass = set()

    for piece in pieces_to_place[1:]:
        # For each valid position already found, find all valid position that also include `piece`.
        for position in last_pass:
            attacked_in_position = attacked_coordinates_in_position(position)
            for coords in coordinates:
                # Are these coordinates already attacked or occupied?
                if coords in position.board or coords in attacked_in_position:
                    continue
                placed_piece = PlacedPiece(piece, coords, dimensions)
                attacked_by_piece = get_attacked_coordinates(placed_piece)
                # Does the piece at this position attack any of the other pieces?
                if set(attacked_by_piece) & set(position.board.keys()):
                    continue
                board = {coords: piece}
                board.update(position.board)
                frozen_board = frozendict(board)
                new_position = Position(frozen_board, dimensions)
                current_pass.add(new_position)
        last_pass, current_pass = current_pass, set()
    return last_pass


def filter_coordinates(coordinates, dimensions):
    """
    Filter iterable `coordinates` from all members who are outisde of `dimensions`.
    """
    return filter(lambda coord: 0 <= coord.x < dimensions.x and 0 <= coord.y < dimensions.y, coordinates)


@cache_attack_map
def rank_and_file(piece):
    """
    Return a set of all `coordinate`s on the same rank and file as `piece`.
    """
    dimensions = piece.board_dimensions
    coord = piece.coordinate
    return set(
        Coordinate(x=x, y=y)
        for x, y in itertools.chain(
            ((coord.x, y) for y in range(dimensions.y) if y != coord.y),
            ((x, coord.y) for x in range(dimensions.x) if x != coord.x),
        ))


def diagonals_iter(piece):
    """
    Generate all `coordinate`s on the same diagonals as `piece`.
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
    """
    Return a set of all `coordinate`s on the same diagonals as `piece`.
    """
    return set(diagonals_iter(piece))


@cache_attack_map
def knight_moves(piece):
    """
    Return a set of all `coordinate`s a knight's move away from `piece`.
    """
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
    """
    Return a set of all `coordinate`s a king's move away from `piece`.
    """
    coord = piece.coordinate
    dimensions = piece.board_dimensions
    potential_attacked = (
        Coordinate(x=coord.x + d_x, y=coord.y + d_y)
        for d_x, d_y in itertools.product((-1, 0, 1), repeat=2)
        if not (d_x == 0 and d_y == 0))
    return set(filter_coordinates(potential_attacked, dimensions))


@cache_attack_map
def queen_moves(piece):
    """
    Return a set of all `coordinate`s a queens's move away from `piece`.
    """
    return diagonals(piece) | rank_and_file(piece)


def get_attacked_coordinates(piece):
    """
    Return a set of all positions attacked by `PlacePiece` `piece`.
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


def parse():
    """
    Create CLI parser, and parse arugments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('N', type=int, help='First board dimension')
    parser.add_argument('M', type=int, help='Second board dimension')
    parser.add_argument('--kings', type=int, metavar='n', default=0, help='Number of king pieces to place on the board')
    parser.add_argument('--queens', type=int, metavar='n', default=0, help='Number of queen pieces to place on the board')
    parser.add_argument('--bishops', type=int, metavar='n', default=0, help='Number of bishop pieces to place on the board')
    parser.add_argument('--knights', type=int, metavar='n', default=0, help='Number of knight pieces to place on the board')
    parser.add_argument('--rooks', type=int, metavar='n', default=0, help='Number of rook pieces to place on the board')
    parser.add_argument('--print-pieces', action='store_true', help='Print the pieces to be placed on the board')
    return parser.parse_args()


def main():
    """
    Handle all CLI I/O.
    """
    args = parse()
    dimensions = Dimensions(args.N, args.M)
    pieces = args.kings * KING + args.queens * QUEEN + args.bishops * BISHOP
    pieces += args.knights * KNIGHT + args.rooks * ROOK
    if args.print_pieces:
        print(pieces)
    print(len(get_positions_iter(dimensions, pieces)))

if __name__ == '__main__':
    main()
