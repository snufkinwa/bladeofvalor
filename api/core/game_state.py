from typing import Dict, Optional
from src.core.chess_engine import ChessEngine

class GameStateManager:
    def __init__(self):
        self.games: Dict[str, ChessEngine] = {}
    
    def create_game(self, game_id: str) -> None:
        self.games[game_id] = ChessEngine()
    
    def get_game(self, game_id: str) -> Optional[ChessEngine]:
        return self.games.get(game_id)
    
    def remove_game(self, game_id: str) -> None:
        if game_id in self.games:
            self.games[game_id].engine.quit()
            del self.games[game_id]