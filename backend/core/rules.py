from typing import List, Callable
from .context import LobbyContext
from .player import Player

class Rule:
    def __init__(self, name: str, check: Callable):
        self.name = name
        self.check = check

class RuleEngine:
    def __init__(self):
        self.rules: List[Rule] = []
        self.setup_default_rules()
    
    def setup_default_rules(self):
        self.add_rule('lobby_not_full', lambda lobby, player: not lobby.is_full())
        self.add_rule('player_not_in_lobby', lambda lobby, player: player.player_id not in lobby.players)
        self.add_rule('lobby_accepting', lambda lobby, player: lobby.state in ['waiting', 'open'])
    
    def add_rule(self, name: str, check: Callable):
        self.rules.append(Rule(name, check))
    
    def remove_rule(self, name: str):
        self.rules = [r for r in self.rules if r.name != name]
    
    def can_join(self, lobby: LobbyContext, player: Player) -> bool:
        for rule in self.rules:
            try:
                if not rule.check(lobby, player):
                    return False
            except Exception as e:
                print(f"Rule {rule.name} failed: {e}")
                return False
        return True
    
    def validate_action(self, action_name: str, context: dict) -> bool:
        action_rules = {
            'start_match': lambda ctx: all(p.ready for p in ctx.get('players', [])),
            'add_bot': lambda ctx: ctx.get('bot_count', 0) < ctx.get('max_bots', 4),
            'kick_player': lambda ctx: ctx.get('has_permission', False)
        }
        
        if action_name in action_rules:
            try:
                return action_rules[action_name](context)
            except:
                return False
        
        return True