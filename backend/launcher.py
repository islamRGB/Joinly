import webbrowser
import time
import sys
import os

def check_dependencies():
    required = ['flask', 'flask_cors', 'flask_socketio', 'toml']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    return missing

def launch_joinly():
    print("=" * 50)
    print("  JOINLY - Multiplayer Lobby Framework")
    print("=" * 50)
    print()
    
    print("Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"\n✗ Missing packages: {', '.join(missing)}")
        print("\nPlease install dependencies first:")
        print("  pip install -r requirements.txt")
        print("\nOr use Joinly.py launcher for automatic installation.")
        input("\nPress Enter to exit...")
        return
    
    print("✓ All dependencies found")
    print()
    
    print("Opening control panel in 2 seconds...")
    time.sleep(2)
    webbrowser.open('http://localhost:5000/control')
    
    print()
    print("Control Panel: http://localhost:5000/control")
    print("Player UI: http://localhost:5000")
    print("API Docs: http://localhost:5000/api")
    print()
    print("Press Ctrl+C to stop the server")
    print()
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        import app
        from flask_socketio import SocketIO
        
        app.bootstrap.start_services()
        app.socketio.run(app.app, host='0.0.0.0', port=5000, debug=False, log_output=False)
        
    except KeyboardInterrupt:
        print("\nShutting down Joinly...")
        app.bootstrap.stop_services()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")

if __name__ == '__main__':
    launch_joinly()