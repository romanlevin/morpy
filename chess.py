from itertools import permutations

PIECES = {
    'K': 'rules',
    'Q': 'rules',
    'B': 'rules',
    'N': 'rules',
    'R': 'rules',
}


def get_positions(self, x, y, **pieces):
    """
    Iterates over all possible positions.
    Each position is a tuple.

    x, y - board dimensions
    pieces - mapping of piece type to amount (eg. {'K': 2, 'B': 1})
    """
    if not all(piece in PIECES for piece in pieces):
        raise TypeError('Invalid piece type')

    pieces_string = ''.join(k * v for k, v in pieces.items())

    empty_squares = x * y - len(pieces_string)
    if empty_squares < 0:
        raise ValueError('Too many pieces')

    pieces_string += ' ' * empty_squares
    return permutations(pieces_string)
