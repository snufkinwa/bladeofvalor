# main.py
from config import MODEL_PATH
from cnn_chess_engine import CNNChessEngine
import chess

def main():
    # Initialize the engine with the model path from config
    engine = CNNChessEngine(MODEL_PATH)

    # List of predetermined moves for Black (UCI format)
    black_opening_moves = ["e7e5", "g8f6", "d7d6"]

    black_move_index = 0

    while not engine.board.board.is_game_over():
        print(engine.board.board)

        if engine.board.board.turn == chess.BLACK:
            if black_move_index < len(black_opening_moves):
                # Play predetermined opening moves for Black
                move = black_opening_moves[black_move_index]
                black_move_index += 1
                engine.board.push_uci(move)
                print(f"Black plays: {move}")
            else:
                # Human player's turn
                move = input("Enter your move (in UCI format, e.g. e2e4): ")
                try:
                    engine.board.push_uci(move)
                except ValueError:
                    print("Invalid move. Please try again.")
                    continue
        else:
            # Engine's turn
            move = engine.get_best_move(depth=3)
            print(f"Engine plays: {move}")
            engine.board.push_uci(move)

        print(f"Position evaluation: {engine.evaluate_position()}")

    print("Game Over")
    print(f"Result: {engine.board.board.result()}")

if __name__ == "__main__":
    main()


