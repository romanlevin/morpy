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
