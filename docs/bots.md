# Joinly Bot System Documentation

## Overview

Joinly includes a comprehensive bot system that allows AI players to participate in lobbies with customizable behaviors and skill levels.

## Bot Profiles

### Default Profile

Balanced bot suitable for most scenarios.

```python
{
    'username': 'BotAlpha123',
    'skill_rating': 1000,
    'behavior': 'normal',
    'auto_ready': True,
    'ready_delay': 2.0
}
```

### Beginner Profile

Easy difficulty bot for new players.

```python
{
    'username': 'NewbieBot456',
    'skill_rating': 500-800,
    'behavior': 'passive',
    'auto_ready': True,
    'ready_delay': 3.0
}
```

### Intermediate Profile

Medium difficulty bot.

```python
{
    'username': 'PlayerBot789',
    'skill_rating': 900-1200,
    'behavior': 'normal',
    'auto_ready': True,
    'ready_delay': 2.0
}
```

### Expert Profile

Hard difficulty bot for experienced players.

```python
{
    'username': 'ProBot321',
    'skill_rating': 1400-1800,
    'behavior': 'aggressive',
    'auto_ready': True,
    'ready_delay': 1.0
}
```

### Master Profile

Expert level bot with highest skill.

```python
{
    'username': 'MasterBot999',
    'skill_rating': 1900-2500,
    'behavior': 'aggressive',
    'auto_ready': True,
    'ready_delay': 0.5
}
```

## Bot Manager

### Creating Bots

```python
from bots.bot_manager import BotManager

bot_manager = BotManager(engine)

bot = bot_manager.create_bot('expert')

bots = bot_manager.create_bots(5, 'intermediate')
```

### Adding Bots to Lobbies

```python
bot = bot_manager.add_bot_to_lobby('lobby_123', 'expert')

bots = bot_manager.fill_lobby_with_bots('lobby_123', 'default')
```

### Removing Bots

```python
bot_manager.remove_bot('bot_123')
```

### Getting Bot Information

```python
bot = bot_manager.get_bot('bot_123')

all_bots = bot_manager.get_all_bots()

stats = bot_manager.get_bot_stats()
```

## Bot Behaviors

### Normal Behavior

Standard bot behavior with predictable timing.

```python
def _normal_behavior(self, bot: Bot):
    if not bot.ready and bot.auto_ready:
        if time.time() - bot.joined_at > bot.ready_delay:
            bot.ready = True
```

### Aggressive Behavior

Quick actions and faster ready times.

```python
def _aggressive_behavior(self, bot: Bot):
    if not bot.ready and bot.auto_ready:
        if time.time() - bot.joined_at > bot.ready_delay * 0.5:
            bot.ready = True
```

### Passive Behavior

Delayed actions and slower ready times.

```python
def _passive_behavior(self, bot: Bot):
    if not bot.ready and bot.auto_ready:
        if time.time() - bot.joined_at > bot.ready_delay * 1.5:
            bot.ready = True
```

### Random Behavior

Unpredictable timing for varied gameplay.

```python
def _random_behavior(self, bot: Bot):
    if not bot.ready and bot.auto_ready:
        delay = random.uniform(bot.ready_delay * 0.5, bot.ready_delay * 2.0)
        if time.time() - bot.joined_at > delay:
            bot.ready = True
```

## Custom Bot Profiles

### Creating Custom Profiles

```python
from bots.bot_profiles import BotProfileLibrary

profile_library = BotProfileLibrary()

custom_profile = {
    'username': 'CustomBot',
    'skill_rating': 1500,
    'behavior': 'aggressive',
    'auto_ready': True,
    'ready_delay': 1.5,
    'metadata': {
        'difficulty': 'custom',
        'special_ability': 'fast_reflexes'
    }
}

profile_library.add_profile('custom', custom_profile)

bot = bot_manager.create_bot('custom')
```

### Random Profile Selection

```python
profile = profile_library.get_random_profile()
bot = bot_manager.create_bot(profile['username'])
```

## Custom Behaviors

### Adding Custom Behavior

```python
from bots.behavior import BehaviorController

def custom_behavior(bot: Bot):
    if not bot.ready:
        if random.random() < 0.1:
            bot.ready = True

behavior_controller = BehaviorController()
behavior_controller.add_behavior('custom', custom_behavior)

bot.behavior = 'custom'
```

## Bot Lifecycle

### Creation

```
BotManager.create_bot(profile)
  → BotProfileLibrary.get_profile(profile)
    → Bot(bot_id, profile)
      → Register in active_bots
```

### Update Loop

```
Engine.tick()
  → Bot.tick()
    → Bot.update()
      → BehaviorController.execute_behavior()
        → Behavior function
```

### Removal

```
BotManager.remove_bot(bot_id)
  → Engine.remove_bot_from_lobby()
    → Unregister from active_bots
```

## API Integration

### REST API

```bash
curl -X POST http://localhost:5000/api/bots \
  -H "Content-Type: application/json" \
  -d '{"profile": "expert"}'

curl -X POST http://localhost:5000/api/lobbies/lobby_123/bots \
  -H "Content-Type: application/json" \
  -d '{"profile": "intermediate"}'

curl -X POST http://localhost:5000/api/lobbies/lobby_123/bots/fill \
  -H "Content-Type: application/json" \
  -d '{"profile": "default"}'
```

### WebSocket

```javascript
socket.emit('add_bot', {
    lobby_id: 'lobby_123',
    profile: 'expert'
});
```

## Best Practices

### Bot Naming

Generate unique names to avoid confusion:

```python
def _generate_name(self, prefix: str = 'Bot') -> str:
    suffixes = ['Alpha', 'Beta', 'Gamma', 'Delta']
    numbers = random.randint(100, 999)
    return f"{prefix}{random.choice(suffixes)}{numbers}"
```

### Skill Balancing

Use appropriate bots for player skill levels:

```python
avg_player_skill = sum(p.skill_rating for p in players) / len(players)

if avg_player_skill < 1000:
    profile = 'beginner'
elif avg_player_skill < 1500:
    profile = 'intermediate'
else:
    profile = 'expert'

bot_manager.add_bot_to_lobby(lobby_id, profile)
```

### Bot Limits

Respect lobby bot limits:

```python
if lobby.get_bot_count() < lobby.max_bots:
    bot_manager.add_bot_to_lobby(lobby_id, profile)
```

### Cleanup

Remove inactive bots:

```python
for bot_id, bot in bot_manager.active_bots.items():
    if not bot.lobby_id:
        bot_manager.remove_bot(bot_id)
```

## Performance

### Update Frequency

Bots are updated every engine tick (default 1.0s).

### Resource Usage

Each bot consumes minimal resources:
- Memory: ~1KB per bot
- CPU: Negligible per tick

### Scaling

System can handle 100+ concurrent bots efficiently.