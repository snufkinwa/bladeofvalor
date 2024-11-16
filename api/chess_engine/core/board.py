import chess
import numpy as np

piece_square_tables = {
    chess.PAWN: [
        0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5,  5, 10, 25, 25, 10,  5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5, -5, -10,  0,  0, -10, -5,  5,
        5, 10, 10, -20, -20, 10, 10,  5,
        0,  0,  0,  0,  0,  0,  0,  0
    ],
    chess.KNIGHT: [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20,  0,  0,  0,  0, -20, -40,
        -30,  0, 10, 15, 15, 10,  0, -30,
        -30,  5, 15, 20, 20, 15,  5, -30,
        -30,  0, 15, 20, 20, 15,  0, -30,
        -30,  5, 10, 15, 15, 10,  5, -30,
        -40, -20,  0,  5,  5,  0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50,
    ],
    chess.BISHOP: [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10,  0,  0,  0,  0,  0,  0, -10,
        -10,  0,  5, 10, 10,  5,  0, -10,
        -10,  5,  5, 10, 10,  5,  5, -10,
        -10,  0, 10, 10, 10, 10,  0, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -10,  5,  0,  0,  0,  0,  5, -10,
        -20, -10, -10, -10, -10, -10, -10, -20,
    ],
    chess.ROOK: [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 10, 10, 10, 10, 10,  5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        0,  0,  0,  5,  5,  0,  0,  0
    ],
    chess.QUEEN: [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
         -5,  0,  5,  5,  5,  5,  0, -5,
          0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20
    ],
    chess.KING: [
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -10, -20, -20, -20, -20, -20, -20, -10,
         20, 20,  0,  0,  0,  0, 20, 20,
         20, 30, 10,  0,  0, 10, 30, 20
    ]
}


class Board:
    def __init__(self):
        self.board = chess.Board()
        self.move_count = 0
        self.history = []

    def set_position(self, fen=None, moves=None):
        if fen:
            self.board.set_fen(fen)
        else:
            self.board.reset()  # Set to starting position if no FEN is provided
        
        self.history.clear()
        self.move_count = self.board.fullmove_number

        if moves:
            for move in moves:
                self.make_move(move)

    def make_move(self, move):
        """Make a move on the board."""
        legal_moves = self.generate_moves()
        if move not in legal_moves:
            raise ValueError(f"Illegal move: {move}. Legal moves are: {legal_moves}")
        self.board.push_uci(move)
        self.history.append(move)
        self.move_count += 1

    def undo_move(self):
        """Undo the last move."""
        if self.history:
            self.board.pop()
            return self.history.pop()
        return None

    def generate_moves(self):
        """Generate all legal moves in UCI format."""
        return [move.uci() for move in self.board.legal_moves]

    def is_game_over(self):
        """Check if the game is over."""
        return self.board.is_game_over()

    def get_result(self):
        """Get the game result if the game is over."""
        if self.board.is_checkmate():
            return "Checkmate"
        elif self.board.is_stalemate():
            return "Stalemate"
        elif self.board.is_insufficient_material():
            return "Draw (Insufficient Material)"
        elif self.board.can_claim_fifty_moves():
            return "Draw (Fifty-Move Rule)"
        elif self.board.can_claim_threefold_repetition():
            return "Draw (Threefold Repetition)"
        else:
            return "Game in progress"

    def get_fen(self):
        """Get the current position in FEN notation."""
        return self.board.fen()

    def evaluate(self):
        piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }

        score = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                value = piece_values[piece.piece_type]
                if piece.color == chess.WHITE:
                    score += value
                else:
                    score -= value

        # Add positional bonuses
        score += self.positional_score()

        # Add bonus for castling rights
        score += self.castling_score()

        # Add penalty for exposed king
        score += self.king_safety_score()

        # Return the score from the perspective of the current player
        return score if self.board.turn == chess.WHITE else -score

    def positional_score(self):
        score = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                if piece.color == chess.WHITE:
                    score += piece_square_tables[piece.piece_type][square]
                else:
                    score -= piece_square_tables[piece.piece_type][chess.square_mirror(square)]
        return score

    def castling_score(self):
        score = 0
        if self.board.has_kingside_castling_rights(chess.WHITE):
            score += 30
        if self.board.has_queenside_castling_rights(chess.WHITE):
            score += 20
        if self.board.has_kingside_castling_rights(chess.BLACK):
            score -= 30
        if self.board.has_queenside_castling_rights(chess.BLACK):
            score -= 20
        return score

    def king_safety_score(self):
        score = 0
        for color in [chess.WHITE, chess.BLACK]:
            king_square = self.board.king(color)
            if king_square:
                score += len(self.board.attackers(not color, king_square)) * (-50 if color == chess.WHITE else 50)
        return score

    def set_fen(self, fen):
        fen_parts = fen.split()
        self.board.set_fen(fen)
        
        # Set en passant square
        if len(fen_parts) > 3:
            if fen_parts[3] == '-':
                self.board.ep_square = None
            else:
                try:
                    self.board.ep_square = chess.parse_square(fen_parts[3])
                except ValueError:
                    self.board.ep_square = None
        else:
            self.board.ep_square = None
        
        # Ensure the board state is updated
        self.board.clear_stack()
        self.history.clear()
        self.move_count = self.board.fullmove_number

    def push_uci(self, uci):
            move = chess.Move.from_uci(uci)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.history.append(move)
            else:
                raise ValueError(f"Illegal move: {uci}")

    def board_to_3d_array(self):
        # Convert the board to a 3D array
        board_3d = np.zeros((8, 8, 21), dtype=np.float32)

        piece_map = {
            'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5,
            'p': 6, 'n': 7, 'b': 8, 'r': 9, 'q': 10, 'k': 11
        }

        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                board_3d[chess.square_rank(square), chess.square_file(square), piece_map[piece.symbol()]] = 1

        # Add extra planes for game state information
        board_3d[:, :, 12] = self.board.turn  # Whose turn it is
        board_3d[:, :, 13] = self.board.has_kingside_castling_rights(chess.WHITE)
        board_3d[:, :, 14] = self.board.has_queenside_castling_rights(chess.WHITE)
        board_3d[:, :, 15] = self.board.has_kingside_castling_rights(chess.BLACK)
        board_3d[:, :, 16] = self.board.has_queenside_castling_rights(chess.BLACK)

        if self.board.ep_square:
            ep_rank = chess.square_rank(self.board.ep_square)
            ep_file = chess.square_file(self.board.ep_square)
            board_3d[ep_rank, ep_file, 17] = 1

        # Add plane for half-move clock
        half_move_clock = self.board.halfmove_clock
        board_3d[:, :, 18] = half_move_clock / 50.0  # Normalize value for the network

        # Add plane for full-move number
        full_move_number = self.board.fullmove_number
        board_3d[:, :, 19] = full_move_number / 100.0  # Normalize value for the network

        # Additional plane for other purposes if needed, initialized to zero
        # board_3d[:, :, 20] = 0  # Placeholder for any future use

        return board_3d