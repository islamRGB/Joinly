from flask import Blueprint, request, jsonify
from matchmaking.tickets import MatchTicket

matchmaking_bp = Blueprint('matchmaking', __name__)

def init_matchmaking_routes(matcher):
    
    @matchmaking_bp.route('/queues', methods=['GET'])
    def get_queues():
        queues = matcher.get_all_queues()
        return jsonify({'queues': queues})
    
    @matchmaking_bp.route('/queues', methods=['POST'])
    def create_queue():
        data = request.json
        queue_id = data.get('queue_id')
        config = data.get('config', {})
        
        queue = matcher.create_queue(queue_id, config)
        return jsonify({'success': True, 'queue': queue.to_dict()})
    
    @matchmaking_bp.route('/queues/<queue_id>', methods=['GET'])
    def get_queue(queue_id):
        queue = matcher.get_queue(queue_id)
        if not queue:
            return jsonify({'error': 'Queue not found'}), 404
        return jsonify({'queue': queue.to_dict()})
    
    @matchmaking_bp.route('/queues/<queue_id>/join', methods=['POST'])
    def join_queue(queue_id):
        data = request.json
        
        ticket = MatchTicket(
            player_id=data.get('player_id'),
            username=data.get('username'),
            skill_rating=data.get('skill_rating', 1000),
            metadata=data.get('metadata', {})
        )
        
        success = matcher.add_ticket(queue_id, ticket)
        if success:
            return jsonify({'success': True, 'ticket': ticket.to_dict()})
        return jsonify({'error': 'Could not join queue'}), 400
    
    @matchmaking_bp.route('/queues/<queue_id>/leave', methods=['POST'])
    def leave_queue(queue_id):
        data = request.json
        ticket_id = data.get('ticket_id')
        
        matcher.remove_ticket(queue_id, ticket_id)
        return jsonify({'success': True})
    
    @matchmaking_bp.route('/tickets/<ticket_id>', methods=['GET'])
    def get_ticket_status(ticket_id):
        for queue in matcher.queues.values():
            ticket = queue.get_ticket(ticket_id)
            if ticket:
                return jsonify({'ticket': ticket.to_dict()})
        
        return jsonify({'error': 'Ticket not found'}), 404
    
    return matchmaking_bp