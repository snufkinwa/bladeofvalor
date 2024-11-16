import unittest
import numpy as np
import chess
from core import Board, CNNChessEngine

# A simple mock CNN model for testing
class MockCNNModel:
    def predict(self, X):
        # This mock model will just sum the features across the planes as a dummy prediction
        return np.sum(X, axis=(1, 2, 3)).reshape(-1, 1)

class TestCNNChessEngine(unittest.TestCase):
    def setUp(self):
        self.model = MockCNNModel()
        self.engine = CNNChessEngine(self.model)

    def test_evaluate_position(self):
        # Test the evaluation of the starting position
        self.engine.board = Board()
        eval = self.engine.evaluate_position()
        self.assertNotEqual(eval, 0)



    def test_get_best_move(self):
        # Test getting the best move from the starting position
        self.engine.board = Board()
        best_move = self.engine.get_best_move(depth=1)
        self.assertIsNotNone(best_move)
        
        # Ensure the move is legal
        self.assertIn(chess.Move.from_uci(best_move), self.engine.board.board.legal_moves)

    def test_search(self):
        # Test the search function
        self.engine.board = Board()

        def mock_evaluate_position():
            eval = self.engine.board.evaluate()
            print(f"Mock evaluation: {eval}")  # Add this debug print
            return eval

        self.engine.evaluate_position = mock_evaluate_position

        # Print the initial evaluation
        initial_eval = self.engine.board.evaluate()
        print(f"Initial board evaluation: {initial_eval}")

        # Run search and print the result
        eval = self.engine.search(depth=1)
        print(f"Search evaluation: {eval}")

        self.assertIsNotNone(eval)  # Ensure the search result is not None
        self.assertLess(abs(eval), 100)  # Adjust this threshold as needed

        # Make a move and check if the evaluation changes
        moves = self.engine.board.generate_moves()
        if moves:
            move = moves[0]
            self.engine.board.make_move(move)

            new_eval = self.engine.search(depth=1)
            print(f"Evaluation after move: {new_eval}")

            self.engine.board.undo_move()

            self.assertIsNotNone(new_eval)  # Ensure the search result is not None after a move
            self.assertNotEqual(new_eval, initial_eval)

    def test_minimax(self):
        # Test the minimax function
        self.engine.board = Board()

        def mock_evaluate_position():
            eval = self.engine.board.evaluate()
            print(f"Mock evaluation: {eval}")  # Add this debug print
            return eval

        self.engine.evaluate_position = mock_evaluate_position

        # Print the initial evaluation
        initial_eval = self.engine.board.evaluate()
        print(f"Initial board evaluation: {initial_eval}")

        # Run minimax and print the result
        eval = self.engine.minimax(depth=1, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
        print(f"Minimax evaluation: {eval}")

        # The initial position should be close to 0, but not necessarily exactly 0
        self.assertLess(abs(eval), 100)  # Adjust this threshold as needed

        # Make a move and check if the evaluation changes
        moves = self.engine.board.generate_moves()
        if moves:
            print(f"Available moves: {moves}")
            move = moves[0]
            print(f"Making move: {move}")
            self.engine.board.push_uci(move)

            # Get the FEN representation after the move
            fen_after_move = self.engine.board.board.fen()
            print("Position after move (FEN):")
            print(fen_after_move)

            print("Position after move (UCI):")
            print(move)

            new_eval = self.engine.minimax(depth=1, alpha=float('-inf'), beta=float('inf'), maximizing_player=False)
            print(f"Evaluation after move: {new_eval}")

            self.engine.board.undo_move()

            self.assertNotEqual(new_eval, initial_eval)
        else:
            print("No moves available")

    def test_board_to_3d_array(self):
        # Test the board_to_3d_array function
        self.engine = CNNChessEngine()
        board_3d = self.engine.board_to_3d_array()

        self.assertEqual(board_3d.shape, (8, 8, 21))  # Correct shape

        # Check that each square has exactly one piece or is empty
        piece_sum = np.sum(board_3d[:, :, :12])
        self.assertEqual(piece_sum, 32)  # 32 pieces at the start of the game (16 for each side)

        # Verify initial piece placement
        self.assertEqual(np.sum(board_3d[:, :, 0]), 8)  # 8 white pawns
        self.assertEqual(np.sum(board_3d[:, :, 6]), 8)  # 8 black pawns

        # Check game state information
        self.assertTrue(np.all(board_3d[:, :, 13] == 1))  # White's turn
        self.assertTrue(np.all(board_3d[:, :, 14] == 1))  # White kingside castling
        self.assertTrue(np.all(board_3d[:, :, 15] == 1))  # White queenside castling
        self.assertTrue(np.all(board_3d[:, :, 16] == 1))  # Black kingside castling
        self.assertTrue(np.all(board_3d[:, :, 17] == 1))  # Black queenside castling

        self.assertEqual(np.sum(board_3d[:, :, 18]), 0)  # No en passant
        self.assertTrue(np.all(board_3d[:, :, 19] == 0))  # Half-move clock is 0
        self.assertTrue(np.all(board_3d[:, :, 20] == 1 / 100))  # Full-move number is 1

        # Total sum will be 32 (for pieces) plus game state info
        total_sum = np.sum(board_3d)
        self.assertGreater(total_sum, 32)

    def test_board_evaluation(self):
        self.engine.board = Board()
        initial_eval = self.engine.board.evaluate()
        print(f"Initial board evaluation: {initial_eval}")
        
        # Make a move
        move = list(self.engine.board.board.legal_moves)[0]
        self.engine.board.push_uci(move.uci())
        
        new_eval = self.engine.board.evaluate()
        print(f"Evaluation after move {move}: {new_eval}")
        
        self.assertNotEqual(initial_eval, new_eval)

if __name__ == "__main__":
    unittest.main()