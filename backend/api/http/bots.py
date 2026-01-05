from flask import Blueprint, request, jsonify

bots_bp = Blueprint('bots', __name__)

def init_bots_routes(bot_manager):
    
    @bots_bp.route('/bots', methods=['GET'])
    def get_bots():
        bots = bot_manager.get_all_bots()
        return jsonify({'bots': [b.to_dict() for b in bots]})
    
    @bots_bp.route('/bots', methods=['POST'])
    def create_bot():
        data = request.json
        profile_name = data.get('profile', 'default')
        
        bot = bot_manager.create_bot(profile_name)
        return jsonify({'success': True, 'bot': bot.to_dict()})
    
    @bots_bp.route('/bots/<bot_id>', methods=['GET'])
    def get_bot(bot_id):
        bot = bot_manager.get_bot(bot_id)
        if not bot:
            return jsonify({'error': 'Bot not found'}), 404
        return jsonify({'bot': bot.to_dict()})
    
    @bots_bp.route('/bots/<bot_id>', methods=['DELETE'])
    def delete_bot(bot_id):
        bot_manager.remove_bot(bot_id)
        return jsonify({'success': True})
    
    @bots_bp.route('/lobbies/<lobby_id>/bots', methods=['POST'])
    def add_bot_to_lobby(lobby_id):
        data = request.json
        profile_name = data.get('profile', 'default')
        
        bot = bot_manager.add_bot_to_lobby(lobby_id, profile_name)
        if bot:
            return jsonify({'success': True, 'bot': bot.to_dict()})
        return jsonify({'error': 'Could not add bot'}), 400
    
    @bots_bp.route('/lobbies/<lobby_id>/bots/fill', methods=['POST'])
    def fill_lobby_with_bots(lobby_id):
        data = request.json
        profile_name = data.get('profile', 'default')
        
        bots = bot_manager.fill_lobby_with_bots(lobby_id, profile_name)
        return jsonify({
            'success': True,
            'bots_added': len(bots),
            'bots': [b.to_dict() for b in bots]
        })
    
    @bots_bp.route('/bots/profiles', methods=['GET'])
    def get_bot_profiles():
        profiles = bot_manager.profile_library.get_all_profiles()
        return jsonify({'profiles': profiles})
    
    @bots_bp.route('/bots/stats', methods=['GET'])
    def get_bot_stats():
        stats = bot_manager.get_bot_stats()
        return jsonify({'stats': stats})
    
    return bots_bp