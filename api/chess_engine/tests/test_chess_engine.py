import unittest
import chess
from core.board import Board

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_initial_board(self):
        self.assertEqual(self.board.board.fen(), chess.STARTING_FEN)

    def test_make_move(self):
        self.board.make_move("e2e4")
        self.assertEqual(self.board.board.piece_at(chess.E4), chess.Piece(chess.PAWN, chess.WHITE))
        self.assertIsNone(self.board.board.piece_at(chess.E2))

    def test_illegal_move(self):
        with self.assertRaises(ValueError):
            self.board.make_move("e2e5")

    def test_undo_move(self):
        self.board.make_move("e2e4")
        self.board.undo_move()
        self.assertEqual(self.board.board.fen(), chess.STARTING_FEN)

    def test_generate_moves(self):
        moves = self.board.generate_moves()
        self.assertEqual(len(moves), 20)  # There are 20 possible moves in the starting position

    def test_is_game_over(self):
        self.assertFalse(self.board.is_game_over())
        # Set up a checkmate position
        self.board.set_fen("7k/5Q2/5K2/8/8/8/8/8 b - - 0 1")
        self.assertTrue(self.board.is_game_over())

    def test_evaluate(self):
        # Test the initial position (should be close to balanced)
        initial_eval = self.board.evaluate()
        print(f"Initial position evaluation: {initial_eval}")
        self.assertAlmostEqual(initial_eval, 0, delta=100)  # Allow for some bias

        # Make a move and test again
        self.board.move_piece("e2e4")
        after_move_eval = self.board.evaluate()
        print(f"Evaluation after e2e4: {after_move_eval}")
        self.assertGreater(after_move_eval, 0)  # Should be positive (White's advantage)

        # Set up a position where White is ahead
        self.board.set_fen("rnbqkbnr/pppp1ppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
        white_advantage_eval = self.board.evaluate()
        print(f"Evaluation with White advantage: {white_advantage_eval}")
        self.assertLess(white_advantage_eval, 0)  # Should be negative (Black's perspective)

        # Set up a position where Black is ahead
        self.board.set_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1")
        black_advantage_eval = self.board.evaluate()
        print(f"Evaluation with Black advantage: {black_advantage_eval}")
        self.assertLess(black_advantage_eval, 0)  # Should be negative (White's perspective)

        # Test a more complex position
        self.board.set_fen("r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R w KQkq - 4 4")
        complex_eval = self.board.evaluate()
        print(f"Evaluation of complex position: {complex_eval}")
        self.assertAlmostEqual(complex_eval, 0, delta=100)  # Should be roughly balanced

    def test_set_fen(self):
        test_fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"
        self.board.set_fen(test_fen)
        self.assertEqual(self.board.board.fen(), test_fen)

    def test_push_uci(self):
        self.board.push_uci("e2e4")
        self.assertEqual(self.board.board.piece_at(chess.E4), chess.Piece(chess.PAWN, chess.WHITE))
        self.assertIsNone(self.board.board.piece_at(chess.E2))

if __name__ == '__main__':
    unittest.main()
