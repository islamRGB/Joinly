import time
from typing import Dict, List
from collections import defaultdict

class AnalyticsService:
    def __init__(self, engine):
        self.engine = engine
        self.metrics: Dict[str, any] = defaultdict(int)
        self.event_counts: Dict[str, int] = defaultdict(int)
        self.start_time = time.time()
        
        self._setup_event_tracking()
    
    def _setup_event_tracking(self):
        events = [
            'lobby_created', 'lobby_deleted', 'player_joined',
            'player_left', 'player_ready_changed', 'bot_joined',
            'bot_left', 'match_created', 'lobby_all_ready'
        ]
        
        for event in events:
            self.engine.event_bus.on(event, self._track_event)
    
    def _track_event(self, event_data):
        event_name = event_data.get('event')
        self.event_counts[event_name] += 1
        self.metrics['total_events'] += 1
    
    def get_analytics(self) -> dict:
        uptime = time.time() - self.start_time
        
        analytics = {
            'uptime_seconds': uptime,
            'total_lobbies': len(self.engine.lobbies),
            'total_players': len(self.engine.players),
            'total_bots': len(self.engine.bots),
            'total_parties': len(self.engine.parties),
            'event_counts': dict(self.event_counts),
            'metrics': dict(self.metrics)
        }
        
        if self.engine.lobbies:
            analytics['avg_players_per_lobby'] = len(self.engine.players) / len(self.engine.lobbies)
        
        return analytics
    
    def track_custom_metric(self, name: str, value: any):
        self.metrics[name] = value
    
    def increment_metric(self, name: str, amount: int = 1):
        self.metrics[name] += amount
    
    def get_metric(self, name: str) -> any:
        return self.metrics.get(name, 0)
    
    def reset_metrics(self):
        self.metrics.clear()
        self.event_counts.clear()