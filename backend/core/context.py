import time
from typing import Dict, Optional
from .player import Player
from .bot import Bot

class LobbyContext:
    def __init__(self, lobby_id: str, config: dict, event_bus):
        self.lobby_id = lobby_id
        self.config = config
        self.event_bus = event_bus
        self.players: Dict[str, Player] = {}
        self.bots: Dict[str, Bot] = {}
        self.state = 'waiting'
        self.created_at = time.time()
        self.max_players = config.get('max_players', 10)
        self.max_bots = config.get('max_bots', 4)
        self.require_all_ready = config.get('require_all_ready', True)
        self.metadata = {}
    
    def add_player(self, player: Player):
        if len(self.players) < self.max_players:
            self.players[player.player_id] = player
            player.lobby_id = self.lobby_id
    
    def remove_player(self, player_id: str):
        if player_id in self.players:
            del self.players[player_id]
    
    def get_player(self, player_id: str) -> Optional[Player]:
        return self.players.get(player_id)
    
    def add_bot(self, bot: Bot):
        if len(self.bots) < self.max_bots:
            self.bots[bot.bot_id] = bot
            bot.lobby_id = self.lobby_id
    
    def remove_bot(self, bot_id: str):
        if bot_id in self.bots:
            del self.bots[bot_id]
    
    def set_player_ready(self, player_id: str, ready: bool):
        if player_id in self.players:
            self.players[player_id].ready = ready
            self.check_all_ready()
    
    def check_all_ready(self) -> bool:
        if not self.players:
            return False
        
        all_ready = all(p.ready for p in self.players.values())
        
        if all_ready and self.require_all_ready:
            self.state = 'ready'
            self.event_bus.emit('lobby_all_ready', {'lobby_id': self.lobby_id})
            return True
        
        return False
    
    def get_player_count(self) -> int:
        return len(self.players)
    
    def get_bot_count(self) -> int:
        return len(self.bots)
    
    def is_full(self) -> bool:
        return len(self.players) >= self.max_players
    
    def tick(self):
        for bot in self.bots.values():
            bot.update()
    
    def to_dict(self) -> dict:
        return {
            'lobby_id': self.lobby_id,
            'state': self.state,
            'player_count': self.get_player_count(),
            'bot_count': self.get_bot_count(),
            'max_players': self.max_players,
            'max_bots': self.max_bots,
            'players': [p.to_dict() for p in self.players.values()],
            'bots': [b.to_dict() for b in self.bots.values()],
            'created_at': self.created_at,
            'metadata': self.metadata
        }