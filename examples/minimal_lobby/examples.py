import sys
sys.path.append('../../backend')

from bootstrap import JoinlyBootstrap
from core.player import Player
import time

bootstrap = JoinlyBootstrap()
bootstrap.start_services()

engine = bootstrap.engine

print("Creating lobby...")
lobby = engine.create_lobby('example_lobby', {
    'max_players': 4,
    'max_bots': 2,
    'require_all_ready': True
})

print(f"Lobby created: {lobby.lobby_id}")

print("\nAdding players...")
for i in range(3):
    player = Player(
        player_id=f'player_{i}',
        username=f'Player{i}',
        metadata={'skill_rating': 1000 + i * 100}
    )
    engine.add_player_to_lobby(lobby.lobby_id, player)
    print(f"Added {player.username}")

print("\nLobby state:")
print(f"Players: {lobby.get_player_count()}/{lobby.max_players}")
print(f"State: {lobby.state}")

print("\nSetting players ready...")
for player_id in lobby.players:
    engine.set_player_ready(lobby.lobby_id, player_id, True)
    print(f"{player_id} is ready")

time.sleep(1)

print("\nFinal lobby state:")
print(f"State: {lobby.state}")
print(f"All ready: {lobby.check_all_ready()}")

print("\nExample complete!")
bootstrap.stop_services()