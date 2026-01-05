import uuid
from typing import Dict, List, Optional
from .bot_profiles import BotProfileLibrary
from .behavior import BehaviorController
from core.bot import Bot

class BotManager:
    def __init__(self, engine):
        self.engine = engine
        self.profile_library = BotProfileLibrary()
        self.behavior_controller = BehaviorController()
        self.active_bots: Dict[str, Bot] = {}
    
    def create_bot(self, profile_name: str = 'default') -> Bot:
        profile = self.profile_library.get_profile(profile_name)
        bot_id = f"bot_{uuid.uuid4().hex[:8]}"
        
        bot = Bot(bot_id, profile)
        self.active_bots[bot_id] = bot
        
        return bot
    
    def create_bots(self, count: int, profile_name: str = 'default') -> List[Bot]:
        bots = []
        for _ in range(count):
            bot = self.create_bot(profile_name)
            bots.append(bot)
        return bots
    
    def add_bot_to_lobby(self, lobby_id: str, profile_name: str = 'default') -> Optional[Bot]:
        bot = self.create_bot(profile_name)
        
        if self.engine.add_bot_to_lobby(lobby_id, bot):
            return bot
        
        del self.active_bots[bot.bot_id]
        return None
    
    def remove_bot(self, bot_id: str):
        if bot_id in self.active_bots:
            bot = self.active_bots[bot_id]
            if bot.lobby_id:
                self.engine.remove_bot_from_lobby(bot.lobby_id, bot_id)
            del self.active_bots[bot_id]
    
    def get_bot(self, bot_id: str) -> Optional[Bot]:
        return self.active_bots.get(bot_id)
    
    def get_all_bots(self) -> List[Bot]:
        return list(self.active_bots.values())
    
    def fill_lobby_with_bots(self, lobby_id: str, profile_name: str = 'default'):
        lobby = self.engine.get_lobby(lobby_id)
        if not lobby:
            return []
        
        available_slots = lobby.max_players - lobby.get_player_count()
        bot_slots = min(available_slots, lobby.max_bots - lobby.get_bot_count())
        
        added_bots = []
        for _ in range(bot_slots):
            bot = self.add_bot_to_lobby(lobby_id, profile_name)
            if bot:
                added_bots.append(bot)
        
        return added_bots
    
    def update_all_bots(self):
        for bot in self.active_bots.values():
            bot.tick()
            self.behavior_controller.execute_behavior(bot)
    
    def get_bot_stats(self) -> dict:
        return {
            'total_bots': len(self.active_bots),
            'bots_by_behavior': self._count_by_behavior(),
            'bots_in_lobbies': self._count_in_lobbies()
        }
    
    def _count_by_behavior(self) -> Dict[str, int]:
        counts = {}
        for bot in self.active_bots.values():
            behavior = bot.behavior
            counts[behavior] = counts.get(behavior, 0) + 1
        return counts
    
    def _count_in_lobbies(self) -> int:
        return sum(1 for bot in self.active_bots.values() if bot.lobby_id)