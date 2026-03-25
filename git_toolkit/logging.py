import logging
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

# Default log directory
LOG_DIR = Path(".git-toolkit") / "logs"
HISTORY_FILE = Path(".git-toolkit") / "history.json"
CACHE_DIR = Path(".git-toolkit") / "cache"

class ToolkitLogger:
    def __init__(self, name="git-toolkit", level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG) # Allow all levels, handle filtering in handlers
        self.logger.handlers = [] # Clear existing handlers

        # Console handler
        self.console_handler = logging.StreamHandler(sys.stdout)
        self.console_handler.setLevel(level)
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        self.console_handler.setFormatter(formatter)
        self.logger.addHandler(self.console_handler)

        # File handler (debug log)
        try:
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            log_file = LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.log"
            self.file_handler = logging.FileHandler(log_file)
            self.file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.file_handler.setFormatter(file_formatter)
            self.logger.addHandler(self.file_handler)
        except Exception:
            # Fallback if file logging fails
            pass

    def set_level(self, level):
        self.console_handler.setLevel(level)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

# Global logger instance
logger = ToolkitLogger()

def log_execution(command: str, args: Dict[str, Any], status: str, details: Optional[str] = None):
    """Logs an execution to the history file."""
    try:
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        history = []
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, 'r') as f:
                    history = json.load(f)
            except json.JSONDecodeError:
                history = []

        entry = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "args": {k: str(v) for k, v in args.items() if k != 'token'}, # Basic scrubbing
            "status": status,
            "details": details
        }
        
        history.append(entry)
        
        # Keep only the last 100 entries
        history = history[-100:]
        
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
            
    except Exception as e:
        logger.debug(f"Failed to log execution to history: {e}")

def get_history(limit: int = 10) -> list:
    """Retrieves execution history."""
    if not HISTORY_FILE.exists():
        return []
    
    try:
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
            return history[-limit:]
    except (json.JSONDecodeError, IOError):
        return []

def set_cache(key: str, data: Any, ttl: int = 3600):
    """Sets a value in the cache with a given TTL (in seconds)."""
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_file = CACHE_DIR / f"{key}.json"
        
        cache_entry = {
            "timestamp": time.time(),
            "ttl": ttl,
            "data": data
        }
        
        with open(cache_file, 'w') as f:
            json.dump(cache_entry, f)
            
    except Exception as e:
        logger.debug(f"Failed to set cache for {key}: {e}")

def get_cache(key: str) -> Optional[Any]:
    """Retrieves a value from the cache if it exists and is not expired."""
    cache_file = CACHE_DIR / f"{key}.json"
    if not cache_file.exists():
        return None
        
    try:
        with open(cache_file, 'r') as f:
            cache_entry = json.load(f)
            
        timestamp = cache_entry.get("timestamp", 0)
        ttl = cache_entry.get("ttl", 3600)
        
        if time.time() - timestamp > ttl:
            cache_file.unlink() # Delete expired cache
            return None
            
        return cache_entry.get("data")
    except (json.JSONDecodeError, IOError, OSError) as e:
        logger.debug(f"Failed to read cache for {key}: {e}")
        return None

def clear_cache():
    """Clears all cached data."""
    if not CACHE_DIR.exists():
        return
        
    try:
        for cache_file in CACHE_DIR.glob("*.json"):
            cache_file.unlink()
    except Exception as e:
        logger.debug(f"Failed to clear cache: {e}")
