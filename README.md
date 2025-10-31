# RookVsBishop
My solution for the technical Assignment (Rook Vs. Bishop). 

## Overview
This repository implements a simplified chess simulation with two pieces:
- A stationary white bishop on `c3`
- A black rook starting on `h1`

Across 15 rounds, the rook moves for survival:
- Coin toss each round: Heads → move up; Tails → move right
- Roll 2d6; the sum is the number of squares moved
- Wrap-around: moving past the top wraps to rank 1; past file `h` wraps to `a`

After each rook move, outcomes are checked immediately:
- If the rook lands exactly on the bishop’s square (`c3`) → Rook wins
- Else if the rook lies on the bishop’s diagonal → Bishop wins
- Else continue to the next round

If there’s no capture after 15 rounds, the rook survives and wins.

## Language choice
Implemented in Python for fast iteration, readability, and built-in testing (`unittest`). It’s well-suited for small simulations and concise logging.

### My approach and thinking (in my own words)
- I chose a test-driven approach where I write all the tests and edge cases that my code needs to cover. After writing all the tests in `test_rook_vs_bishop.py`, I then started creating the class/function design in `rook_vs_bishop.py`.
- I optimized for clarity over cleverness. Once the basic assignment worked, I made the `play(...)` function accept parameters (`bishop_square`, `rook_square`, `rounds`, `seed`) so it’s easy to try other scenarios without changing the core logic.
- I kept the output simple (prints) so I can see the coin result, dice total, and rook position after every move.

## How to run
Run directly by path:

```bash
python3 /Users/mahika/Documents/RookVsBishop/rook_vs_bishop.py
```

From the project directory:

```bash
cd /Users/mahika/Documents/RookVsBishop
python3 rook_vs_bishop.py
```

Deterministic (reproducible) run with a seed:

```bash
python3 -c "import rook_vs_bishop as g; g.play(seed=42)"
```

### Defaults vs. flexibility
The simulation uses assignment-friendly defaults (`bishop_square='c3'`, `rook_square='h1'`, `rounds=15`), but the `play(...)` function is generic. You can change starting squares or rounds without changing the code:

```python
import rook_vs_bishop as g

# Example: move the stationary bishop and change the rook start/rounds
g.play(bishop_square="d4", rook_square="a1", rounds=20, seed=7)
```

## How to test
Run unit tests:

```bash
cd /Users/mahika/Documents/RookVsBishop
python3 -m unittest
```

## Design
- Board representation: files `a–h` and ranks `1–8` mapped to zero-based indices `0–7`. Helpers convert to/from notation (e.g., `c3`).
- Classes:
  - `Position`: holds file/rank, notation conversion, diagonal check helper.
  - `Bishop`: stores position; `can_capture` checks diagonal (abs(dx) == abs(dy) and not same square).
  - `Rook`: stores position; `move` supports up/right with modulo-8 wrap-around; `can_capture` checks same file or same rank.
- Simulation: `play(rounds=15, seed=None)` runs the game loop, prints per-round logs, and returns the winner string (`"rook"` or `"bishop"`).

### Design pattern and data structures
- I loosely followed an MVC-ish separation:
  - Model: `Position`, `Bishop`, `Rook` hold state and rules (movement/capture checks).
  - Controller: `play(...)` runs the simulation, randomizes coin/dice, and applies rules.
  - View: `print` statements to show what happened each round.
- Data structures are intentionally simple:
  - `Position` is just two ints (`file`, `rank`) with helpers to convert to/from chess notation.
  - I use strings (like `"c3"`) at the edges and zero-based ints internally so the math stays clean.

### Naming note: file/rank vs row/col
Chess uses the terms **file** (column, `a–h`) and **rank** (row, `1–8`). The code uses file/rank to align with chess notation and make conversions like `c3` ↔ `(file=2, rank=2)` straightforward. If you prefer grid terms, you can mentally map: `file → column`, `rank → row`. This choice also matches common chess libraries and keeps notation helpers simple.

## Rules and assumptions
- Rook only moves up or right as dictated by the coin toss.
- Steps per move are the sum of two 6-sided dice.
- Wrap-around on files/ranks via modulo 8 arithmetic.
- Order of checks after each move:
  1) If rook lands on bishop’s square → Rook wins.
  2) Else if rook is on bishop’s diagonal → Bishop wins.
  3) Else continue.
- If no capture occurs in 15 rounds → Rook wins by survival.

## Pros
- Simple, readable OOP structure.
- Deterministic runs enabled by an optional seed.
- Comprehensive tests covering notation roundtrip, bishop diagonal logic, rook capture rules, wrap-around (including large steps), seeded simulation smoke test, and zero-round survival.

### Why Python (my reasoning)
- I chose Python as an object-oriented language mostly because it is my strongest language, it has built-in testing, and it’s quick to write and read. The syntax is clean, logging/printing is simple, and it’s great for this kind of small simulation.
- If I wanted to extend it, I could add CLI flags (`argparse`), use `pytest` for richer tests, or even a simple GUI with Tkinter/PyQt. For this challenge, a CLI felt right.

### Possible cons of Python (as I see it here)
- The cons of Python are that it’s not the fastest language (irrelevant here), dynamic typing means I lean on tests and type hints, and shipping a single binary can be more work (not needed here).

## Cons
- Minimal chess model tailored to the assignment (no other pieces, turns, or obstacles).
- Console logging only; no structured logs or CLI flags.
- Rook’s move set is problem-specific (up/right) rather than full chess movement.

## Possible extensions
- CLI options (rounds, seed, starting squares).
- Structured logs (CSV/JSON) or quiet/verbose modes.
- Generalize to a broader board/piece engine.
- Property-based testing for additional randomized coverage.

## File layout
- `rook_vs_bishop.py`: Core implementation and simulation entry point.
- `test_rook_vs_bishop.py`: Unit tests.

## Sample output
```
Start: bishop=c3, rook=h1
Round 1: coin=T, dice=7, rook=g1
Round 2: coin=H, dice=4, rook=g5
Round 3: coin=T, dice=12, rook=c5
Round 4: coin=T, dice=6, rook=a5
Result: Bishop can capture the rook. Bishop wins.
```

## My process, pros/cons, and struggles
- Process: I wrote tests first (notation roundtrip, bishop/rook capture rules, wrap-around, seeded simulation), then built the minimal `Position`/`Bishop`/`Rook`/`play` pieces, and finally generalized the entrypoint.
- Pros: high confidence from tests; clear separation of rules vs. orchestration; easy to extend and reason about.
- Cons: slightly more structure than an all-in-one script for a small problem.
- I also had to write functions to convert an internal position (like `2,2`) to what the game/user sees (`c3`) since internal indices start at 0.
- I also want to talk about the data structures I used and the design pattern I used: I loosely followed an MVC-style separation (Models: `Position`, `Bishop`, `Rook`; Controller: `play`; View: printed logs).

> Note on language choice alternatives: Java could also be a reasonable choice; it has robust GUI options (Swing/JavaFX). Python also has GUI options (Tkinter/PyQt). For this assignment, I kept it CLI-focused.

## Overview of my solution
At a high level, I model the board state and piece rules explicitly, then drive a small simulation loop that applies coin/dice randomness and checks results immediately after each rook move. The code keeps chess notation ("c3") at the edges and converts to zero-based coordinates internally for clear math and wrap-around.

## Pros and cons of my approach
### Approach and design pattern
- I followed a lightweight MVC-like separation:
  - Model: `Position`, `Bishop`, `Rook` encapsulate rules and state
  - Controller: `play(...)` orchestrates randomness and turn logic
  - View: simple textual `print` logs (and an optional `print_board(...)`)

### Test-driven workflow
- I began with tests in `test_rook_vs_bishop.py` (notation round-trip, bishop diagonals, rook capture rules, wrap-around, seeded runs), then implemented the minimal classes/functions to satisfy them.

### Why this over alternatives
- Pros:
  - Clear separation of concerns makes the rules easy to extend (more pieces, obstacles, validations).
  - Tests give fast feedback and confidence, especially with randomness.
  - Deterministic seeds make runs reproducible for debugging.
- Cons:
  - Slightly more structure than a single-script solution.
  - A textual view is basic compared to a GUI or rich CLI.

## Reasons for my language choice
- I chose Python because it is my strongest language and supports an object-oriented style that maps naturally to chess pieces and positions. Python’s standard library (`unittest`, `argparse`) and concise syntax make iteration fast.
- Alternatives:
  - Java (also OOP) could be attractive if a desktop GUI were a goal (Swing/JavaFX). It encourages stricter typing and can provide a polished UI sooner. The tradeoff is more boilerplate and slower iteration for a small simulation.
  - For this CLI-focused assignment, Python’s development speed and readability outweighed those downsides.

## Notation helpers (from and to)
- `Position.to_notation()` converts internal zero-based `(file, rank)` to human-readable chess squares like "c3".
- `Position.from_notation(sq)` parses strings like "c3" into internal coordinates.
- Keeping this conversion centralized avoids off-by-one mistakes and lets the rest of the code stay numeric and simple.

## My workflow details
- I start by writing an outline docstring listing the classes and functions I expect to need, and then refine as I implement.
- During development, I added `print_board(...)` specifically to visualize positions after each move so I could validate wrap-around and capture checks at a glance.

## Data structure discussion
I represent the board as an explicit 8×8 list-of-lists when rendering or visualizing, while the core logic works directly with `Position` objects.

### Pros
- Clarity/encapsulation: A concrete board state is explicit and easy to reason about or extend (e.g., adding obstacles, more pieces).
- Ease of rendering: Printing is a straightforward read of `board[r][f]`.
- Future features: Supports validations (e.g., occupancy checks), alternate renderers, or saving/loading game state.
- Locality of changes: Updating squares is O(1) and centralized.

### Cons
- Slight overhead: You build/read an 8×8 matrix each render; for a fixed board this is constant-time but adds minor constant cost vs directly appending symbols.
- Extra code maintenance: More helpers and state to keep consistent.
- Potential duplication: Logic (e.g., bishop/rook location) exists both in objects and the matrix unless carefully managed.

### Performance impact
- Asymptotics: Unchanged for a fixed 8×8. Rendering is O(64)=O(1) per round; the overall simulation remains O(R) for R rounds.
- Constant factors: The board matrix adds a tiny constant cost; not noticeable in this assignment.
