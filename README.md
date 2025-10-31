# Rook Vs. Bishop

This file explains my solution for the programming problem Rook vs. Bishop. The goal is to simulate a simplified chess scenario where a stationary bishop at c3 and a rook starting at h1 interact over 15 turns based on random movement rules. The rook moves each round based on a coin toss and a roll of two six-sided dice. If the toss is heads, the rook moves "up"; if tails, it moves "right." The dice sum determines the number of squares moved. The board wraps around at the edges. If the rook lands exactly on c3, it wins. If it ever lands on the bishop's diagonal, the bishop wins. If neither happens after 15 rounds, the rook wins by surviving.

The overview of my solution involves my design approach, my data structure, my language choice, as well as the pros and cons for each:

## Design approach

I followed a test-driven development approach. Before writing the main logic, I created a test file and wrote unit tests based on the instructions, including edge cases such as wrap-around movement and diagonal detection. Once I wrote my tests, I then implemented the classes and functions. This approach helped keep the logic clean, and it made debugging easier since I could immediately validate each component as I built it.

I began by writing a docstring outline to structure the design. This helps me think through object responsibilities before writing code. Below is the outline I started with, which guided the implementation:
```
Design outline for classes and functions:

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
```

As I coded, I made small adjustments. For instance, I added a print_board function once I realized a visual representation would help me verify correctness during development. I also kept all functions and classes flexible by using parameters rather than hard-coding values, even though the original problem had fixed piece positions. This makes the simulation more reusable and easier to test.

I loosely followed an MVC-style pattern: the Position, Rook, and Bishop classes represent the model; the play() function acts as the controller coordinating logic and state changes; and printed output serves as a simple view.

**Pros:** I believe that this design choice keeps the game logic and piece behavior clearly separated. It also made unit testing easier since the piece movements and board logic are isolated.

**Cons:** My code implementation is mutable, where an object's attributes (like position) are directly modified. With an immutable state, it would return a new state instead of modifying one state, there would be less room for errors with helper functions that could unintentionally modify the state, and would also be easier to track the state history.

## Data structure

I represented the chess board as an 8×8 list of lists. I found this structure to be intuitive for representing index squares, updating piece positions, and printing the board state. It also aligns well with a grid-based game and supports wrap-around logic in a straightforward way.

**Pros:** A list of lists was easy to visualize and print to the console. Accessing the 'board' with row and column indices was straightforward, as well as updating the location after a round.

**Cons:** A list of lists to represent a full board wasn't exactly necessary, since only two positions needed to be tracked. A simpler coordinate-based approach (storing file/rank tuples without initializing a whole board matrix) would have been more minimal and memory-efficient. However, since the difference in time complexity wasn't significant, I chose this structure to make the program easier to read, reason about, and extend, rather than optimizing for the smallest possible representation.

## Language choice

I chose Python because it is the language I am most comfortable writing quickly and clearly in. Here are the pros and cons I debated before ultimately choosing python:

**Pros:** The syntax is simple for lists, classes, and random number generation, making it easier to focus on the game logic for me. Python's unittest framework also made it straightforward to implement my choice of a test-driven approach.

**Cons:** Python has dynamic typing, where a variable is determined at the runtime and not before execution. This means that type errors appear during the execution and not before the run. A language like Java can detect type errors before the program runs. Since there weren't many different variable types I had to work with in this code, I ultimately chose Python.

## Other details to note

I used file and rank terminology to match chess conventions and keep the code aligned with the context of the problem. I also wrote the simulation to accept optional parameters such as number of rounds and a random seed so the game can be reproduced and extended beyond the fixed assignment rules.

## How to run

In the terminal, run:
```bash
python rook_vs_bishop.py
```