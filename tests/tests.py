from morpy import morpy
from morpy.frozendict import frozendict


def test_attacked_positions_king():
    piece_type = morpy.KING
    dimensions = morpy.Dimensions(x=3, y=3)
    coords = morpy.Coordinate(x=1, y=1)
    placed_piece = morpy.PlacedPiece(
        type=piece_type, coordinate=coords, board_dimensions=dimensions)
    attacked_coordinates = morpy.get_attacked_coordinates(placed_piece)
    expected = {morpy.Coordinate(x, y) for x, y in ((0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2))}
    assert attacked_coordinates == expected


def test_attacked_positions_king_in_corner():
    piece_type = morpy.KING
    dimensions = morpy.Dimensions(x=3, y=3)
    coords = morpy.Coordinate(x=0, y=0)
    placed_piece = morpy.PlacedPiece(
        type=piece_type, coordinate=coords, board_dimensions=dimensions)
    attacked_coordinates = morpy.get_attacked_coordinates(placed_piece)
    expected = {morpy.Coordinate(x, y) for x, y in ((0, 1), (1, 0), (1, 1))}
    assert attacked_coordinates == expected


def x_test_attacked_positions_queen_in_corner():
    piece_type = morpy.QUEEN
    dimensions = morpy.Dimensions(x=3, y=3)
    coords = morpy.Coordinate(x=0, y=0)
    placed_piece = morpy.PlacedPiece(
        type=piece_type, coordinate=coords, board_dimensions=dimensions)
    attacked_coordinates = morpy.get_attacked_coordinates(placed_piece)
    expected = {morpy.Coordinate(x, y) for x, y in ((0, 1), (0, 2), (1, 0), (2, 0), (1, 1), (2, 2))}
    assert attacked_coordinates == expected


def test_attacked_positions_bishop_in_corner():
    piece_type = morpy.BISHOP
    dimensions = morpy.Dimensions(x=3, y=3)
    coords = morpy.Coordinate(x=0, y=0)
    placed_piece = morpy.PlacedPiece(
        type=piece_type, coordinate=coords, board_dimensions=dimensions)
    attacked_coordinates = morpy.get_attacked_coordinates(placed_piece)
    expected = {morpy.Coordinate(x, y) for x, y in ((1, 1), (2, 2))}
    assert attacked_coordinates == expected


def test_attacked_positions_rook_in_corner():
    piece_type = morpy.ROOK
    dimensions = morpy.Dimensions(x=3, y=3)
    coords = morpy.Coordinate(x=0, y=0)
    placed_piece = morpy.PlacedPiece(
        type=piece_type, coordinate=coords, board_dimensions=dimensions)
    attacked_coordinates = morpy.get_attacked_coordinates(placed_piece)
    expected = {morpy.Coordinate(x, y) for x, y in ((0, 1), (0, 2), (1, 0), (2, 0))}
    assert attacked_coordinates == expected


def test_attacked_positions_knight_in_corner():
    piece_type = morpy.KNIGHT
    dimensions = morpy.Dimensions(x=3, y=3)
    coords = morpy.Coordinate(x=0, y=0)
    placed_piece = morpy.PlacedPiece(
        type=piece_type, coordinate=coords, board_dimensions=dimensions)
    attacked_coordinates = morpy.get_attacked_coordinates(placed_piece)
    expected = {morpy.Coordinate(x, y) for x, y in ((2, 1), (1, 2))}
    assert attacked_coordinates == expected


def test_get_valid_positions_3_by_3_two_kings_one_rook():
    Coordinate = morpy.Coordinate
    dimensions = morpy.Dimensions(3, 3)
    pieces = 2 * morpy.KING + morpy.ROOK
    positions = morpy.get_valid_positions(dimensions, pieces)
    position_1 = morpy.Position(
        frozendict({
            Coordinate(0, 1): morpy.ROOK,
            Coordinate(2, 0): morpy.KING,
            Coordinate(2, 2): morpy.KING,
        }),
        dimensions)
    position_2 = morpy.Position(
        frozendict({
            Coordinate(1, 0): morpy.ROOK,
            Coordinate(0, 2): morpy.KING,
            Coordinate(2, 2): morpy.KING,
        }),
        dimensions)
    position_3 = morpy.Position(
        frozendict({
            Coordinate(1, 2): morpy.ROOK,
            Coordinate(0, 0): morpy.KING,
            Coordinate(2, 0): morpy.KING,
        }),
        dimensions)
    position_4 = morpy.Position(
        frozendict({
            Coordinate(2, 1): morpy.ROOK,
            Coordinate(0, 0): morpy.KING,
            Coordinate(0, 2): morpy.KING,
        }),
        dimensions)
    expected = (position_1, position_2, position_3, position_4)
    assert set(expected) == set(positions)


def test_get_valid_positions_3_by_3_two_kings_one_rook_iter():
    Coordinate = morpy.Coordinate
    dimensions = morpy.Dimensions(3, 3)
    pieces = 2 * morpy.KING + morpy.ROOK
    positions = morpy.get_positions_iter(dimensions, pieces)
    position_1 = morpy.Position(
        frozendict({
            Coordinate(0, 1): morpy.ROOK,
            Coordinate(2, 0): morpy.KING,
            Coordinate(2, 2): morpy.KING,
        }),
        dimensions)
    position_2 = morpy.Position(
        frozendict({
            Coordinate(1, 0): morpy.ROOK,
            Coordinate(0, 2): morpy.KING,
            Coordinate(2, 2): morpy.KING,
        }),
        dimensions)
    position_3 = morpy.Position(
        frozendict({
            Coordinate(1, 2): morpy.ROOK,
            Coordinate(0, 0): morpy.KING,
            Coordinate(2, 0): morpy.KING,
        }),
        dimensions)
    position_4 = morpy.Position(
        frozendict({
            Coordinate(2, 1): morpy.ROOK,
            Coordinate(0, 0): morpy.KING,
            Coordinate(0, 2): morpy.KING,
        }),
        dimensions)
    expected = (position_1, position_2, position_3, position_4)
    assert set(expected) == set(positions)
