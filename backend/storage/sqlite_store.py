import sqlite3
from typing import Optional, List
from .base import StorageBackend

class SQLiteStore(StorageBackend):
    def __init__(self, db_path: str = 'joinly.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS storage (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def disconnect(self):
        if self.conn:
            self.conn.close()
    
    def set(self, key: str, value: str) -> bool:
        try:
            self.cursor.execute(
                'INSERT OR REPLACE INTO storage (key, value) VALUES (?, ?)',
                (key, value)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"SQLite set error: {e}")
            return False
    
    def get(self, key: str) -> Optional[str]:
        try:
            self.cursor.execute('SELECT value FROM storage WHERE key = ?', (key,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"SQLite get error: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        try:
            self.cursor.execute('DELETE FROM storage WHERE key = ?', (key,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"SQLite delete error: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        try:
            self.cursor.execute('SELECT 1 FROM storage WHERE key = ?', (key,))
            return self.cursor.fetchone() is not None
        except:
            return False
    
    def keys(self, pattern: str = '*') -> List[str]:
        try:
            if pattern == '*':
                self.cursor.execute('SELECT key FROM storage')
            else:
                sql_pattern = pattern.replace('*', '%')
                self.cursor.execute('SELECT key FROM storage WHERE key LIKE ?', (sql_pattern,))
            
            results = self.cursor.fetchall()
            return [row[0] for row in results]
        except Exception as e:
            print(f"SQLite keys error: {e}")
            return []
    
    def clear(self):
        try:
            self.cursor.execute('DELETE FROM storage')
            self.conn.commit()
        except Exception as e:
            print(f"SQLite clear error: {e}")