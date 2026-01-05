import time
import uuid
from typing import Optional

class MatchTicket:
    def __init__(self, player_id: str, username: str, skill_rating: int = 1000, metadata: dict = None):
        self.ticket_id = str(uuid.uuid4())
        self.player_id = player_id
        self.username = username
        self.skill_rating = skill_rating
        self.metadata = metadata or {}
        self.status = 'queued'
        self.created_at = time.time()
        self.queued_at = time.time()
        self.matched_at: Optional[float] = None
        self.party_id: Optional[str] = None
        self.priority = 0
    
    def set_status(self, status: str):
        self.status = status
        if status == 'matched':
            self.matched_at = time.time()
    
    def get_wait_time(self) -> float:
        if self.matched_at:
            return self.matched_at - self.queued_at
        return time.time() - self.queued_at
    
    def to_player(self):
        from core.player import Player
        return Player(
            player_id=self.player_id,
            username=self.username,
            metadata={
                'skill_rating': self.skill_rating,
                **self.metadata
            }
        )
    
    def to_dict(self) -> dict:
        return {
            'ticket_id': self.ticket_id,
            'player_id': self.player_id,
            'username': self.username,
            'skill_rating': self.skill_rating,
            'status': self.status,
            'wait_time': self.get_wait_time(),
            'created_at': self.created_at,
            'party_id': self.party_id,
            'metadata': self.metadata
        }