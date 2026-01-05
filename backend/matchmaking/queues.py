import time
from typing import Dict, List
from .tickets import MatchTicket

class MatchQueue:
    def __init__(self, queue_id: str, config: dict):
        self.queue_id = queue_id
        self.config = config
        self.tickets: Dict[str, MatchTicket] = {}
        self.created_at = time.time()
        
        self.players_per_match = config.get('players_per_match', 10)
        self.max_skill_diff = config.get('max_skill_diff', 200)
        self.team_mode = config.get('team_mode', False)
        self.team_size = config.get('team_size', 5)
        self.max_wait_time = config.get('max_wait_time', 300)
        self.priority_enabled = config.get('priority_enabled', False)
    
    def add_ticket(self, ticket: MatchTicket):
        self.tickets[ticket.ticket_id] = ticket
        ticket.queued_at = time.time()
    
    def remove_ticket(self, ticket_id: str):
        if ticket_id in self.tickets:
            del self.tickets[ticket_id]
    
    def get_ticket(self, ticket_id: str) -> MatchTicket:
        return self.tickets.get(ticket_id)
    
    def get_active_tickets(self) -> List[MatchTicket]:
        current_time = time.time()
        active = []
        
        for ticket in self.tickets.values():
            if ticket.status == 'queued':
                wait_time = current_time - ticket.queued_at
                
                if wait_time > self.max_wait_time:
                    ticket.status = 'timeout'
                else:
                    active.append(ticket)
        
        return active
    
    def get_queue_length(self) -> int:
        return len([t for t in self.tickets.values() if t.status == 'queued'])
    
    def get_average_wait_time(self) -> float:
        current_time = time.time()
        queued_tickets = [t for t in self.tickets.values() if t.status == 'queued']
        
        if not queued_tickets:
            return 0.0
        
        total_wait = sum(current_time - t.queued_at for t in queued_tickets)
        return total_wait / len(queued_tickets)
    
    def clear_expired_tickets(self):
        current_time = time.time()
        expired = []
        
        for ticket_id, ticket in self.tickets.items():
            if ticket.status == 'timeout' or ticket.status == 'cancelled':
                expired.append(ticket_id)
            elif current_time - ticket.created_at > 3600:
                expired.append(ticket_id)
        
        for ticket_id in expired:
            self.remove_ticket(ticket_id)
    
    def to_dict(self) -> dict:
        return {
            'queue_id': self.queue_id,
            'players_per_match': self.players_per_match,
            'team_mode': self.team_mode,
            'team_size': self.team_size,
            'queue_length': self.get_queue_length(),
            'average_wait_time': self.get_average_wait_time(),
            'max_skill_diff': self.max_skill_diff,
            'created_at': self.created_at
        }