import ctypes
import os
from typing import Optional

class NativeStorageBinding:
    def __init__(self, dll_path: str = 'joinly_storage.dll'):
        self.dll_path = dll_path
        self.lib = None
        
        if os.path.exists(dll_path):
            try:
                self.lib = ctypes.CDLL(dll_path)
                self._setup_functions()
            except Exception as e:
                print(f"Failed to load storage DLL: {e}")
    
    def _setup_functions(self):
        if not self.lib:
            return
        
        self.lib.native_set.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.lib.native_set.restype = ctypes.c_int
        
        self.lib.native_get.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
        self.lib.native_get.restype = ctypes.c_int
        
        self.lib.native_delete.argtypes = [ctypes.c_char_p]
        self.lib.native_delete.restype = ctypes.c_int
    
    def set(self, key: str, value: str) -> bool:
        if not self.lib:
            return False
        
        key_bytes = key.encode('utf-8')
        value_bytes = value.encode('utf-8')
        result = self.lib.native_set(key_bytes, value_bytes)
        return result == 0
    
    def get(self, key: str) -> Optional[str]:
        if not self.lib:
            return None
        
        key_bytes = key.encode('utf-8')
        buffer = ctypes.create_string_buffer(4096)
        result = self.lib.native_get(key_bytes, buffer, 4096)
        
        if result == 0:
            return buffer.value.decode('utf-8')
        return None
    
    def delete(self, key: str) -> bool:
        if not self.lib:
            return False
        
        key_bytes = key.encode('utf-8')
        result = self.lib.native_delete(key_bytes)
        return result == 0

class NativeCryptoBinding:
    def __init__(self, dll_path: str = 'joinly_crypto.dll'):
        self.dll_path = dll_path
        self.lib = None
        
        if os.path.exists(dll_path):
            try:
                self.lib = ctypes.CDLL(dll_path)
                self._setup_functions()
            except Exception as e:
                print(f"Failed to load crypto DLL: {e}")
    
    def _setup_functions(self):
        if not self.lib:
            return
        
        self.lib.hash_password.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
        self.lib.hash_password.restype = ctypes.c_int
        
        self.lib.verify_password.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.lib.verify_password.restype = ctypes.c_int
    
    def hash_password(self, password: str) -> Optional[str]:
        if not self.lib:
            return None
        
        password_bytes = password.encode('utf-8')
        buffer = ctypes.create_string_buffer(256)
        result = self.lib.hash_password(password_bytes, buffer, 256)
        
        if result == 0:
            return buffer.value.decode('utf-8')
        return None
    
    def verify_password(self, password: str, hash_str: str) -> bool:
        if not self.lib:
            return False
        
        password_bytes = password.encode('utf-8')
        hash_bytes = hash_str.encode('utf-8')
        result = self.lib.verify_password(password_bytes, hash_bytes)
        return result == 0