import chess
import sys
from cnn_chess_engine import CNNChessEngine
from config import MODEL_PATH

class UCI:
    def __init__(self, model_path):
        self.engine = CNNChessEngine(model_path=MODEL_PATH)
        self.board = chess.Board()

    def uci(self):
        print("id name CNNChessEngine")
        print("id author YourName")
        print("uciok")

    def isready(self):
        print("readyok")

    def ucinewgame(self):
        print("Calling new_game() in UCI class")  # Debug print
        self.engine.new_game()
        self.board.reset()

    def position(self, command):
        parts = command.split()
        if parts[0] == 'startpos':
            fen = chess.STARTING_FEN
            moves = parts[2:] if len(parts) > 2 and parts[1] == 'moves' else []
        else:
            fen_parts = []
            for part in parts[1:]:
                if part == 'moves':
                    break
                fen_parts.append(part)
            fen = ' '.join(fen_parts)
            moves = parts[parts.index('moves')+1:] if 'moves' in parts else []
        
        self.engine.set_position(fen, moves)

    def go(self, command):
        # Parse the command for depth
        depth = 3  # default depth
        if "depth" in command:
            depth = int(command.split()[1])

        self.board.generate_legal_moves()
        
        # Call the engine's search method
        best_move = self.engine.search(depth)
        
        # Output the best move
        print(f"bestmove {best_move}")

    def stop(self):
        self.engine.stop()

    def quit(self):
        sys.exit()

    def run(self):
        while True:
            try:
                command = input().strip()
                if command == 'quit':
                    break
                self.process_command(command)
            except EOFError:
                break

    def process_command(self, command):
        if command == "uci":
            self.uci()
        elif command == "isready":
            self.isready()
        elif command == "ucinewgame":
            self.ucinewgame()
        elif command.startswith("position"):
            self.position(command[9:])
        elif command.startswith("go"):
            self.go(command[3:])
        elif command == "stop":
            self.stop()

if __name__ == "__main__":
    uci = UCI(MODEL_PATH)
    uci.run()