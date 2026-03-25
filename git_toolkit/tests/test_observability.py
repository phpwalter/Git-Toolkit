import pytest
import json
import os
from pathlib import Path
from git_toolkit.logging import ToolkitLogger, log_execution, get_history, HISTORY_FILE

def test_logger_creation(tmp_path, monkeypatch):
    # Mock LOG_DIR to use tmp_path
    log_dir = tmp_path / "logs"
    monkeypatch.setattr("git_toolkit.logging.LOG_DIR", log_dir)
    
    logger = ToolkitLogger("test-logger")
    logger.info("Test info message")
    logger.debug("Test debug message")
    
    # Check if log file was created
    log_files = list(log_dir.glob("*.log"))
    assert len(log_files) == 1
    
    content = log_files[0].read_text()
    assert "test-logger - INFO - Test info message" in content
    assert "test-logger - DEBUG - Test debug message" in content

def test_log_execution(tmp_path, monkeypatch):
    # Mock HISTORY_FILE to use tmp_path
    history_file = tmp_path / "history.json"
    monkeypatch.setattr("git_toolkit.logging.HISTORY_FILE", history_file)
    
    log_execution("test-cmd", {"arg1": "val1"}, "SUCCESS")
    log_execution("test-cmd-2", {"arg2": "val2"}, "FAILED", "Some error")
    
    assert history_file.exists()
    
    with open(history_file, 'r') as f:
        history = json.load(f)
    
    assert len(history) == 2
    assert history[0]["command"] == "test-cmd"
    assert history[0]["status"] == "SUCCESS"
    assert history[1]["command"] == "test-cmd-2"
    assert history[1]["status"] == "FAILED"
    assert history[1]["details"] == "Some error"

def test_get_history(tmp_path, monkeypatch):
    history_file = tmp_path / "history.json"
    monkeypatch.setattr("git_toolkit.logging.HISTORY_FILE", history_file)
    
    for i in range(15):
        log_execution(f"cmd-{i}", {}, "SUCCESS")
    
    history = get_history(limit=5)
    assert len(history) == 5
    assert history[-1]["command"] == "cmd-14"
    assert history[0]["command"] == "cmd-10"

def test_history_limit(tmp_path, monkeypatch):
    history_file = tmp_path / "history.json"
    monkeypatch.setattr("git_toolkit.logging.HISTORY_FILE", history_file)
    
    # log_execution in logging.py has a hard limit of 100 entries
    for i in range(110):
        log_execution(f"cmd-{i}", {}, "SUCCESS")
        
    with open(history_file, 'r') as f:
        history = json.load(f)
    
    assert len(history) == 100
    assert history[0]["command"] == "cmd-10"
    assert history[-1]["command"] == "cmd-109"
