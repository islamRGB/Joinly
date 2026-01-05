import random
import time

class BehaviorController:
    def __init__(self):
        self.behaviors = {
            'normal': self._normal_behavior,
            'aggressive': self._aggressive_behavior,
            'passive': self._passive_behavior,
            'random': self._random_behavior
        }
    
    def execute_behavior(self, bot):
        behavior_func = self.behaviors.get(bot.behavior, self._normal_behavior)
        behavior_func(bot)
    
    def _normal_behavior(self, bot):
        if not bot.ready and bot.auto_ready:
            if time.time() - bot.joined_at > bot.ready_delay:
                bot.ready = True
    
    def _aggressive_behavior(self, bot):
        if not bot.ready and bot.auto_ready:
            if time.time() - bot.joined_at > bot.ready_delay * 0.5:
                bot.ready = True
    
    def _passive_behavior(self, bot):
        if not bot.ready and bot.auto_ready:
            if time.time() - bot.joined_at > bot.ready_delay * 1.5:
                bot.ready = True
    
    def _random_behavior(self, bot):
        if not bot.ready and bot.auto_ready:
            delay = random.uniform(bot.ready_delay * 0.5, bot.ready_delay * 2.0)
            if time.time() - bot.joined_at > delay:
                bot.ready = True
    
    def add_behavior(self, name: str, behavior_func):
        self.behaviors[name] = behavior_func
    
    def get_available_behaviors(self):
        return list(self.behaviors.keys())