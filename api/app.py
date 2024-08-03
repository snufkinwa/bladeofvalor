from flask import Flask, request, jsonify
from model import create_model
from api.chess_engine.core.cnn_chess_engine import VectorChessEngine
import chess

app = Flask(__name__)

engine = VectorChessEngine(model)

@app.route('/get_move', methods=['POST'])
def get_move():
    data = request.json
    fen = data.get('fen', chess.STARTING_FEN)
    engine.board.set_fen(fen)
    best_move = engine.get_best_move()
    return jsonify({'move': best_move})

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.json
    fen = data.get('fen', chess.STARTING_FEN)
    move = data.get('move')
    engine.board.set_fen(fen)
    engine.board.push_uci(move)
    return jsonify({
        'fen': engine.board.board.fen(),
        'game_over': engine.board.is_game_over(),
        'result': engine.board.board.result() if engine.board.is_game_over() else None
    })

if __name__ == '__main__':
    app.run(debug=True)

