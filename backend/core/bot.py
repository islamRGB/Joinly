import time
import random
from typing import Optional

class Bot:
    def __init__(self, bot_id: str, profile: dict):
        self.bot_id = bot_id
        self.username = profile.get('username', f'Bot_{bot_id[:4]}')
        self.profile = profile
        self.ready = False
        self.team = None
        self.lobby_id: Optional[str] = None
        self.skill_rating = profile.get('skill_rating', 1000)
        self.behavior = profile.get('behavior', 'normal')
        self.auto_ready = profile.get('auto_ready', True)
        self.ready_delay = profile.get('ready_delay', 2.0)
        self.joined_at = time.time()
        self.last_action = time.time()
        self.metadata = profile.get('metadata', {})
    
    def update(self):
        if self.auto_ready and not self.ready:
            if time.time() - self.joined_at > self.ready_delay:
                self.ready = True
    
    def set_team(self, team: int):
        self.team = team
    
    def tick(self):
        current_time = time.time()
        
        if self.behavior == 'aggressive':
            if current_time - self.last_action > 1.0:
                self.last_action = current_time
                
        elif self.behavior == 'passive':
            if current_time - self.last_action > 5.0:
                self.last_action = current_time
        
        self.update()
    
    def to_dict(self) -> dict:
        return {
            'bot_id': self.bot_id,
            'username': self.username,
            'ready': self.ready,
            'team': self.team,
            'lobby_id': self.lobby_id,
            'skill_rating': self.skill_rating,
            'behavior': self.behavior,
            'is_bot': True,
            'metadata': self.metadata
        }