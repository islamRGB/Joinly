# Joinly API Documentation

## Base URL

```
http://localhost:5000/api
```

## Lobby Endpoints

### Get All Lobbies

```http
GET /lobbies
```

**Response:**
```json
{
  "lobbies": [
    {
      "lobby_id": "lobby_123",
      "state": "waiting",
      "player_count": 3,
      "bot_count": 1,
      "max_players": 10,
      "max_bots": 4,
      "players": [...],
      "bots": [...]
    }
  ]
}
```

### Create Lobby

```http
POST /lobbies
```

**Request Body:**
```json
{
  "lobby_id": "my_lobby",
  "config": {
    "max_players": 10,
    "max_bots": 4,
    "require_all_ready": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "lobby": {...}
}
```

### Get Lobby Details

```http
GET /lobbies/{lobby_id}
```

**Response:**
```json
{
  "lobby": {
    "lobby_id": "lobby_123",
    "state": "waiting",
    "players": [...],
    "bots": [...]
  }
}
```

### Delete Lobby

```http
DELETE /lobbies/{lobby_id}
```

**Response:**
```json
{
  "success": true
}
```

### Join Lobby

```http
POST /lobbies/{lobby_id}/join
```

**Request Body:**
```json
{
  "player_id": "player_456",
  "username": "PlayerOne",
  "metadata": {
    "skill_rating": 1200
  }
}
```

**Response:**
```json
{
  "success": true,
  "player": {
    "player_id": "player_456",
    "username": "PlayerOne",
    "ready": false
  }
}
```

### Leave Lobby

```http
POST /lobbies/{lobby_id}/leave
```

**Request Body:**
```json
{
  "player_id": "player_456"
}
```

### Set Ready Status

```http
POST /lobbies/{lobby_id}/ready
```

**Request Body:**
```json
{
  "player_id": "player_456",
  "ready": true
}
```

## Matchmaking Endpoints

### Get All Queues

```http
GET /queues
```

**Response:**
```json
{
  "queues": [
    {
      "queue_id": "casual",
      "players_per_match": 10,
      "queue_length": 5,
      "average_wait_time": 45.2
    }
  ]
}
```

### Create Queue

```http
POST /queues
```

**Request Body:**
```json
{
  "queue_id": "ranked",
  "config": {
    "players_per_match": 10,
    "max_skill_diff": 100,
    "team_mode": true,
    "team_size": 5
  }
}
```

### Join Queue

```http
POST /queues/{queue_id}/join
```

**Request Body:**
```json
{
  "player_id": "player_456",
  "username": "PlayerOne",
  "skill_rating": 1200
}
```

**Response:**
```json
{
  "success": true,
  "ticket": {
    "ticket_id": "ticket_789",
    "status": "queued",
    "wait_time": 0
  }
}
```

### Leave Queue

```http
POST /queues/{queue_id}/leave
```

**Request Body:**
```json
{
  "ticket_id": "ticket_789"
}
```

### Get Ticket Status

```http
GET /tickets/{ticket_id}
```

**Response:**
```json
{
  "ticket": {
    "ticket_id": "ticket_789",
    "status": "queued",
    "wait_time": 23.4
  }
}
```

## Bot Endpoints

### Get All Bots

```http
GET /bots
```

### Create Bot

```http
POST /bots
```

**Request Body:**
```json
{
  "profile": "expert"
}
```

### Delete Bot

```http
DELETE /bots/{bot_id}
```

### Add Bot to Lobby

```http
POST /lobbies/{lobby_id}/bots
```

**Request Body:**
```json
{
  "profile": "intermediate"
}
```

### Fill Lobby with Bots

```http
POST /lobbies/{lobby_id}/bots/fill
```

**Request Body:**
```json
{
  "profile": "default"
}
```

### Get Bot Profiles

```http
GET /bots/profiles
```

**Response:**
```json
{
  "profiles": {
    "default": {...},
    "beginner": {...},
    "expert": {...}
  }
}
```

## Admin Endpoints

### Get System Stats

```http
GET /admin/stats
```

**Response:**
```json
{
  "total_lobbies": 5,
  "total_players": 23,
  "total_bots": 8,
  "lobbies": [...]
}
```

### Get Event History

```http
GET /admin/events?limit=100
```

**Response:**
```json
{
  "events": [
    {
      "event": "player_joined",
      "data": {...},
      "timestamp": 1234567890
    }
  ]
}
```

### Get Analytics

```http
GET /admin/analytics
```

**Response:**
```json
{
  "analytics": {
    "uptime_seconds": 3600,
    "total_lobbies": 10,
    "event_counts": {...}
  }
}
```

### Kick Player

```http
POST /admin/lobbies/{lobby_id}/kick
```

**Request Body:**
```json
{
  "player_id": "player_456"
}
```

### Clear Data

```http
POST /admin/clear
```

**Request Body:**
```json
{
  "type": "lobbies"
}
```

## WebSocket Events

### Connect to WebSocket

```javascript
const socket = io('http://localhost:5000');
```

### Client Events

#### Join Lobby
```javascript
socket.emit('join_lobby', {
  lobby_id: 'lobby_123',
  player_id: 'player_456',
  username: 'PlayerOne'
});
```

#### Leave Lobby
```javascript
socket.emit('leave_lobby', {
  lobby_id: 'lobby_123',
  player_id: 'player_456'
});
```

#### Set Ready
```javascript
socket.emit('set_ready', {
  lobby_id: 'lobby_123',
  player_id: 'player_456',
  ready: true
});
```

#### Add Bot
```javascript
socket.emit('add_bot', {
  lobby_id: 'lobby_123',
  profile: 'expert'
});
```

### Server Events

#### Lobby State
```javascript
socket.on('lobby_state', (data) => {
  console.log(data);
});
```

#### Player Joined
```javascript
socket.on('player_joined', (data) => {
  console.log(data.player_id);
});
```

#### Player Left
```javascript
socket.on('player_left', (data) => {
  console.log(data.player_id);
});
```

#### Player Ready
```javascript
socket.on('player_ready', (data) => {
  console.log(data.player_id, data.ready);
});
```

## Error Responses

All endpoints may return error responses:

```json
{
  "error": "Error message",
  "code": "ERROR_CODE"
}
```

Common HTTP status codes:
- `200` - Success
- `400` - Bad request
- `404` - Not found
- `500` - Server error