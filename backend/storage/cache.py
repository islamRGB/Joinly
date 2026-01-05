import time
import threading
from typing import Dict, Optional
from collections import OrderedDict

class CacheEntry:
    def __init__(self, value: str, ttl: Optional[int] = None):
        self.value = value
        self.created_at = time.time()
        self.ttl = ttl
        self.access_count = 0
        self.last_accessed = time.time()
    
    def is_expired(self) -> bool:
        if self.ttl is None:
            return False
        return (time.time() - self.created_at) > self.ttl
    
    def access(self):
        self.access_count += 1
        self.last_accessed = time.time()

class LRUCache:
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.lock = threading.RLock()
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[str]:
        with self.lock:
            if key in self.cache:
                entry = self.cache[key]
                
                if entry.is_expired():
                    del self.cache[key]
                    self.misses += 1
                    return None
                
                entry.access()
                self.cache.move_to_end(key)
                self.hits += 1
                return entry.value
            
            self.misses += 1
            return None
    
    def set(self, key: str, value: str, ttl: Optional[int] = None):
        with self.lock:
            if key in self.cache:
                del self.cache[key]
            
            if len(self.cache) >= self.max_size:
                self.cache.popitem(last=False)
            
            self.cache[key] = CacheEntry(value, ttl)
    
    def delete(self, key: str):
        with self.lock:
            if key in self.cache:
                del self.cache[key]
    
    def clear(self):
        with self.lock:
            self.cache.clear()
            self.hits = 0
            self.misses = 0
    
    def cleanup_expired(self):
        with self.lock:
            expired_keys = [k for k, v in self.cache.items() if v.is_expired()]
            for key in expired_keys:
                del self.cache[key]
    
    def get_stats(self) -> dict:
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': round(hit_rate, 2)
        }