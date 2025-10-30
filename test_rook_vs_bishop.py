import unittest
from rook_vs_bishop import Position, Bishop, Rook, play


# Tests for Position: turning squares like 'c3' into numbers and back again
class TestPosition(unittest.TestCase):
    def test_notation_roundtrip(self):
        """Test #1: make sure a single square roundtrips 'c3' -> Position -> 'c3'"""
        p = Position.from_notation("c3")
        self.assertEqual(p.to_notation(), "c3")

    def test_notation_roundtrip_all_board(self):
        """Test #2: make sure all 64 squares roundtrip to/from notation correctly"""
        files = "abcdefgh"
        for f in files:
            for r in range(1, 9):
                sq = f"{f}{r}"
                self.assertEqual(Position.from_notation(sq).to_notation(), sq)


# Tests for Bishop: it captures only on diagonals from c3 (not straight lines)
class TestBishop(unittest.TestCase):
    def test_bishop_capture_on_diagonal(self):
        """Test #3: bishop captures on diagonals, not on same rank/file only"""
        b = Bishop("c3")
        self.assertTrue(b.can_capture(Position.from_notation("g7")))  
        self.assertFalse(b.can_capture(Position.from_notation("a3")))  

    def test_bishop_diagonals_full_from_c3(self):
        """Test #4: bishop at c3 can capture all diagonal targets and not non-diagonals"""
        b = Bishop("c3")
        true_targets = ["a1", "b2", "d4", "e5", "f6", "g7", "h8", "a5", "b4", "d2", "e1"]
        for sq in true_targets:
            with self.subTest(sq=sq):
                self.assertTrue(b.can_capture(Position.from_notation(sq)))
        false_targets = ["c3", "c4", "d3", "h1", "a8"]
        for sq in false_targets:
            with self.subTest(sq=sq):
                # checking c3 = bishop square, and that play() handles equality before diagonal
                self.assertEqual(b.can_capture(Position.from_notation(sq)), sq != "c3" and sq in true_targets)


# Tests for Rook: it captures on same row/column and wraps around the edges
class TestRook(unittest.TestCase):
    def test_rook_can_capture(self):
        """Test #5: rook captures on same file or same rank, not on unrelated squares"""
        r = Rook("h1")
        # Same file (column)
        self.assertTrue(r.can_capture(Position.from_notation("h8")))
        # Same rank (row)
        self.assertTrue(r.can_capture(Position.from_notation("a1")))
        # Neither
        self.assertFalse(r.can_capture(Position.from_notation("c3")))

    def test_rook_wrap_right(self):
        """Test #6: moving right from 'h' wraps to 'a' (modulo 8)"""
        r = Rook("h1")
        r.move("right", 1) 
        self.assertEqual(r.position.to_notation(), "a1")

    def test_rook_wrap_up(self):
        """Test #7: moving up from rank 8 wraps to rank 1 (modulo 8)"""
        r = Rook("h8")
        r.move("up", 1)  
        self.assertEqual(r.position.to_notation(), "h1")

    def test_rook_wrap_large_steps(self):
        """Test #8: wrap works for large steps (>= 8) for both directions"""
        r = Rook("a1")
        r.move("right", 15) 
        self.assertEqual(r.position.to_notation(), "h1")
        r = Rook("a1")
        r.move("up", 16) 
        self.assertEqual(r.position.to_notation(), "a1")


# Tests for the whole game: it runs, and valid winners are returned
class TestSimulation(unittest.TestCase):
    def test_play_smoke_with_seed(self):
        """Test #9: seeded simulation runs and returns either 'rook' or 'bishop'"""
        # returns a valid winner and doesn't crash
        winner = play(seed=42)
        self.assertIn(winner, {"rook", "bishop"})

    def test_play_zero_rounds_rook_survives(self):
        """Test #10: with zero rounds, rook survives automatically"""
        winner = play(rounds=0, seed=1)
        self.assertEqual(winner, "rook")


if __name__ == "__main__":
    unittest.main()


