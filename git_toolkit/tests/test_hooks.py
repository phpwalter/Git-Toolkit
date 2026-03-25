import pytest
import subprocess
from unittest.mock import MagicMock, patch
from git_toolkit.hooks import HookManager
from git_toolkit.config import Hook

def test_run_hook_no_script():
    mgr = HookManager({"pre_status": Hook(script=None)})
    assert mgr.run_hook("pre_status") is True

def test_run_hook_not_defined():
    mgr = HookManager({})
    assert mgr.run_hook("pre_status") is True

@patch("subprocess.run")
def test_run_hook_success(mock_run):
    mock_run.return_value = MagicMock(returncode=0)
    mgr = HookManager({"pre_status": Hook(script="echo 'hi'")})
    assert mgr.run_hook("pre_status") is True
    mock_run.assert_called_once()
    assert mock_run.call_args[0][0] == "echo 'hi'"

@patch("subprocess.run")
def test_run_hook_failure(mock_run):
    mock_run.return_value = MagicMock(returncode=1)
    mgr = HookManager({"pre_status": Hook(script="exit 1")})
    assert mgr.run_hook("pre_status") is False

@patch("subprocess.run")
def test_run_hook_exception(mock_run):
    mock_run.side_effect = Exception("error")
    mgr = HookManager({"pre_status": Hook(script="exit 1")})
    assert mgr.run_hook("pre_status") is False

@patch("subprocess.run")
def test_run_hook_env(mock_run):
    mock_run.return_value = MagicMock(returncode=0)
    mgr = HookManager({"pre_status": Hook(script="echo $TEST_VAR")})
    assert mgr.run_hook("pre_status", env={"TEST_VAR": "hi"}) is True
    env_called = mock_run.call_args[1]["env"]
    assert env_called["TEST_VAR"] == "hi"
