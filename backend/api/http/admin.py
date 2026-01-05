from flask import Blueprint, request, jsonify
import psutil

admin_bp = Blueprint('admin', __name__)

def init_admin_routes(engine, analytics_service):
    
    @admin_bp.route('/admin/stats', methods=['GET'])
    def get_stats():
        stats = {
            'total_lobbies': len(engine.lobbies),
            'total_players': len(engine.players),
            'total_bots': len(engine.bots),
            'total_parties': len(engine.parties),
            'lobbies': engine.get_all_lobbies()
        }
        return jsonify(stats)
    
    @admin_bp.route('/admin/events', methods=['GET'])
    def get_events():
        limit = request.args.get('limit', 100, type=int)
        events = engine.event_bus.get_history(limit)
        return jsonify({'events': events})
    
    @admin_bp.route('/admin/lobbies/<lobby_id>/kick', methods=['POST'])
    def kick_player(lobby_id):
        data = request.json
        player_id = data.get('player_id')
        
        engine.remove_player_from_lobby(lobby_id, player_id)
        return jsonify({'success': True})
    
    @admin_bp.route('/admin/analytics', methods=['GET'])
    def get_analytics():
        analytics = analytics_service.get_analytics()
        return jsonify({'analytics': analytics})
    
    @admin_bp.route('/admin/system', methods=['GET'])
    def get_system_info():
        import platform
        
        try:
            import psutil
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory().percent
        except:
            cpu_percent = 0
            memory_percent = 0
        
        info = {
            'platform': platform.system(),
            'python_version': platform.python_version(),
            'cpu_percent': cpu_percent,
            'memory_percent': memory_percent,
            'uptime': __import__('time').time() - engine.lobbies.get(list(engine.lobbies.keys())[0]).created_at if engine.lobbies else 0
        }
        return jsonify(info)
    
    @admin_bp.route('/admin/clear', methods=['POST'])
    def clear_all():
        data = request.json
        clear_type = data.get('type', 'all')
        
        if clear_type == 'lobbies' or clear_type == 'all':
            for lobby_id in list(engine.lobbies.keys()):
                engine.delete_lobby(lobby_id)
        
        if clear_type == 'events' or clear_type == 'all':
            engine.event_bus.clear_history()
        
        return jsonify({'success': True})
    
    return admin_bp