from __future__ import annotations

import json
import logging
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

LOG_DIR = Path(".git-toolkit") / "logs"
HISTORY_FILE = Path(".git-toolkit") / "history.json"
CACHE_DIR = Path(".git-toolkit") / "cache"

_SECRET_KEYS = {"token", "password", "secret", "pat", "authorization"}


class ToolkitLogger:
    def __init__(self, name: str = "git-toolkit", level: int = logging.INFO) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()
        self.logger.propagate = False

        self.console_handler = logging.StreamHandler(sys.stdout)
        self.console_handler.setLevel(level)
        self.console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        self.logger.addHandler(self.console_handler)

        try:
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            log_file = LOG_DIR / f"{datetime.now(UTC).strftime('%Y-%m-%d')}.log"
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(
                logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            )
            self.logger.addHandler(file_handler)
        except OSError:
            pass

    def set_level(self, level: int) -> None:
        self.console_handler.setLevel(level)

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.logger.error(msg, *args, **kwargs)


logger = ToolkitLogger()


def _scrub_args(args: dict[str, Any]) -> dict[str, str]:
    scrubbed: dict[str, str] = {}
    for key, value in args.items():
        if key.lower() in _SECRET_KEYS or any(secret in key.lower() for secret in _SECRET_KEYS):
            scrubbed[key] = "***"
        else:
            scrubbed[key] = str(value)
    return scrubbed


def log_execution(
    command: str,
    args: dict[str, Any],
    status: str,
    details: str | None = None,
) -> None:
    """Append a scrubbed execution event to the bounded local journal."""
    try:
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        history: list[dict[str, Any]] = []
        if HISTORY_FILE.exists():
            try:
                loaded = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
                if isinstance(loaded, list):
                    history = loaded
            except (json.JSONDecodeError, OSError):
                history = []

        history.append(
            {
                "timestamp": datetime.now(UTC).isoformat(),
                "command": command,
                "args": _scrub_args(args),
                "status": status,
                "details": details,
            }
        )
        HISTORY_FILE.write_text(json.dumps(history[-100:], indent=2), encoding="utf-8")
    except OSError as exc:
        logger.debug("Failed to write execution history: %s", exc)


def get_history(limit: int = 10) -> list[dict[str, Any]]:
    if not HISTORY_FILE.exists():
        return []
    try:
        loaded = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        if not isinstance(loaded, list):
            return []
        return loaded[-max(0, limit) :]
    except (json.JSONDecodeError, OSError):
        return []


def set_cache(key: str, data: Any, ttl: int = 3600) -> None:
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_file = CACHE_DIR / f"{key}.json"
        cache_file.write_text(
            json.dumps({"timestamp": time.time(), "ttl": ttl, "data": data}),
            encoding="utf-8",
        )
    except (OSError, TypeError) as exc:
        logger.debug("Failed to set cache for %s: %s", key, exc)


def get_cache(key: str) -> Any | None:
    cache_file = CACHE_DIR / f"{key}.json"
    if not cache_file.exists():
        return None
    try:
        entry = json.loads(cache_file.read_text(encoding="utf-8"))
        if time.time() - float(entry.get("timestamp", 0)) > int(entry.get("ttl", 3600)):
            cache_file.unlink(missing_ok=True)
            return None
        return entry.get("data")
    except (json.JSONDecodeError, OSError, TypeError, ValueError) as exc:
        logger.debug("Failed to read cache for %s: %s", key, exc)
        return None


def clear_cache() -> None:
    if not CACHE_DIR.exists():
        return
    try:
        for cache_file in CACHE_DIR.glob("*.json"):
            cache_file.unlink(missing_ok=True)
    except OSError as exc:
        logger.debug("Failed to clear cache: %s", exc)
