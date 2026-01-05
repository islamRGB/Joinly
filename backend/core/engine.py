import threading
import time
from typing import Dict, List, Optional
from .context import LobbyContext
from .player import Player
from .party import Party
from .bot import Bot
from .events import EventBus
from .rules import RuleEngine
from .permissions import PermissionManager

class LobbyEngine:
    def __init__(self):
        self.lobbies: Dict[str, LobbyContext] = {}
        self.players: Dict[str, Player] = {}
        self.parties: Dict[str, Party] = {}
        self.bots: Dict[str, Bot] = {}
        self.event_bus = EventBus()
        self.rule_engine = RuleEngine()
        self.permission_manager = PermissionManager()
        self.lock = threading.RLock()
        
    def create_lobby(self, lobby_id: str, config: dict) -> LobbyContext:
        with self.lock:
            lobby = LobbyContext(lobby_id, config, self.event_bus)
            self.lobbies[lobby_id] = lobby
            self.event_bus.emit('lobby_created', {'lobby_id': lobby_id})
            return lobby
    
    def get_lobby(self, lobby_id: str) -> Optional[LobbyContext]:
        return self.lobbies.get(lobby_id)
    
    def delete_lobby(self, lobby_id: str):
        with self.lock:
            if lobby_id in self.lobbies:
                lobby = self.lobbies[lobby_id]
                for player_id in list(lobby.players.keys()):
                    self.remove_player_from_lobby(lobby_id, player_id)
                del self.lobbies[lobby_id]
                self.event_bus.emit('lobby_deleted', {'lobby_id': lobby_id})
    
    def add_player_to_lobby(self, lobby_id: str, player: Player) -> bool:
        with self.lock:
            lobby = self.get_lobby(lobby_id)
            if not lobby:
                return False
            
            if not self.rule_engine.can_join(lobby, player):
                return False
            
            lobby.add_player(player)
            self.players[player.player_id] = player
            self.event_bus.emit('player_joined', {
                'lobby_id': lobby_id,
                'player_id': player.player_id
            })
            return True
    
    def remove_player_from_lobby(self, lobby_id: str, player_id: str):
        with self.lock:
            lobby = self.get_lobby(lobby_id)
            if lobby and player_id in lobby.players:
                lobby.remove_player(player_id)
                if player_id in self.players:
                    del self.players[player_id]
                self.event_bus.emit('player_left', {
                    'lobby_id': lobby_id,
                    'player_id': player_id
                })
    
    def set_player_ready(self, lobby_id: str, player_id: str, ready: bool):
        with self.lock:
            lobby = self.get_lobby(lobby_id)
            if lobby and player_id in lobby.players:
                lobby.set_player_ready(player_id, ready)
                self.event_bus.emit('player_ready_changed', {
                    'lobby_id': lobby_id,
                    'player_id': player_id,
                    'ready': ready
                })
    
    def add_bot_to_lobby(self, lobby_id: str, bot: Bot) -> bool:
        with self.lock:
            lobby = self.get_lobby(lobby_id)
            if not lobby:
                return False
            
            lobby.add_bot(bot)
            self.bots[bot.bot_id] = bot
            self.event_bus.emit('bot_joined', {
                'lobby_id': lobby_id,
                'bot_id': bot.bot_id
            })
            return True
    
    def remove_bot_from_lobby(self, lobby_id: str, bot_id: str):
        with self.lock:
            lobby = self.get_lobby(lobby_id)
            if lobby and bot_id in lobby.bots:
                lobby.remove_bot(bot_id)
                if bot_id in self.bots:
                    del self.bots[bot_id]
                self.event_bus.emit('bot_left', {
                    'lobby_id': lobby_id,
                    'bot_id': bot_id
                })
    
    def create_party(self, party_id: str, leader_id: str) -> Party:
        with self.lock:
            party = Party(party_id, leader_id)
            self.parties[party_id] = party
            return party
    
    def get_all_lobbies(self) -> List[dict]:
        with self.lock:
            return [lobby.to_dict() for lobby in self.lobbies.values()]
    
    def get_player(self, player_id: str) -> Optional[Player]:
        return self.players.get(player_id)
    
    def get_all_players(self) -> List[Player]:
        with self.lock:
            return list(self.players.values())
    
    def tick(self):
        with self.lock:
            for lobby in self.lobbies.values():
                lobby.tick()
            for bot in self.bots.values():
                bot.tick()