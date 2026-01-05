import threading
from typing import Dict, List, Callable
import time

class EventBus:
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
        self.event_history: List[dict] = []
        self.max_history = 1000
        self.lock = threading.Lock()
    
    def on(self, event_name: str, callback: Callable):
        with self.lock:
            if event_name not in self.listeners:
                self.listeners[event_name] = []
            self.listeners[event_name].append(callback)
    
    def off(self, event_name: str, callback: Callable):
        with self.lock:
            if event_name in self.listeners:
                self.listeners[event_name].remove(callback)
    
    def emit(self, event_name: str, data: dict = None):
        event_data = {
            'event': event_name,
            'data': data or {},
            'timestamp': time.time()
        }
        
        with self.lock:
            self.event_history.append(event_data)
            if len(self.event_history) > self.max_history:
                self.event_history.pop(0)
            
            if event_name in self.listeners:
                for callback in self.listeners[event_name]:
                    try:
                        callback(event_data)
                    except Exception as e:
                        print(f"Error in event listener: {e}")
    
    def get_history(self, limit: int = 100) -> List[dict]:
        with self.lock:
            return self.event_history[-limit:]
    
    def clear_history(self):
        with self.lock:
            self.event_history.clear()