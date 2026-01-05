from typing import Optional, List
from .base import StorageBackend
import fnmatch

try:
    import plyvel
    LEVELDB_AVAILABLE = True
except ImportError:
    LEVELDB_AVAILABLE = False

class LevelDBStore(StorageBackend):
    def __init__(self, db_path: str = 'joinly_leveldb'):
        if not LEVELDB_AVAILABLE:
            raise ImportError("plyvel not installed. Install with: pip install plyvel")
        
        self.db_path = db_path
        self.db = None
    
    def connect(self):
        self.db = plyvel.DB(self.db_path, create_if_missing=True)
    
    def disconnect(self):
        if self.db:
            self.db.close()
    
    def set(self, key: str, value: str) -> bool:
        try:
            self.db.put(key.encode('utf-8'), value.encode('utf-8'))
            return True
        except Exception as e:
            print(f"LevelDB set error: {e}")
            return False
    
    def get(self, key: str) -> Optional[str]:
        try:
            value = self.db.get(key.encode('utf-8'))
            return value.decode('utf-8') if value else None
        except Exception as e:
            print(f"LevelDB get error: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        try:
            self.db.delete(key.encode('utf-8'))
            return True
        except Exception as e:
            print(f"LevelDB delete error: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        try:
            return self.db.get(key.encode('utf-8')) is not None
        except:
            return False
    
    def keys(self, pattern: str = '*') -> List[str]:
        try:
            all_keys = []
            for key, _ in self.db:
                key_str = key.decode('utf-8')
                if pattern == '*' or fnmatch.fnmatch(key_str, pattern):
                    all_keys.append(key_str)
            return all_keys
        except Exception as e:
            print(f"LevelDB keys error: {e}")
            return []
    
    def clear(self):
        try:
            for key in self.keys():
                self.delete(key)
        except Exception as e:
            print(f"LevelDB clear error: {e}")