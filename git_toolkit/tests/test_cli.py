from unittest.mock import patch

from git_toolkit.cli import main
from git_toolkit.config import Config, Repository, Security


def _config() -> Config:
    return Config(repositories=[Repository(name="repo1", path=".")])


@patch("git_toolkit.cli.PluginManager")
@patch("git_toolkit.cli.load_config")
@patch("git_toolkit.cli.get_repo_status")
@patch("sys.argv", ["git-toolkit", "status"])
def test_cli_status(mock_status, mock_load, mock_plugin_manager, capsys) -> None:
    mock_load.return_value = _config()
    mock_plugin_manager.return_value.plugins = []
    mock_plugin_manager.return_value.register_all_commands.return_value = None
    mock_status.return_value = {
        "exists": True,
        "branch": "main",
        "is_dirty": False,
        "ahead": 0,
        "behind": 0,
        "error": None,
    }

    main()

    output = capsys.readouterr().out
    assert "repo1" in output
    assert "main" in output
    assert "Clean" in output


@patch("git_toolkit.cli.PluginManager")
@patch("git_toolkit.cli.load_config")
@patch("git_toolkit.cli.clone_repo")
@patch("sys.argv", ["git-toolkit", "clone"])
def test_cli_clone(mock_clone, mock_load, mock_plugin_manager, capsys) -> None:
    mock_load.return_value = _config()
    mock_plugin_manager.return_value.plugins = []
    mock_plugin_manager.return_value.register_all_commands.return_value = None
    mock_clone.return_value = {"name": "repo1", "success": True, "message": "Cloned"}

    main()

    assert "Cloned" in capsys.readouterr().out


@patch("git_toolkit.cli.PluginManager")
@patch("git_toolkit.cli.load_config")
@patch("git_toolkit.cli.get_repo_stats")
@patch("sys.argv", ["git-toolkit", "stats", "--format", "json"])
def test_cli_stats_json(mock_stats, mock_load, mock_plugin_manager, capsys) -> None:
    mock_load.return_value = _config()
    mock_plugin_manager.return_value.plugins = []
    mock_plugin_manager.return_value.register_all_commands.return_value = None
    mock_stats.return_value = {
        "success": True,
        "name": "repo1",
        "active_branch": "main",
        "commit_count": 10,
        "contributor_count": 2,
        "stale_branches": [],
        "large_files": [],
    }

    main()

    output = capsys.readouterr().out
    assert '"name": "repo1"' in output
    assert '"commit_count": 10' in output


@patch("git_toolkit.cli.PluginManager")
@patch("git_toolkit.cli.load_config")
@patch("git_toolkit.cli.run_shell_command")
@patch("sys.argv", ["git-toolkit", "quality"])
def test_configured_command_is_executable(mock_shell, mock_load, mock_plugin_manager, capsys) -> None:
    config = Config(
        repositories=[Repository(name="repo1", path=".")],
        commands={"quality": {"description": "Quality gate", "script": "pytest"}},
        security=Security(allow_project_scripts=True),
    )
    mock_load.return_value = config
    mock_plugin_manager.return_value.plugins = []
    mock_plugin_manager.return_value.register_all_commands.return_value = None
    mock_shell.return_value = {"success": True, "message": "Command succeeded."}

    main()

    assert "Command succeeded" in capsys.readouterr().out
    mock_shell.assert_called_once()


@patch("git_toolkit.cli.PluginManager")
@patch("git_toolkit.cli.load_config")
@patch("sys.argv", ["git-toolkit", "config", "validate"])
def test_config_validate(mock_load, mock_plugin_manager, capsys) -> None:
    mock_load.return_value = _config()
    mock_plugin_manager.return_value.plugins = []
    mock_plugin_manager.return_value.register_all_commands.return_value = None

    main()

    assert "Configuration is valid" in capsys.readouterr().out
