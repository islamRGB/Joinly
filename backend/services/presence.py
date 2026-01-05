import threading
import time
from typing import Dict

class PresenceService:
    def __init__(self, engine):
        self.engine = engine
        self.active = False
        self.check_interval = 10
        self.timeout = 30
        self.thread = None
    
    def start(self):
        self.active = True
        self.thread = threading.Thread(target=self._presence_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        self.active = False
        if self.thread:
            self.thread.join()
    
    def _presence_loop(self):
        while self.active:
            try:
                self._check_player_presence()
            except Exception as e:
                print(f"Presence check error: {e}")
            time.sleep(self.check_interval)
    
    def _check_player_presence(self):
        current_time = time.time()
        disconnected_players = []
        
        for player_id, player in self.engine.players.items():
            if not player.is_alive(self.timeout):
                disconnected_players.append((player_id, player.lobby_id))
                player.connected = False
        
        for player_id, lobby_id in disconnected_players:
            if lobby_id:
                self.engine.remove_player_from_lobby(lobby_id, player_id)
                self.engine.event_bus.emit('player_disconnected', {
                    'player_id': player_id,
                    'lobby_id': lobby_id
                })
    
    def update_player_presence(self, player_id: str):
        player = self.engine.get_player(player_id)
        if player:
            player.heartbeat()
    
    def get_online_count(self) -> int:
        return sum(1 for p in self.engine.players.values() if p.connected)