from __future__ import annotations

from argparse import Namespace
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from git_toolkit.cli import _dispatch
from git_toolkit.config import Config, Repository, Step, Workflow


def _config() -> Config:
    return Config(repositories=[Repository(name="repo", path=".")])


def _manager() -> MagicMock:
    manager = MagicMock()
    manager.handle_command.return_value = False
    manager.diagnostics.return_value = {"plugins": ["demo"], "errors": [], "api_version": "1"}
    return manager


def _args(command: str, **overrides) -> Namespace:
    values = {
        "command": command,
        "group": None,
        "dry_run": False,
        "force_with_lease": False,
        "branch": "main",
        "message": "msg",
        "source": "feature",
        "onto": "main",
        "tag": "v1",
        "format": "table",
        "workflow": "wf",
        "parallel": False,
        "workers": 2,
        "config_command": None,
        "plugin_command": None,
        "limit": 5,
    }
    values.update(overrides)
    return Namespace(**values)


@pytest.mark.parametrize(
    ("command", "patched", "kwargs"),
    [
        ("fetch", "fetch_repo", {}),
        ("pull", "pull_repo", {}),
        ("sync", "sync_repo", {}),
        ("checkout", "checkout_repo", {"branch": "dev"}),
        ("commit", "commit_repo", {"message": "change"}),
        ("merge", "merge_repo", {"source": "feature"}),
        ("rebase", "rebase_repo", {"onto": "main"}),
        ("tag", "tag_repo", {"tag": "v1"}),
        ("submodule", "update_submodules", {}),
    ],
)
def test_core_repository_commands(command: str, patched: str, kwargs: dict[str, str], capsys) -> None:
    config = _config()
    manager = _manager()
    with patch(f"git_toolkit.cli.{patched}") as operation:
        operation.return_value = {"name": "repo", "success": True, "message": "ok"}
        assert _dispatch(_args(command, **kwargs), config, manager, Path("project.yml")) == 0
        operation.assert_called_once()
    assert "ok" in capsys.readouterr().out


def test_fetch_and_pull_receive_configured_safety_policy() -> None:
    config = _config()
    config.safety.allowed_remote_hosts = ["github.com"]
    manager = _manager()
    repo = config.repositories[0]

    with patch("git_toolkit.cli.fetch_repo") as fetch:
        fetch.return_value = {"name": "repo", "success": True, "message": "ok"}
        assert _dispatch(_args("fetch", dry_run=True), config, manager, Path("project.yml")) == 0
        fetch.assert_called_once_with(repo, True, config.safety)

    with patch("git_toolkit.cli.pull_repo") as pull:
        pull.return_value = {"name": "repo", "success": True, "message": "ok"}
        assert _dispatch(_args("pull", dry_run=True), config, manager, Path("project.yml")) == 0
        pull.assert_called_once_with(repo, True, config.safety)


def test_workflow_dispatch_paths(capsys) -> None:
    manager = _manager()
    config = _config()
    assert _dispatch(_args("run", workflow="missing"), config, manager, Path("project.yml")) == 2
    assert "not found" in capsys.readouterr().err

    workflow = Workflow(steps=[Step(command="status")], webhook_url="https://example.invalid/hook")
    config.workflows = {"wf": workflow}
    with patch("git_toolkit.cli.run_workflow", return_value=["repo: FAILED - bad"]), patch(
        "git_toolkit.cli.send_webhook_notification"
    ) as notify:
        assert _dispatch(_args("run"), config, manager, Path("project.yml")) == 1
        notify.assert_called_once()

    with patch("git_toolkit.cli.run_workflow", return_value=["repo: OK - clean"]), patch(
        "git_toolkit.cli.send_webhook_notification"
    ) as notify:
        assert _dispatch(_args("run", dry_run=True), config, manager, Path("project.yml")) == 0
        notify.assert_not_called()


def test_config_and_plugin_dispatch(capsys) -> None:
    config = _config()
    manager = _manager()

    assert _dispatch(_args("config", config_command="show", format="json"), config, manager, Path("project.yml")) == 0
    assert _dispatch(_args("config", config_command="show", format="yaml"), config, manager, Path("project.yml")) == 0

    with patch("git_toolkit.cli.explain_config_value", return_value=(True, "defaults")):
        assert _dispatch(
            _args("config", config_command="explain", key="safety.prevent_force_push"),
            config,
            manager,
            Path("project.yml"),
        ) == 0

    with patch("git_toolkit.cli.initialize_project_config") as initialize:
        assert _dispatch(
            _args("config", config_command="init", force=True), config, manager, Path("project.yml")
        ) == 0
        initialize.assert_called_once()

    assert _dispatch(_args("plugins", plugin_command="list"), config, manager, Path("project.yml")) == 0
    manager.diagnostics.return_value = {"plugins": [], "errors": ["problem"], "api_version": "1"}
    assert _dispatch(_args("plugins", plugin_command="doctor"), config, manager, Path("project.yml")) == 1

    output = capsys.readouterr().out
    assert "source: defaults" in output


def test_history_cache_and_plugin_fallback(capsys) -> None:
    config = Config()
    manager = _manager()

    with patch("git_toolkit.cli.get_history", return_value=[{"command": "status"}]):
        assert _dispatch(_args("history", limit=3), config, manager, Path("project.yml")) == 0

    with patch("git_toolkit.cli.clear_cache") as clear_cache:
        assert _dispatch(_args("clear-cache"), config, manager, Path("project.yml")) == 0
        clear_cache.assert_called_once()

    manager.handle_command.return_value = True
    assert _dispatch(_args("plugin-command"), config, manager, Path("project.yml")) == 0
    manager.handle_command.return_value = False
    assert _dispatch(_args("unknown"), config, manager, Path("project.yml")) == 2

    assert "Cache cleared" in capsys.readouterr().out
