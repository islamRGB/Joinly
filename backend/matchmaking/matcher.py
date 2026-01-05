import time
import threading
from typing import List, Dict, Optional
from .tickets import MatchTicket
from .queues import MatchQueue
from .balancer import TeamBalancer

class Matcher:
    def __init__(self, engine):
        self.engine = engine
        self.queues: Dict[str, MatchQueue] = {}
        self.balancer = TeamBalancer()
        self.active = True
        self.match_thread = None
        self.lock = threading.RLock()
    
    def start(self):
        self.active = True
        self.match_thread = threading.Thread(target=self._matching_loop, daemon=True)
        self.match_thread.start()
    
    def stop(self):
        self.active = False
        if self.match_thread:
            self.match_thread.join()
    
    def create_queue(self, queue_id: str, config: dict) -> MatchQueue:
        with self.lock:
            queue = MatchQueue(queue_id, config)
            self.queues[queue_id] = queue
            return queue
    
    def get_queue(self, queue_id: str) -> Optional[MatchQueue]:
        return self.queues.get(queue_id)
    
    def add_ticket(self, queue_id: str, ticket: MatchTicket) -> bool:
        with self.lock:
            queue = self.get_queue(queue_id)
            if queue:
                queue.add_ticket(ticket)
                return True
            return False
    
    def remove_ticket(self, queue_id: str, ticket_id: str):
        with self.lock:
            queue = self.get_queue(queue_id)
            if queue:
                queue.remove_ticket(ticket_id)
    
    def _matching_loop(self):
        while self.active:
            try:
                self._process_queues()
            except Exception as e:
                print(f"Matching error: {e}")
            time.sleep(1.0)
    
    def _process_queues(self):
        with self.lock:
            for queue in self.queues.values():
                matches = self._find_matches(queue)
                for match_group in matches:
                    self._create_match(queue, match_group)
    
    def _find_matches(self, queue: MatchQueue) -> List[List[MatchTicket]]:
        matches = []
        tickets = queue.get_active_tickets()
        
        if len(tickets) < queue.players_per_match:
            return matches
        
        sorted_tickets = sorted(tickets, key=lambda t: t.skill_rating)
        
        for i in range(0, len(sorted_tickets) - queue.players_per_match + 1, queue.players_per_match):
            group = sorted_tickets[i:i + queue.players_per_match]
            
            if len(group) == queue.players_per_match:
                avg_skill = sum(t.skill_rating for t in group) / len(group)
                skill_diff = max(t.skill_rating for t in group) - min(t.skill_rating for t in group)
                
                if skill_diff <= queue.max_skill_diff:
                    matches.append(group)
        
        return matches
    
    def _create_match(self, queue: MatchQueue, tickets: List[MatchTicket]):
        lobby_id = f"match_{int(time.time()*1000)}"
        
        lobby_config = {
            'max_players': queue.players_per_match,
            'max_bots': 0,
            'require_all_ready': True
        }
        
        lobby = self.engine.create_lobby(lobby_id, lobby_config)
        
        if queue.team_mode:
            teams = self.balancer.balance_teams(tickets, queue.team_size)
            for team_id, team_tickets in enumerate(teams):
                for ticket in team_tickets:
                    player = ticket.to_player()
                    player.team = team_id
                    self.engine.add_player_to_lobby(lobby_id, player)
                    queue.remove_ticket(ticket.ticket_id)
        else:
            for ticket in tickets:
                player = ticket.to_player()
                self.engine.add_player_to_lobby(lobby_id, player)
                queue.remove_ticket(ticket.ticket_id)
        
        self.engine.event_bus.emit('match_created', {
            'lobby_id': lobby_id,
            'queue_id': queue.queue_id,
            'player_count': len(tickets)
        })
    
    def get_all_queues(self) -> List[dict]:
        with self.lock:
            return [q.to_dict() for q in self.queues.values()]