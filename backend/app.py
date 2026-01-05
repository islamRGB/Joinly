from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import os
import sys

print("=" * 60)
print("JOINLY SERVER STARTING")
print("=" * 60)

print("\n[1/7] Importing bootstrap...")
try:
    from bootstrap import JoinlyBootstrap
    print("✓ Bootstrap imported")
except Exception as e:
    print(f"✗ Bootstrap import failed: {e}")
    sys.exit(1)

print("[2/7] Importing API routes...")
try:
    from api.http.lobby import init_lobby_routes
    print("  ✓ lobby routes")
    from api.http.matchmaking import init_matchmaking_routes
    print("  ✓ matchmaking routes")
    from api.http.bots import init_bots_routes
    print("  ✓ bots routes")
    from api.http.admin import init_admin_routes
    print("  ✓ admin routes")
    from api.websocket import init_websocket
    print("  ✓ websocket handlers")
    print("✓ API routes imported")
except Exception as e:
    import traceback
    print(f"✗ API import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

print("[3/7] Creating Flask app...")
app = Flask(__name__, static_folder='../frontend-web', static_url_path='')
app.config['SECRET_KEY'] = 'joinly_secret_key'
CORS(app, resources={r"/*": {"origins": "*"}})
print("✓ Flask app created")

print("[4/7] Initializing SocketIO...")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', logger=False, engineio_logger=False)
print("✓ SocketIO initialized")

print("[5/7] Bootstrapping Joinly...")
bootstrap = JoinlyBootstrap()
components = bootstrap.get_components()

engine = components['engine']
matcher = components['matcher']
bot_manager = components['bot_manager']
analytics = components['analytics']
print("✓ Joinly components ready")

print("[6/7] Registering API blueprints...")
lobby_bp = init_lobby_routes(engine)
matchmaking_bp = init_matchmaking_routes(matcher)
bots_bp = init_bots_routes(bot_manager)
admin_bp = init_admin_routes(engine, analytics)

app.register_blueprint(lobby_bp, url_prefix='/api')
app.register_blueprint(matchmaking_bp, url_prefix='/api')
app.register_blueprint(bots_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')
print("✓ API blueprints registered")

print("[7/7] Initializing WebSocket handlers...")
init_websocket(socketio, engine, bot_manager)
print("✓ WebSocket handlers ready")

@app.route('/')
def index():
    try:
        return send_from_directory('../frontend-web', 'index.html')
    except Exception as e:
        return jsonify({'error': 'Frontend not found', 'message': str(e)}), 404

@app.route('/control')
def control_panel():
    try:
        return send_from_directory('../control-ui', 'index.html')
    except Exception as e:
        return jsonify({'error': 'Control panel not found', 'message': str(e)}), 404

@app.route('/lobby.css')
def lobby_css():
    try:
        return send_from_directory('../frontend-web', 'lobby.css')
    except:
        return '', 404

@app.route('/dashboard.css')
def dashboard_css():
    try:
        return send_from_directory('../control-ui', 'dashboard.css')
    except:
        return '', 404

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    try:
        return send_from_directory('../frontend-web/assets', filename)
    except:
        try:
            return send_from_directory('../control-ui/assets', filename)
        except:
            return '', 404

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error', 'message': str(e)}), 500

if __name__ == '__main__':
    print("Starting Joinly server...")
    bootstrap.start_services()
    
    try:
        socketio.run(app, host='0.0.0.0', port=5000, debug=False, log_output=False)
    except KeyboardInterrupt:
        print("\nShutting down...")
        bootstrap.stop_services()