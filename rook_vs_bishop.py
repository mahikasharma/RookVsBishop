"""Design outline for classes and functions:

BOARD HELPER FUNCTIONS:
  1) new_board(): return an empty 8x8 list-of-lists filled with '.'
  2) build_board(bishop_pos, rook_pos): return board with 'B' and 'R' placed at respective positions

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

# importing random for the coin tosses and dice rolls
import random  
# representing the chess file letters as a string
FILES = "abcdefgh" 

# Create an empty 8x8 board matrix filled with '.'
def new_board() -> list[list[str]]:
    return [["." for _ in range(8)] for _ in range(8)]

# Build a board for the current positions of the bishop and rook
def build_board(bishop_pos: "Position", rook_pos: "Position") -> list[list[str]]:
    board = new_board()
    board[bishop_pos.rank][bishop_pos.file] = "B"
    board[rook_pos.rank][rook_pos.file] = "R"
    return board

# For visualizing the board in the terminal 
def print_board(bishop_pos: "Position", rook_pos: "Position") -> None:
    header = "    " + " ".join(list(FILES))
    print(header)
    print("   " + "-" * (2 * 8 - 1))
    # iterating through ranks 8 to 1
    for r in range(7, -1, -1):  
        row_cells = []
        board = build_board(bishop_pos, rook_pos)
        # iterating through files a to h
        for f in range(8): 
            row_cells.append(board[r][f])
        print(f"{r+1} | " + " ".join(row_cells))
    print()

class Position:
    # Represents a square on the board as starting from 0 (file, rank)
    def __init__(self, file: int, rank: int):
        self.file = file  
        self.rank = rank  

    def to_notation(self):
        # Convert coordinates to chess notation like (2,2) -> 'c3'
        return f"{FILES[self.file]}{self.rank + 1}"

    # Static method to make a position from text like 'c3' (no instance needed)
    @staticmethod
    def from_notation(sq):
        # Convert chess notation like 'c3' to zero-based Position
        return Position(FILES.index(sq[0]), int(sq[1]) - 1)

    def on_same_diagonal(self, other: "Position") -> bool:
        # Bishop moves diagonally, so equal absolute differences mean they're on the same diagonal
        return abs(self.file - other.file) == abs(self.rank - other.rank)


class Bishop:
    # bishop (that is stationary) is initialized at a chess square
    def __init__(self, square: str):
        self.position = Position.from_notation(square)

    def can_capture(self, target: Position) -> bool:
        # Bishop can capture if the target lies on the same diagonal and is not the same square
        file_diff = abs(self.position.file - target.file)
        rank_diff = abs(self.position.rank - target.rank)
        return file_diff == rank_diff and file_diff > 0


class Rook:
    # Rook that moves up or right with a wrap-around
    def __init__(self, square: str):
        self.position = Position.from_notation(square)

    def move(self, direction: str, steps: int) -> None:
        # Move the rook by 'steps'/squares; wrap around using modulo (%) 8 
        if direction == "up":
            self.position.rank = (self.position.rank + steps) % 8
        else:  # "right"
            self.position.file = (self.position.file + steps) % 8

    def can_capture(self, target: Position) -> bool:
        # Rook can capture if target is on the same file (column) or same rank (row)
        return (self.position.file == target.file or self.position.rank == target.rank)


def play(bishop_square="c3", rook_square="h1", rounds=15, seed: int | None = None, show_board: bool = True) -> str:
    # Play the game and print the board at the start and after each round 
    # Optional parameter 'seed' for reproducing the same run
    if seed is not None:
        random.seed(seed)  

    bishop = Bishop(bishop_square)  
    rook = Rook(rook_square)     

    # Initial positions of bisho pand rook
    print(f"Start: bishop={bishop.position.to_notation()}, rook={rook.position.to_notation()}")  
    if show_board:
        print_board(bishop.position, rook.position)

    # Iterate through each round
    for r in range(1, rounds + 1):  
        # H = up, T = right
        coin = "H" if random.random() < 0.5 else "T" 
        # Sum of 2 dice
        steps = random.randint(1, 6) + random.randint(1, 6)  
        # Translating coin to direction
        direction = "up" if coin == "H" else "right" 

        # Move the rook with wrap-around
        rook.move(direction, steps)  
        print(f"Round {r}: coin={coin}, dice={steps}, rook={rook.position.to_notation()}")  
        if show_board:
            print_board(bishop.position, rook.position)

        # Check if rook lands on bishop's square (if so, rook captures bishop)
        if rook.position.file == bishop.position.file and rook.position.rank == bishop.position.rank:
            print("Result: Rook captured the bishop. Rook wins.")
            return "rook"

        # Check if bishop can capture rook
        if bishop.can_capture(rook.position):  
            print("Result: Bishop can capture the rook. Bishop wins.")
            return "bishop"

    print("Result: Rook survived {} rounds. Rook wins.".format(rounds))  
    return "rook"


if __name__ == "__main__":  
    play()  