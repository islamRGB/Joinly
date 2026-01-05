import sys
sys.path.append('../../backend')

from bootstrap import JoinlyBootstrap
from core.player import Player
from bots.bot_manager import BotManager
import time

bootstrap = JoinlyBootstrap()
bootstrap.start_services()

engine = bootstrap.engine
bot_manager = BotManager(engine)

print("Creating bot-heavy lobby...")
lobby = engine.create_lobby('bot_lobby', {
    'max_players': 10,
    'max_bots': 8,
    'require_all_ready': False
})

print(f"Lobby created: {lobby.lobby_id}")

print("\nAdding 2 human players...")
for i in range(2):
    player = Player(
        player_id=f'player_{i}',
        username=f'HumanPlayer{i}',
        metadata={'skill_rating': 1200}
    )
    engine.add_player_to_lobby(lobby.lobby_id, player)
    print(f"Added {player.username}")

print("\nFilling lobby with bots...")
profiles = ['beginner', 'intermediate', 'expert', 'master']

for i, profile in enumerate(profiles * 2):
    bot = bot_manager.add_bot_to_lobby(lobby.lobby_id, profile)
    if bot:
        print(f"Added {bot.username} ({profile})")

print("\nWaiting for bots to get ready...")
for _ in range(5):
    time.sleep(1)
    ready_count = sum(1 for p in lobby.players.values() if p.ready)
    ready_count += sum(1 for b in lobby.bots.values() if b.ready)
    total = lobby.get_player_count() + lobby.get_bot_count()
    print(f"Ready: {ready_count}/{total}")
    
    bot_manager.update_all_bots()

print("\nFinal lobby composition:")
print(f"Human players: {lobby.get_player_count()}")
print(f"Bots: {lobby.get_bot_count()}")

for bot in lobby.bots.values():
    status = "READY" if bot.ready else "NOT READY"
    print(f"  {bot.username} ({bot.behavior}) - {status}")

print("\nBot statistics:")
stats = bot_manager.get_bot_stats()
print(f"Total bots: {stats['total_bots']}")
print(f"Bots by behavior: {stats['bots_by_behavior']}")
print(f"Bots in lobbies: {stats['bots_in_lobbies']}")

print("\nExample complete!")
bootstrap.stop_services()