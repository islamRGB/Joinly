import toml
import logging
import colorlog
from logging.handlers import RotatingFileHandler
from core.engine import LobbyEngine
from matchmaking.matcher import Matcher
from bots.bot_manager import BotManager
from services.presence import PresenceService
from services.heartbeat import HeartbeatService
from services.analytics import AnalyticsService
from services.scheduler import SchedulerService
from storage.base import StorageManager
from storage.sqlite_store import SQLiteStore

def setup_logger(name='joinly', level='INFO', log_file='joinly.log'):
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    if logger.hasHandlers():
        logger.handlers.clear()
    
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(name)s%(reset)s - %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10485760,
            backupCount=5
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except:
        pass
    
    return logger

class JoinlyBootstrap:
    def __init__(self):
        self.logger = setup_logger()
        self.config = self._load_config()
        
        self.engine = LobbyEngine()
        self.matcher = Matcher(self.engine)
        self.bot_manager = BotManager(self.engine)
        
        self.presence_service = PresenceService(self.engine)
        self.heartbeat_service = HeartbeatService(self.engine)
        self.analytics_service = AnalyticsService(self.engine)
        self.scheduler_service = SchedulerService()
        
        storage_backend = SQLiteStore()
        self.storage_manager = StorageManager(storage_backend)
        
        self.logger.info("Joinly framework initialized")
    
    def _load_config(self):
        config = {}
        
        try:
            with open('config/lobby.toml', 'r') as f:
                config['lobby'] = toml.load(f)
        except:
            config['lobby'] = {}
        
        try:
            with open('config/matchmaking.toml', 'r') as f:
                config['matchmaking'] = toml.load(f)
        except:
            config['matchmaking'] = {}
        
        try:
            with open('config/admin.toml', 'r') as f:
                config['admin'] = toml.load(f)
        except:
            config['admin'] = {}
        
        return config
    
    def start_services(self):
        self.logger.info("Starting services...")
        
        self.heartbeat_service.start()
        self.presence_service.start()
        self.matcher.start()
        self.scheduler_service.start()
        
        self.scheduler_service.add_job_minutes(5, self._periodic_cleanup)
        
        self.logger.info("All services started")
    
    def stop_services(self):
        self.logger.info("Stopping services...")
        
        self.heartbeat_service.stop()
        self.presence_service.stop()
        self.matcher.stop()
        self.scheduler_service.stop()
        self.storage_manager.close()
        
        self.logger.info("All services stopped")
    
    def _periodic_cleanup(self):
        self.logger.info("Running periodic cleanup")
        
        for queue in self.matcher.queues.values():
            queue.clear_expired_tickets()
    
    def get_components(self):
        return {
            'engine': self.engine,
            'matcher': self.matcher,
            'bot_manager': self.bot_manager,
            'presence': self.presence_service,
            'heartbeat': self.heartbeat_service,
            'analytics': self.analytics_service,
            'scheduler': self.scheduler_service,
            'storage': self.storage_manager
        }