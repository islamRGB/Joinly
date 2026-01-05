# Joinly Architecture

## Overview

Joinly is built with a modular, event-driven architecture that separates concerns into distinct layers.

## Core Components

### 1. Lobby Engine (`core/engine.py`)

The central component managing all lobbies, players, and bots.

**Responsibilities:**
- Lobby lifecycle management
- Player/bot registration
- State synchronization
- Event emission

**Key Methods:**
- `create_lobby()` - Creates new lobby instances
- `add_player_to_lobby()` - Adds player with rule validation
- `set_player_ready()` - Updates ready state
- `tick()` - Updates all lobby states

### 2. Matchmaking System (`matchmaking/`)

Handles skill-based matchmaking and queue management.

**Components:**
- **Matcher**: Finds matches from queues
- **Queues**: Manages player tickets
- **Balancer**: Creates balanced teams
- **Tickets**: Represents matchmaking requests

**Algorithm:**
- Sort players by skill rating
- Group within skill threshold
- Balance teams if team mode enabled
- Create lobby and assign players

### 3. Bot System (`bots/`)

AI players with configurable behavior.

**Components:**
- **BotManager**: Bot lifecycle management
- **BotProfiles**: Predefined bot configurations
- **BehaviorController**: Executes bot behaviors

**Behaviors:**
- Normal: Standard timing
- Aggressive: Quick actions
- Passive: Delayed actions
- Random: Unpredictable timing

### 4. Storage Layer (`storage/`)

Persistent data storage with multiple backends.

**Implementations:**
- SQLite: Relational storage
- LevelDB: Key-value storage
- Cache: In-memory LRU cache

**Interface:**
```python
get(key) -> value
set(key, value)
delete(key)
keys(pattern) -> list
```

### 5. Event System (`core/events.py`)

Pub/sub event bus for loose coupling.

**Features:**
- Event listeners
- Event history
- Async event handling

**Event Flow:**
```
Action → Engine → Event Bus → Listeners → Services
```

### 6. API Layer (`api/`)

HTTP REST and WebSocket endpoints.

**HTTP Routes:**
- Lobby management
- Matchmaking
- Bot control
- Admin operations

**WebSocket Events:**
- Real-time state updates
- Bidirectional communication
- Room-based broadcasting

### 7. Services Layer (`services/`)

Background services for system operations.

**Services:**
- **Presence**: Player connection monitoring
- **Heartbeat**: System tick updates
- **Analytics**: Metrics collection
- **Scheduler**: Periodic tasks

## Data Flow

### Player Joins Lobby

```
Client → HTTP POST /api/lobbies/{id}/join
  → Engine.add_player_to_lobby()
    → RuleEngine.can_join()
      → Lobby.add_player()
        → EventBus.emit('player_joined')
          → WebSocket broadcast
            → All clients receive update
```

### Matchmaking Flow

```
Player → Queue.add_ticket()
  → Matcher (background thread)
    → Find compatible tickets
      → Balancer.balance_teams()
        → Engine.create_lobby()
          → Add all players
            → Notify players
```

## Concurrency

- Thread-safe with `threading.RLock()`
- Background threads for services
- Non-blocking WebSocket I/O

## Scalability

**Current Design:**
- Single-process architecture
- In-memory state
- Suitable for 100s of concurrent players

**Future Scaling:**
- Redis for distributed state
- Message queue for events
- Horizontal scaling with load balancer

## Extension Points

1. **Custom Rules**: Extend `RuleEngine`
2. **Bot Behaviors**: Add to `BehaviorController`
3. **Storage Backends**: Implement `StorageBackend`
4. **Event Handlers**: Subscribe to event bus
5. **API Endpoints**: Add Flask blueprints

## Configuration

Separated into TOML files:
- `lobby.toml` - Lobby settings
- `matchmaking.toml` - Queue configs
- `admin.toml` - System settings

## Security Considerations

- Input validation on all endpoints
- Rate limiting (future)
- Authentication (future)
- WebSocket origin checking

## Performance

**Optimizations:**
- LRU cache for frequent reads
- Batch operations where possible
- Efficient data structures (dicts for O(1) lookup)
- Minimal lock contention

## Testing Strategy

- Unit tests for core logic
- Integration tests for API
- Load tests for concurrency
- End-to-end tests with clients