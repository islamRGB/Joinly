from abc import ABC, abstractmethod
from typing import Optional, List, Dict

class StorageBackend(ABC):
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def disconnect(self):
        pass
    
    @abstractmethod
    def set(self, key: str, value: str) -> bool:
        pass
    
    @abstractmethod
    def get(self, key: str) -> Optional[str]:
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        pass
    
    @abstractmethod
    def exists(self, key: str) -> bool:
        pass
    
    @abstractmethod
    def keys(self, pattern: str = '*') -> List[str]:
        pass
    
    @abstractmethod
    def clear(self):
        pass

class StorageManager:
    def __init__(self, backend: StorageBackend):
        self.backend = backend
        self.backend.connect()
    
    def save_lobby(self, lobby_id: str, data: dict) -> bool:
        import json
        key = f"lobby:{lobby_id}"
        value = json.dumps(data)
        return self.backend.set(key, value)
    
    def load_lobby(self, lobby_id: str) -> Optional[dict]:
        import json
        key = f"lobby:{lobby_id}"
        value = self.backend.get(key)
        if value:
            return json.loads(value)
        return None
    
    def delete_lobby(self, lobby_id: str) -> bool:
        key = f"lobby:{lobby_id}"
        return self.backend.delete(key)
    
    def save_player(self, player_id: str, data: dict) -> bool:
        import json
        key = f"player:{player_id}"
        value = json.dumps(data)
        return self.backend.set(key, value)
    
    def load_player(self, player_id: str) -> Optional[dict]:
        import json
        key = f"player:{player_id}"
        value = self.backend.get(key)
        if value:
            return json.loads(value)
        return None
    
    def get_all_lobbies(self) -> List[str]:
        keys = self.backend.keys("lobby:*")
        return [k.replace("lobby:", "") for k in keys]
    
    def get_all_players(self) -> List[str]:
        keys = self.backend.keys("player:*")
        return [k.replace("player:", "") for k in keys]
    
    def close(self):
        self.backend.disconnect()