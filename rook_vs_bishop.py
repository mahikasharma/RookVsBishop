"""Design outline for classes and functions:

PRINT_BOARD (UTILITY):
  1) print_board(bishop_pos, rook_pos) for visualization of the board

POSITION:
  1) __init__(file, rank): store column/row (calling it file/rank for chess terminology)
  2) to_notation(): convert (file, rank) -> 'c3'
  3) from_notation(sq): convert 'c3' -> (file, rank)
  4) on_same_diagonal(other): bishop-style diagonal check

BISHOP:
  1) __init__(square): set starting square
  2) can_capture(target): true if target is on same diagonal (and not the same square)

ROOK:
  1) __init__(square): set starting square
  2) move(direction, steps): move 'up' or 'right' with modulo-8 wrapping
  3) can_capture(target): same file or same rank

PLAY (FUNCTION):
  1) Accepts bishop_square, rook_square, rounds, seed
  2) Simulates coin toss + dice roll per round
  3) Moves rook with wrap-around
  4) Checks immediate outcomes (rook-on-bishop, bishop-diagonal)
  5) Logs each round and returns winner
"""