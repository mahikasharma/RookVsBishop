import unittest

from rook_vs_bishop import Position, Bishop, Rook, play


class TestPosition(unittest.TestCase):
    # Verify that converting from chess notation to Position and back is lossless
    def test_notation_roundtrip(self):
        p = Position.from_notation("c3")
        self.assertEqual(p.to_notation(), "c3")

    # Roundtrip test for all 64 squares
    def test_notation_roundtrip_all_board(self):
        files = "abcdefgh"
        for f in files:
            for r in range(1, 9):
                sq = f"{f}{r}"
                self.assertEqual(Position.from_notation(sq).to_notation(), sq)


class TestBishop(unittest.TestCase):
    # Bishop should capture along diagonals but not purely horizontal/vertical
    def test_bishop_capture_on_diagonal(self):
        b = Bishop("c3")
        self.assertTrue(b.can_capture(Position.from_notation("g7")))  # same diagonal
        self.assertFalse(b.can_capture(Position.from_notation("a3")))  # same rank, not diagonal

    # Check multiple diagonal targets from c3
    def test_bishop_diagonals_full_from_c3(self):
        b = Bishop("c3")
        true_targets = ["a1", "b2", "d4", "e5", "f6", "g7", "h8", "a5", "b4", "d2", "e1"]
        for sq in true_targets:
            with self.subTest(sq=sq):
                self.assertTrue(b.can_capture(Position.from_notation(sq)))
        false_targets = ["c3", "c4", "d3", "h1", "a8"]
        for sq in false_targets:
            with self.subTest(sq=sq):
                # c3 equals bishop square; play() handles equality before diagonal
                self.assertEqual(b.can_capture(Position.from_notation(sq)), sq != "c3" and sq in true_targets)


class TestRook(unittest.TestCase):
    # Rook captures on same file or rank; not on unrelated squares
    def test_rook_can_capture(self):
        r = Rook("h1")
        # Same file (column)
        self.assertTrue(r.can_capture(Position.from_notation("h8")))
        # Same rank (row)
        self.assertTrue(r.can_capture(Position.from_notation("a1")))
        # Neither
        self.assertFalse(r.can_capture(Position.from_notation("c3")))

    # Moving right from 'h' should wrap around to 'a'
    def test_rook_wrap_right(self):
        r = Rook("h1")
        r.move("right", 1)  # h -> a
        self.assertEqual(r.position.to_notation(), "a1")

    # Moving up from rank 8 should wrap around to rank 1
    def test_rook_wrap_up(self):
        r = Rook("h8")
        r.move("up", 1)  # 8 -> 1
        self.assertEqual(r.position.to_notation(), "h1")

    # Wrapping with large step counts (greater than 8)
    def test_rook_wrap_large_steps(self):
        r = Rook("a1")
        r.move("right", 15)  # 15 mod 8 = 7 → a -> h
        self.assertEqual(r.position.to_notation(), "h1")
        r = Rook("a1")
        r.move("up", 16)  # 16 mod 8 = 0 → stays on same rank
        self.assertEqual(r.position.to_notation(), "a1")


class TestSimulation(unittest.TestCase):
    # Smoke test: with a seed, the simulation should run and return a valid winner
    def test_play_smoke_with_seed(self):
        # Just ensure it returns a valid winner and doesn't crash
        winner = play(seed=42)
        self.assertIn(winner, {"rook", "bishop"})

    # Zero rounds: rook automatically survives and wins
    def test_play_zero_rounds_rook_survives(self):
        winner = play(rounds=0, seed=1)
        self.assertEqual(winner, "rook")


if __name__ == "__main__":
    unittest.main()


