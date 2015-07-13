import chess


def test_attacked_positions_king():
    piece_type = chess.KING
    dimensions = chess.Dimensions(x=3, y=3)
    coords = chess.Coordinate(x=1, y=1)
    placed_piece = chess.PlacedPiece(
        type=piece_type, coordinate=coords, board_dimensions=dimensions)
    attacked_positions = chess.get_attacked_positions(placed_piece)
    expected = {chess.Coordinate(x, y) for x, y in ((0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2))}
    assert attacked_positions == expected


def test_attacked_positions_king_in_corner():
    piece_type = chess.KING
    dimensions = chess.Dimensions(x=3, y=3)
    coords = chess.Coordinate(x=0, y=0)
    placed_piece = chess.PlacedPiece(
        type=piece_type, coordinate=coords, board_dimensions=dimensions)
    attacked_positions = chess.get_attacked_positions(placed_piece)
    expected = {chess.Coordinate(x, y) for x, y in ((0, 1), (1, 0), (1, 1))}
    assert attacked_positions == expected


def x_test_attacked_positions_queen_in_corner():
    piece_type = chess.QUEEN
    dimensions = chess.Dimensions(x=3, y=3)
    coords = chess.Coordinate(x=0, y=0)
    placed_piece = chess.PlacedPiece(
        type=piece_type, coordinate=coords, board_dimensions=dimensions)
    attacked_positions = chess.get_attacked_positions(placed_piece)
    expected = {chess.Coordinate(x, y) for x, y in ((0, 1), (0, 2), (1, 0), (2, 0), (1, 1), (2, 2))}
    assert attacked_positions == expected


def test_attacked_positions_bishop_in_corner():
    piece_type = chess.BISHOP
    dimensions = chess.Dimensions(x=3, y=3)
    coords = chess.Coordinate(x=0, y=0)
    placed_piece = chess.PlacedPiece(
        type=piece_type, coordinate=coords, board_dimensions=dimensions)
    attacked_positions = chess.get_attacked_positions(placed_piece)
    expected = {chess.Coordinate(x, y) for x, y in ((1, 1), (2, 2))}
    assert attacked_positions == expected


def test_attacked_positions_rook_in_corner():
    piece_type = chess.ROOK
    dimensions = chess.Dimensions(x=3, y=3)
    coords = chess.Coordinate(x=0, y=0)
    placed_piece = chess.PlacedPiece(
        type=piece_type, coordinate=coords, board_dimensions=dimensions)
    attacked_positions = chess.get_attacked_positions(placed_piece)
    expected = {chess.Coordinate(x, y) for x, y in ((0, 1), (0, 2), (1, 0), (2, 0))}
    assert attacked_positions == expected


def test_attacked_positions_knight_in_corner():
    piece_type = chess.KNIGHT
    dimensions = chess.Dimensions(x=3, y=3)
    coords = chess.Coordinate(x=0, y=0)
    placed_piece = chess.PlacedPiece(
        type=piece_type, coordinate=coords, board_dimensions=dimensions)
    attacked_positions = chess.get_attacked_positions(placed_piece)
    expected = {chess.Coordinate(x, y) for x, y in ((2, 1), (1, 2))}
    assert attacked_positions == expected


def test_get_valid_positions_3_by_3_two_kings_one_rook():
    Coordinate = chess.Coordinate
    dimensions = chess.Dimensions(3, 3)
    pieces = 2 * chess.KING + chess.ROOK
    positions = chess.get_valid_positions(dimensions, pieces)
    position_1 = chess.Position(
        {
            Coordinate(0, 1): chess.ROOK,
            Coordinate(2, 0): chess.KING,
            Coordinate(2, 2): chess.KING,
        },
        dimensions)
    position_2 = chess.Position(
        {
            Coordinate(1, 0): chess.ROOK,
            Coordinate(0, 2): chess.KING,
            Coordinate(0, 2): chess.KING,
        },
        dimensions)
    position_3 = chess.Position(
        {
            Coordinate(1, 2): chess.ROOK,
            Coordinate(0, 0): chess.KING,
            Coordinate(0, 2): chess.KING,
        },
        dimensions)
    position_4 = chess.Position(
        {
            Coordinate(2, 1): chess.ROOK,
            Coordinate(0, 0): chess.KING,
            Coordinate(0, 2): chess.KING,
        },
        dimensions)
    expected = (position_1, position_2, position_3, position_4)
    for position in positions:
        assert position in expected
    for e in expected:
        assert e in positions
