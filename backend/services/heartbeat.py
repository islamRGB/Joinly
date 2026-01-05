import threading
import time

class HeartbeatService:
    def __init__(self, engine):
        self.engine = engine
        self.active = False
        self.tick_rate = 1.0
        self.thread = None
        self.tick_count = 0
    
    def start(self):
        self.active = True
        self.thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        self.active = False
        if self.thread:
            self.thread.join()
    
    def _heartbeat_loop(self):
        while self.active:
            try:
                self.engine.tick()
                self.tick_count += 1
            except Exception as e:
                print(f"Heartbeat error: {e}")
            time.sleep(self.tick_rate)
    
    def get_tick_count(self) -> int:
        return self.tick_count