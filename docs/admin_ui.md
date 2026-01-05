# Joinly Control Panel Documentation

## Overview

The Joinly Control Panel is a web-based admin dashboard for managing lobbies, players, bots, matchmaking, and monitoring system events.

## Accessing the Control Panel

### URL

```
http://localhost:5000/control
```

### Auto-Launch

The control panel opens automatically when running:

```bash
python launcher.py
```

## Dashboard Overview

### Header

Displays real-time statistics:
- **Lobbies**: Total active lobbies
- **Players**: Total connected players
- **Bots**: Total active bots

### Sidebar Navigation

Five main panels:
1. Lobbies
2. Players
3. Bots
4. Matchmaking
5. Logs

## Lobbies Panel

### Features

- View all active lobbies
- Create new lobbies
- View lobby details
- Delete lobbies
- Monitor lobby state

### Actions

**Create Lobby:**
1. Click "+ Create Lobby" button
2. Lobby is created with default configuration
3. Appears in lobby list

**View Lobby:**
1. Click "View" on any lobby card
2. See detailed lobby information

**Delete Lobby:**
1. Click "Delete" on lobby card
2. Lobby and all players are removed

### Lobby Cards

Each card displays:
- Lobby ID
- Current state (waiting/ready)
- Player count / max players
- Bot count / max bots

## Players Panel

### Features

- View all connected players
- See player details
- Monitor connection status
- View skill ratings

### Player Information

Each player card shows:
- Username
- Player ID
- Skill rating
- Ready status
- Connection status (Online/Offline)

## Bots Panel

### Features

- View all active bots
- Create new bots
- Select bot profiles
- Remove bots

### Creating Bots

1. Select bot profile from dropdown:
   - Default
   - Beginner
   - Intermediate
   - Expert
   - Master

2. Click "+ Create Bot"

3. Bot is created and appears in list

### Bot Information

Each bot card displays:
- Bot username
- Behavior type
- Skill rating
- Ready status

## Matchmaking Panel

### Features

- View matchmaking queues
- Create new queues
- Monitor queue statistics
- Track wait times

### Queue Information

Each queue card shows:
- Queue ID
- Players per match
- Current queue length
- Average wait time

### Creating Queues

1. Click "+ Create Queue"
2. Queue is created with default settings
3. Players can join via API

## Logs Panel

### Features

- Real-time event monitoring
- Event history
- Event filtering
- Clear logs

### Event Types

- lobby_created
- lobby_deleted
- player_joined
- player_left
- player_ready_changed
- bot_joined
- bot_left
- match_created
- lobby_all_ready

### Event Details

Each log entry shows:
- Timestamp
- Event name
- Event data (JSON)

### Clearing Logs

Click "Clear Logs" to remove all log entries.

## Real-Time Updates

### Auto-Refresh

Dashboard automatically refreshes every 5 seconds to show:
- New lobbies
- Player joins/leaves
- Bot additions
- Queue updates

### WebSocket Integration

Real-time updates via WebSocket for instant notifications.

## Customization

### Theme

The control panel uses a dark blue tech theme:
- Background: Dark gradient
- Primary color: #4FC3F7 (cyan blue)
- Cards: Dark blue with rounded corners
- Hover effects: Smooth transitions

### Branding

Footer includes:
- "Made by emodi" watermark
- Link to emodi.me

## Keyboard Shortcuts

- `Ctrl+R`: Refresh data
- `Esc`: Close modals

## Mobile Support

Responsive design adapts to:
- Desktop (1920x1080+)
- Tablet (768x1024)
- Mobile (375x667)

## API Integration

Control panel communicates with backend via:

### REST API

```javascript
fetch('/api/lobbies')
fetch('/api/players')
fetch('/api/bots')
fetch('/api/queues')
fetch('/api/admin/events')
```

### WebSocket

```javascript
socket.on('lobby_state', updateLobby)
socket.on('player_joined', refreshPlayers)
```

## Troubleshooting

### Connection Issues

If dashboard doesn't load:
1. Check server is running: `python app.py`
2. Verify port 5000 is available
3. Check firewall settings

### Data Not Updating

If data is stale:
1. Check console for errors
2. Verify WebSocket connection
3. Manually refresh with F5

### CORS Errors

If seeing CORS errors:
1. Ensure CORS is enabled in `admin.toml`
2. Check allowed origins
3. Restart server

## Performance

### Optimization

- Lazy loading for large lists
- Pagination for events (100 per page)
- Efficient DOM updates
- Debounced refresh

### Resource Usage

- Minimal JavaScript
- No external dependencies (except Socket.IO)
- Optimized CSS
- Fast load time (<1s)

## Security

### Access Control

Currently no authentication (add in production):

```python
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    return username == 'admin' and password == 'secret'

@app.route('/control')
@auth.login_required
def control_panel():
    return render_template('control.html')
```

### HTTPS

Enable HTTPS in production:

```python
socketio.run(app, 
    host='0.0.0.0', 
    port=5000,
    certfile='cert.pem',
    keyfile='key.pem'
)
```