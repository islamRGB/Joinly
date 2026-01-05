# Joinly - Open Source Multiplayer Lobby Framework

Joinly is a comprehensive, production-ready multiplayer lobby system with matchmaking, bot support, and real-time synchronization.

## Features

- **Lobby Management**: Create, join, and manage multiplayer lobbies
- **Matchmaking System**: Skill-based matchmaking with configurable queues
- **Bot Support**: AI players with multiple difficulty levels and behaviors
- **Real-time Updates**: WebSocket support for instant state synchronization
- **Party System**: Group players together in parties
- **Permissions**: Role-based access control
- **Storage**: Multiple backend options (SQLite, LevelDB)
- **Control Panel**: Web-based admin dashboard
- **Cross-platform**: Web, Flutter mobile/desktop clients

## Quick Start

### Installation

```bash
pip install -r backend/requirements.txt
```

### Running the Server

```bash
cd backend
python launcher.py
```

This will:
- Start the Joinly server on `http://localhost:5000`
- Open the control panel automatically
- Expose REST and WebSocket APIs

## Project Structure

```
joinly/
├── backend/          # Python server implementation
├── control-ui/       # Admin dashboard
├── frontend-web/     # Web player client
├── frontend-flutter/ # Mobile/desktop client
├── native/           # C++ native extensions
└── docs/             # Documentation
```

## API Endpoints

### Lobbies

- `GET /api/lobbies` - List all lobbies
- `POST /api/lobbies` - Create a lobby
- `GET /api/lobbies/{id}` - Get lobby details
- `DELETE /api/lobbies/{id}` - Delete a lobby
- `POST /api/lobbies/{id}/join` - Join a lobby
- `POST /api/lobbies/{id}/leave` - Leave a lobby
- `POST /api/lobbies/{id}/ready` - Set ready status

### Matchmaking

- `GET /api/queues` - List matchmaking queues
- `POST /api/queues` - Create a queue
- `POST /api/queues/{id}/join` - Join matchmaking
- `POST /api/queues/{id}/leave` - Leave matchmaking

### Bots

- `GET /api/bots` - List all bots
- `POST /api/bots` - Create a bot
- `DELETE /api/bots/{id}` - Remove a bot
- `POST /api/lobbies/{id}/bots` - Add bot to lobby

### Admin

- `GET /api/admin/stats` - System statistics
- `GET /api/admin/events` - Event history
- `GET /api/admin/analytics` - Analytics data

## WebSocket Events

### Client → Server

- `join_lobby` - Join a lobby
- `leave_lobby` - Leave a lobby
- `set_ready` - Update ready status
- `add_bot` - Add a bot to lobby
- `create_lobby` - Create new lobby

### Server → Client

- `lobby_state` - Current lobby state
- `player_joined` - Player joined event
- `player_left` - Player left event
- `player_ready` - Ready status changed
- `bot_added` - Bot added to lobby

## Configuration

Edit configuration files in `backend/config/`:

- `lobby.toml` - Lobby settings
- `matchmaking.toml` - Matchmaking queues
- `admin.toml` - Server configuration

## Bot Profiles

- **Default**: Balanced bot (1000 skill rating)
- **Beginner**: Easy bot (500-800 rating)
- **Intermediate**: Medium bot (900-1200 rating)
- **Expert**: Hard bot (1400-1800 rating)
- **Master**: Expert bot (1900-2500 rating)

## Development

### Backend Development

```bash
cd backend
python app.py
```

### Frontend Development

Web client: Open `frontend-web/index.html`

Flutter client:
```bash
cd frontend-flutter
flutter run
```

### Building Native Extensions

```bash
cd native/storage
cmake .
cmake --build .
```

## Architecture

Joinly uses:
- **Flask** for HTTP API
- **Flask-SocketIO** for WebSocket
- **SQLite/LevelDB** for persistence
- **Event-driven** architecture
- **Plugin-based** bot system

## Examples

See `examples/` directory for:
- Minimal lobby setup
- Bot-heavy lobby configuration
- Custom matchmaking rules

## License

MIT License - See LICENSE file

## Credits

**Made by [emodi](https://emodi.me)**

Framework designed for multiplayer game developers

---

For detailed documentation, see the `docs/` directory.