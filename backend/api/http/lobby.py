from flask import Blueprint, request, jsonify
from core.player import Player

lobby_bp = Blueprint('lobby', __name__)

def init_lobby_routes(engine):
    
    @lobby_bp.route('/lobbies', methods=['GET'])
    def get_lobbies():
        lobbies = engine.get_all_lobbies()
        return jsonify({'lobbies': lobbies})
    
    @lobby_bp.route('/lobbies', methods=['POST'])
    def create_lobby():
        data = request.json
        lobby_id = data.get('lobby_id', f"lobby_{int(__import__('time').time())}")
        config = data.get('config', {})
        
        lobby = engine.create_lobby(lobby_id, config)
        return jsonify({'success': True, 'lobby': lobby.to_dict()})
    
    @lobby_bp.route('/lobbies/<lobby_id>', methods=['GET'])
    def get_lobby(lobby_id):
        lobby = engine.get_lobby(lobby_id)
        if not lobby:
            return jsonify({'error': 'Lobby not found'}), 404
        return jsonify({'lobby': lobby.to_dict()})
    
    @lobby_bp.route('/lobbies/<lobby_id>', methods=['DELETE'])
    def delete_lobby(lobby_id):
        engine.delete_lobby(lobby_id)
        return jsonify({'success': True})
    
    @lobby_bp.route('/lobbies/<lobby_id>/join', methods=['POST'])
    def join_lobby(lobby_id):
        data = request.json
        player = Player(
            player_id=data.get('player_id'),
            username=data.get('username'),
            metadata=data.get('metadata', {})
        )
        
        success = engine.add_player_to_lobby(lobby_id, player)
        if success:
            return jsonify({'success': True, 'player': player.to_dict()})
        return jsonify({'error': 'Could not join lobby'}), 400
    
    @lobby_bp.route('/lobbies/<lobby_id>/leave', methods=['POST'])
    def leave_lobby(lobby_id):
        data = request.json
        player_id = data.get('player_id')
        
        engine.remove_player_from_lobby(lobby_id, player_id)
        return jsonify({'success': True})
    
    @lobby_bp.route('/lobbies/<lobby_id>/ready', methods=['POST'])
    def set_ready(lobby_id):
        data = request.json
        player_id = data.get('player_id')
        ready = data.get('ready', True)
        
        engine.set_player_ready(lobby_id, player_id, ready)
        return jsonify({'success': True})
    
    @lobby_bp.route('/players', methods=['GET'])
    def get_players():
        players = engine.get_all_players()
        return jsonify({'players': [p.to_dict() for p in players]})
    
    @lobby_bp.route('/players/<player_id>', methods=['GET'])
    def get_player(player_id):
        player = engine.get_player(player_id)
        if not player:
            return jsonify({'error': 'Player not found'}), 404
        return jsonify({'player': player.to_dict()})
    
    return lobby_bp