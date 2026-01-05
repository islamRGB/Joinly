import time
from typing import Dict, List

class Party:
    def __init__(self, party_id: str, leader_id: str):
        self.party_id = party_id
        self.leader_id = leader_id
        self.members: Dict[str, dict] = {}
        self.created_at = time.time()
        self.max_members = 5
        self.lobby_id = None
        
        self.members[leader_id] = {
            'player_id': leader_id,
            'joined_at': time.time(),
            'role': 'leader'
        }
    
    def add_member(self, player_id: str) -> bool:
        if len(self.members) >= self.max_members:
            return False
        
        if player_id not in self.members:
            self.members[player_id] = {
                'player_id': player_id,
                'joined_at': time.time(),
                'role': 'member'
            }
            return True
        return False
    
    def remove_member(self, player_id: str):
        if player_id in self.members:
            del self.members[player_id]
            
            if player_id == self.leader_id and self.members:
                new_leader = list(self.members.keys())[0]
                self.leader_id = new_leader
                self.members[new_leader]['role'] = 'leader'
    
    def is_leader(self, player_id: str) -> bool:
        return player_id == self.leader_id
    
    def get_member_count(self) -> int:
        return len(self.members)
    
    def get_member_ids(self) -> List[str]:
        return list(self.members.keys())
    
    def to_dict(self) -> dict:
        return {
            'party_id': self.party_id,
            'leader_id': self.leader_id,
            'members': list(self.members.values()),
            'member_count': self.get_member_count(),
            'max_members': self.max_members,
            'lobby_id': self.lobby_id,
            'created_at': self.created_at
        }