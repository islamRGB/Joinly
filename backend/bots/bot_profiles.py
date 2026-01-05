import random
from typing import Dict

class BotProfileLibrary:
    def __init__(self):
        self.profiles: Dict[str, dict] = {
            'default': {
                'username': self._generate_name(),
                'skill_rating': 1000,
                'behavior': 'normal',
                'auto_ready': True,
                'ready_delay': 2.0,
                'metadata': {}
            },
            'beginner': {
                'username': self._generate_name('Newbie'),
                'skill_rating': random.randint(500, 800),
                'behavior': 'passive',
                'auto_ready': True,
                'ready_delay': 3.0,
                'metadata': {'difficulty': 'easy'}
            },
            'intermediate': {
                'username': self._generate_name('Player'),
                'skill_rating': random.randint(900, 1200),
                'behavior': 'normal',
                'auto_ready': True,
                'ready_delay': 2.0,
                'metadata': {'difficulty': 'medium'}
            },
            'expert': {
                'username': self._generate_name('Pro'),
                'skill_rating': random.randint(1400, 1800),
                'behavior': 'aggressive',
                'auto_ready': True,
                'ready_delay': 1.0,
                'metadata': {'difficulty': 'hard'}
            },
            'master': {
                'username': self._generate_name('Master'),
                'skill_rating': random.randint(1900, 2500),
                'behavior': 'aggressive',
                'auto_ready': True,
                'ready_delay': 0.5,
                'metadata': {'difficulty': 'expert'}
            }
        }
    
    def _generate_name(self, prefix: str = 'Bot') -> str:
        suffixes = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta']
        numbers = random.randint(100, 999)
        return f"{prefix}{random.choice(suffixes)}{numbers}"
    
    def get_profile(self, profile_name: str) -> dict:
        if profile_name in self.profiles:
            profile = self.profiles[profile_name].copy()
            profile['username'] = self._generate_name(profile_name.capitalize())
            return profile
        return self.profiles['default'].copy()
    
    def add_profile(self, name: str, profile: dict):
        self.profiles[name] = profile
    
    def get_all_profiles(self) -> Dict[str, dict]:
        return self.profiles.copy()
    
    def get_random_profile(self) -> dict:
        profile_name = random.choice(list(self.profiles.keys()))
        return self.get_profile(profile_name)