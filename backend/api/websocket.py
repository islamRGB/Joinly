from flask_socketio import SocketIO, emit, join_room, leave_room
from core.player import Player

def init_websocket(socketio, engine, bot_manager):
    
    @socketio.on('connect')
    def handle_connect():
        emit('connected', {'message': 'Connected to Joinly'})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        pass
    
    @socketio.on('create_lobby')
    def handle_create_lobby(data):
        lobby_id = data.get('lobby_id', f"lobby_{int(__import__('time').time())}")
        config = data.get('config', {})
        
        lobby = engine.create_lobby(lobby_id, config)
        emit('lobby_created', lobby.to_dict())
    
    @socketio.on('join_lobby')
    def handle_join_lobby(data):
        lobby_id = data.get('lobby_id')
        player = Player(
            player_id=data.get('player_id'),
            username=data.get('username'),
            metadata=data.get('metadata', {})
        )
        
        success = engine.add_player_to_lobby(lobby_id, player)
        if success:
            join_room(lobby_id)
            emit('player_joined', player.to_dict(), room=lobby_id, broadcast=True)
            
            lobby = engine.get_lobby(lobby_id)
            emit('lobby_state', lobby.to_dict())
        else:
            emit('error', {'message': 'Could not join lobby'})
    
    @socketio.on('leave_lobby')
    def handle_leave_lobby(data):
        lobby_id = data.get('lobby_id')
        player_id = data.get('player_id')
        
        engine.remove_player_from_lobby(lobby_id, player_id)
        leave_room(lobby_id)
        emit('player_left', {'player_id': player_id}, room=lobby_id, broadcast=True)
    
    @socketio.on('set_ready')
    def handle_set_ready(data):
        lobby_id = data.get('lobby_id')
        player_id = data.get('player_id')
        ready = data.get('ready', True)
        
        engine.set_player_ready(lobby_id, player_id, ready)
        emit('player_ready', {'player_id': player_id, 'ready': ready}, room=lobby_id, broadcast=True)
        
        lobby = engine.get_lobby(lobby_id)
        if lobby:
            emit('lobby_state', lobby.to_dict(), room=lobby_id, broadcast=True)
    
    @socketio.on('add_bot')
    def handle_add_bot(data):
        lobby_id = data.get('lobby_id')
        profile = data.get('profile', 'default')
        
        bot = bot_manager.add_bot_to_lobby(lobby_id, profile)
        if bot:
            emit('bot_added', bot.to_dict(), room=lobby_id, broadcast=True)
            
            lobby = engine.get_lobby(lobby_id)
            emit('lobby_state', lobby.to_dict(), room=lobby_id, broadcast=True)
    
    @socketio.on('get_lobby')
    def handle_get_lobby(data):
        lobby_id = data.get('lobby_id')
        lobby = engine.get_lobby(lobby_id)
        
        if lobby:
            emit('lobby_state', lobby.to_dict())
        else:
            emit('error', {'message': 'Lobby not found'})
    
    @socketio.on('get_lobbies')
    def handle_get_lobbies():
        lobbies = engine.get_all_lobbies()
        emit('lobbies_list', {'lobbies': lobbies})
    
    def broadcast_event(event_data):
        event_name = event_data.get('event')
        data = event_data.get('data', {})
        
        if 'lobby_id' in data:
            emit(event_name, data, room=data['lobby_id'], namespace='/', broadcast=True)
    
    engine.event_bus.on('player_joined', broadcast_event)
    engine.event_bus.on('player_left', broadcast_event)
    engine.event_bus.on('player_ready_changed', broadcast_event)
    engine.event_bus.on('bot_joined', broadcast_event)
    engine.event_bus.on('lobby_all_ready', broadcast_event)