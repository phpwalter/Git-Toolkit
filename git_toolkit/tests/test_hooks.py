from unittest.mock import MagicMock, patch

from git_toolkit.config import Hook
from git_toolkit.hooks import HookManager


def test_run_hook_no_script() -> None:
    manager = HookManager({"pre_status": Hook(script=None)})
    assert manager.run_hook("pre_status") is True


def test_run_hook_not_defined() -> None:
    manager = HookManager({})
    assert manager.run_hook("pre_status") is True


@patch("subprocess.run")
def test_project_hook_is_blocked_by_default(mock_run, capsys) -> None:
    manager = HookManager({"pre_status": Hook(script="echo hi")})
    assert manager.run_hook("pre_status") is False
    mock_run.assert_not_called()
    assert "project scripts are disabled" in capsys.readouterr().err


@patch("subprocess.run")
def test_trusted_hook_success(mock_run) -> None:
    mock_run.return_value = MagicMock(returncode=0)
    manager = HookManager(
        {"pre_status": Hook(script="echo hi")},
        allow_project_scripts=True,
    )
    assert manager.run_hook("pre_status") is True
    mock_run.assert_called_once()


@patch("subprocess.run")
def test_trusted_hook_failure(mock_run) -> None:
    mock_run.return_value = MagicMock(returncode=1)
    manager = HookManager(
        {"pre_status": Hook(script="exit 1")},
        allow_project_scripts=True,
    )
    assert manager.run_hook("pre_status") is False


@patch("subprocess.run")
def test_trusted_hook_environment(mock_run) -> None:
    mock_run.return_value = MagicMock(returncode=0)
    manager = HookManager(
        {"pre_status": Hook(script="echo $TEST_VAR")},
        allow_project_scripts=True,
    )
    assert manager.run_hook("pre_status", env={"TEST_VAR": "hi"}) is True
    assert mock_run.call_args.kwargs["env"]["TEST_VAR"] == "hi"
