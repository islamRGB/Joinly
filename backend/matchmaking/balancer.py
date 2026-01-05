from typing import List
from .tickets import MatchTicket

class TeamBalancer:
    def __init__(self):
        self.balance_method = 'skill_based'
    
    def balance_teams(self, tickets: List[MatchTicket], team_size: int) -> List[List[MatchTicket]]:
        if self.balance_method == 'skill_based':
            return self._balance_by_skill(tickets, team_size)
        elif self.balance_method == 'random':
            return self._balance_random(tickets, team_size)
        else:
            return self._balance_by_skill(tickets, team_size)
    
    def _balance_by_skill(self, tickets: List[MatchTicket], team_size: int) -> List[List[MatchTicket]]:
        sorted_tickets = sorted(tickets, key=lambda t: t.skill_rating, reverse=True)
        
        num_teams = len(tickets) // team_size
        teams = [[] for _ in range(num_teams)]
        team_skills = [0] * num_teams
        
        for ticket in sorted_tickets:
            min_skill_team = team_skills.index(min(team_skills))
            teams[min_skill_team].append(ticket)
            team_skills[min_skill_team] += ticket.skill_rating
        
        return teams
    
    def _balance_random(self, tickets: List[MatchTicket], team_size: int) -> List[List[MatchTicket]]:
        import random
        shuffled = tickets.copy()
        random.shuffle(shuffled)
        
        num_teams = len(tickets) // team_size
        teams = []
        
        for i in range(num_teams):
            team = shuffled[i * team_size:(i + 1) * team_size]
            teams.append(team)
        
        return teams
    
    def calculate_team_balance(self, teams: List[List[MatchTicket]]) -> dict:
        team_skills = []
        
        for team in teams:
            avg_skill = sum(t.skill_rating for t in team) / len(team) if team else 0
            team_skills.append(avg_skill)
        
        if not team_skills:
            return {'balance_score': 0, 'skill_difference': 0}
        
        max_skill = max(team_skills)
        min_skill = min(team_skills)
        skill_diff = max_skill - min_skill
        
        balance_score = 100 - min(skill_diff / 10, 100)
        
        return {
            'balance_score': balance_score,
            'skill_difference': skill_diff,
            'team_skills': team_skills
        }