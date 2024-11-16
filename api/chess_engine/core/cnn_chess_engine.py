import numpy as np
import chess
import time
import tensorflow as tf
import gc
from board import Board


class CNNChessEngine:
    def __init__(self, model_path=None):
        self.board = Board()
        self.model = None
        if model_path:
            self.load_model(model_path)
        self.stop_search = False

    def load_model(self, model_path):
        try:
            self.model = tf.keras.models.load_model(model_path)
            print(f"Model loaded successfully from {model_path}")
        except Exception as e:
            print(f"Error loading model from {model_path}: {str(e)}")
            self.model = None

    def search(self, depth):
        self.stop_search = False
        best_move = None
        best_value = -float('inf') if self.board.board.turn == chess.WHITE else float('inf')
        all_moves = list(self.board.generate_moves())

        for move in all_moves:
            if self.stop_search:
                break
            self.board.push_uci(move)
            board_value = self.minimax(depth - 1, -float('inf'), float('inf'), not self.board.board.turn)
            self.board.undo_move()
            print(f"info depth {depth} score cp {int(board_value * 100)} pv {move}")  # UCI info

            if self.board.board.turn == chess.WHITE:
                if board_value > best_value:
                    best_value = board_value
                    best_move = move
            else:
                if board_value < best_value:
                    best_value = board_value
                    best_move = move

        return best_move

    def evaluate_position(self):
        if self.model is None:
            return self.board.evaluate() / 100.0
        else:
            try:
                board_3d = self.board_to_3d_array()
                board_3d = np.expand_dims(board_3d, axis=0)  # add batch dimension
                evaluation = self.model.predict(board_3d)[0][0]
            except Exception as e:
                print(f"Error using new evaluation method: {str(e)}")
                print("Falling back to original method...")
                evaluation = self.board.evaluate() / 100.0  # Use fallback evaluation

            gc.collect()
            tf.keras.backend.clear_session()

            return evaluation

    def get_best_move(self, depth=1, time_limit=None):
        self.stop_search = False
        best_move = None
        best_value = -float('inf') if self.board.board.turn == chess.WHITE else float('inf')
        all_moves = list(self.board.generate_moves())

        start_time = time.time()
        for move in all_moves:
            if self.stop_search or (time_limit and time.time() - start_time > time_limit):
                break
            self.board.push_uci(move)
            board_value = self.minimax(depth - 1, -float('inf'), float('inf'), not self.board.board.turn)
            self.board.undo_move()
            print(f"info depth {depth} score cp {int(board_value * 100)} pv {move}")  # UCI info

            if self.board.board.turn == chess.WHITE:
                if board_value > best_value:
                    best_value = board_value
                    best_move = move
            else:
                if board_value < best_value:
                    best_value = board_value
                    best_move = move

        return best_move

    def new_game(self):
        self.board = Board()

    def stop(self):
        self.stop_search = True

    def set_position(self, fen=None, moves=None):
        self.board.set_position(fen, moves)

    def new_game(self):
        print("new_game method called")
        self.board = Board()

    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.board.board.is_game_over():
            return self.evaluate_position()

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.board.generate_moves():
                self.board.push_uci(move)
                eval = self.minimax(depth - 1, alpha, beta, False)
                self.board.undo_move()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.board.generate_moves():
                self.board.push_uci(move)
                eval = self.minimax(depth - 1, alpha, beta, True)
                self.board.undo_move()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def board_to_3d_array(self):
        board_3d = np.zeros((8, 8, 21), dtype=np.float32)

        piece_map = {
            chess.PAWN: 0, chess.KNIGHT: 1, chess.BISHOP: 2,
            chess.ROOK: 3, chess.QUEEN: 4, chess.KING: 5
        }

        for square in chess.SQUARES:
            row, col = divmod(square, 8)
            piece = self.board.board.piece_at(square)
            if piece:
                piece_type = piece_map[piece.piece_type]
                if piece.color == chess.BLACK:
                    piece_type += 6
                board_3d[row, col, piece_type] = 1
            else:
                board_3d[row, col, 12] = 1  # Empty square

        # Add extra planes for game state
        if self.board.board.turn == chess.WHITE:
            board_3d[:, :, 13] = 1

        if self.board.board.has_kingside_castling_rights(chess.WHITE):
            board_3d[:, :, 14] = 1
        if self.board.board.has_queenside_castling_rights(chess.WHITE):
            board_3d[:, :, 15] = 1
        if self.board.board.has_kingside_castling_rights(chess.BLACK):
            board_3d[:, :, 16] = 1
        if self.board.board.has_queenside_castling_rights(chess.BLACK):
            board_3d[:, :, 17] = 1

        # Add en passant target plane
        en_passant_square = self.board.board.ep_square
        if en_passant_square is not None:
            row, col = divmod(en_passant_square, 8)
            board_3d[row, col, 18] = 1

        # Add half-move clock (scaled down for normalization purposes)
        halfmove_clock = self.board.board.halfmove_clock
        board_3d[:, :, 19] = halfmove_clock / 50.0

        # Add full-move number (scaled down for normalization purposes)
        fullmove_number = self.board.board.fullmove_number
        board_3d[:, :, 20] = fullmove_number / 100.0  # assuming a max of 100 full moves

        return board_3d