from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from git_toolkit.execution import CommandSpec, parse_argv, run_command


def test_command_spec_requires_exactly_one_mode() -> None:
    with pytest.raises(ValueError):
        CommandSpec()
    with pytest.raises(ValueError):
        CommandSpec(argv=["echo"], shell_command="echo")


def test_parse_argv_and_dry_run(tmp_path) -> None:
    assert parse_argv('git status --short') == ["git", "status", "--short"]
    result = run_command(tmp_path, CommandSpec(argv=["git", "status"]), dry_run=True)
    assert result["success"] is True
    assert "git status" in result["message"]


def test_shell_execution_is_blocked_by_default(tmp_path) -> None:
    result = run_command(tmp_path, CommandSpec(shell_command="echo ok"))
    assert result["success"] is False
    assert "Shell execution is disabled" in result["message"]


def test_argv_execution_uses_shell_false(tmp_path) -> None:
    completed = MagicMock(returncode=0, stdout="ok", stderr="")
    with patch("git_toolkit.execution.subprocess.run", return_value=completed) as run:
        result = run_command(tmp_path, CommandSpec(argv=["git", "status"]))
    assert result["success"] is True
    assert run.call_args.kwargs["shell"] is False


def test_timeout_is_reported(tmp_path) -> None:
    with patch("git_toolkit.execution.subprocess.run", side_effect=__import__("subprocess").TimeoutExpired("git", 2)):
        result = run_command(tmp_path, CommandSpec(argv=["git"], timeout=2))
    assert result["success"] is False
    assert "timed out" in result["message"]
