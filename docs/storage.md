# Joinly Storage Documentation

## Overview

Joinly provides a flexible storage system with multiple backend options and an in-memory cache layer.

## Storage Backends

### SQLite Storage

Default storage backend using SQLite database.

**Features:**
- File-based persistence
- ACID transactions
- SQL query support
- Cross-platform

**Usage:**
```python
from storage.sqlite_store import SQLiteStore
from storage.base import StorageManager

backend = SQLiteStore('joinly.db')
storage = StorageManager(backend)
```

**Configuration:**
```python
storage = SQLiteStore(
    db_path='joinly.db'
)
```

### LevelDB Storage

High-performance key-value storage.

**Features:**
- Fast reads/writes
- Compression
- Efficient for large datasets

**Usage:**
```python
from storage.leveldb_store import LevelDBStore
from storage.base import StorageManager

backend = LevelDBStore('joinly_leveldb')
storage = StorageManager(backend)
```

**Requirements:**
```bash
pip install plyvel
```

### In-Memory Cache

LRU cache for frequently accessed data.

**Features:**
- O(1) access time
- Automatic eviction
- TTL support
- Thread-safe

**Usage:**
```python
from storage.cache import LRUCache

cache = LRUCache(max_size=1000)
cache.set('key', 'value', ttl=300)
value = cache.get('key')
```

## Storage Manager

Unified interface for storage operations.

### Save Lobby

```python
lobby_data = {
    'lobby_id': 'lobby_123',
    'state': 'waiting',
    'players': [...]
}

storage.save_lobby('lobby_123', lobby_data)
```

### Load Lobby

```python
lobby = storage.load_lobby('lobby_123')
```

### Delete Lobby

```python
storage.delete_lobby('lobby_123')
```

### Save Player

```python
player_data = {
    'player_id': 'player_456',
    'username': 'PlayerOne',
    'skill_rating': 1200
}

storage.save_player('player_456', player_data)
```

### Load Player

```python
player = storage.load_player('player_456')
```

### Get All Lobbies

```python
lobby_ids = storage.get_all_lobbies()
```

### Get All Players

```python
player_ids = storage.get_all_players()
```

## Native Storage DLL

C++ implementation for high-performance operations.

### Building

```bash
cd native/storage
cmake .
cmake --build .
```

### Usage

```python
from native.bindings import NativeStorageBinding

storage = NativeStorageBinding('joinly_storage.dll')
storage.set('key', 'value')
value = storage.get('key')
storage.delete('key')
```

## Cache Strategies

### Write-Through

Data written to cache and storage simultaneously.

```python
cache.set('key', 'value')
storage.set('key', 'value')
```

### Write-Behind

Data written to cache first, then asynchronously to storage.

```python
cache.set('key', 'value')
async_queue.put(('key', 'value'))
```

### Read-Through

Check cache first, load from storage on miss.

```python
value = cache.get('key')
if value is None:
    value = storage.get('key')
    cache.set('key', value)
```

## Best Practices

### Data Serialization

Always serialize complex objects:

```python
import json

lobby_json = json.dumps(lobby.to_dict())
storage.set(f'lobby:{lobby_id}', lobby_json)
```

### Key Naming

Use hierarchical keys:

```
lobby:{lobby_id}
player:{player_id}
match:{match_id}
queue:{queue_id}
```

### Cleanup

Periodically clean expired data:

```python
def cleanup_old_data():
    all_lobbies = storage.get_all_lobbies()
    current_time = time.time()
    
    for lobby_id in all_lobbies:
        lobby = storage.load_lobby(lobby_id)
        if current_time - lobby['created_at'] > 86400:
            storage.delete_lobby(lobby_id)
```

### Transactions

Group related operations:

```python
try:
    storage.save_lobby(lobby_id, lobby_data)
    for player in players:
        storage.save_player(player['player_id'], player)
except Exception as e:
    print(f"Transaction failed: {e}")
```

## Performance Tips

1. **Batch Operations**: Group multiple reads/writes
2. **Use Cache**: Cache hot data
3. **Lazy Loading**: Load data when needed
4. **Compression**: Enable for large values
5. **Indexing**: Create indexes for frequent queries

## Monitoring

### Cache Statistics

```python
stats = cache.get_stats()
print(f"Hit rate: {stats['hit_rate']}%")
print(f"Size: {stats['size']}/{stats['max_size']}")
```

### Storage Size

```python
import os

db_size = os.path.getsize('joinly.db')
print(f"Database size: {db_size / 1024 / 1024:.2f} MB")
```

## Backup and Recovery

### Backup

```bash
cp joinly.db joinly_backup_$(date +%Y%m%d).db
```

### Recovery

```python
import shutil

shutil.copy('joinly_backup.db', 'joinly.db')
storage = SQLiteStore('joinly.db')
```

## Migration

### SQLite to LevelDB

```python
from storage.sqlite_store import SQLiteStore
from storage.leveldb_store import LevelDBStore

sqlite = SQLiteStore('joinly.db')
leveldb = LevelDBStore('joinly_leveldb')

for key in sqlite.keys():
    value = sqlite.get(key)
    leveldb.set(key, value)
```