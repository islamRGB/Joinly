import time
from typing import Optional

class Player:
    def __init__(self, player_id: str, username: str, metadata: dict = None):
        self.player_id = player_id
        self.username = username
        self.ready = False
        self.team = None
        self.lobby_id: Optional[str] = None
        self.party_id: Optional[str] = None
        self.connected = True
        self.last_heartbeat = time.time()
        self.metadata = metadata or {}
        self.skill_rating = metadata.get('skill_rating', 1000) if metadata else 1000
        self.joined_at = time.time()
        self.permissions = set()
    
    def set_ready(self, ready: bool):
        self.ready = ready
    
    def set_team(self, team: int):
        self.team = team
    
    def heartbeat(self):
        self.last_heartbeat = time.time()
        self.connected = True
    
    def is_alive(self, timeout: int = 30) -> bool:
        return (time.time() - self.last_heartbeat) < timeout
    
    def to_dict(self) -> dict:
        return {
            'player_id': self.player_id,
            'username': self.username,
            'ready': self.ready,
            'team': self.team,
            'lobby_id': self.lobby_id,
            'party_id': self.party_id,
            'connected': self.connected,
            'skill_rating': self.skill_rating,
            'joined_at': self.joined_at,
            'metadata': self.metadata
        }