import pytest
import sys
from unittest.mock import patch, MagicMock
from git_toolkit.cli import main
from git_toolkit.config import Repository

@patch("git_toolkit.cli.load_config")
@patch("argparse.ArgumentParser.parse_args")
def test_cli_version(mock_args, mock_load):
    # This is a bit tricky since --version exits, 
    # but we can test if it routes to other commands properly.
    pass

@patch("git_toolkit.cli.load_config")
@patch("git_toolkit.cli.get_repo_status")
@patch("git_toolkit.cli.HookManager.run_hook")
@patch("sys.argv", ["git-toolkit", "status"])
def test_cli_status(mock_run_hook, mock_status, mock_load):
    mock_config = MagicMock()
    mock_repo = Repository(name="repo1", path=".")
    mock_config.repositories = [mock_repo]
    mock_config.hooks = {}
    mock_load.return_value = mock_config
    mock_run_hook.return_value = True
    mock_status.return_value = {"exists": True, "is_dirty": False, "branch": "main", "error": None}
    
    with patch("sys.stdout") as mock_stdout:
        main()
        # Verify it printed something related to status
        output = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
        assert "repo1" in output
        assert "main" in output
        assert "Clean" in output

@patch("git_toolkit.cli.load_config")
@patch("git_toolkit.cli.clone_repo")
@patch("git_toolkit.cli.HookManager.run_hook")
@patch("sys.argv", ["git-toolkit", "clone"])
def test_cli_clone(mock_run_hook, mock_clone, mock_load):
    mock_config = MagicMock()
    mock_repo = Repository(name="repo1", path=".")
    mock_config.repositories = [mock_repo]
    mock_config.hooks = {}
    mock_load.return_value = mock_config
    mock_run_hook.return_value = True
    mock_clone.return_value = {"message": "Cloned"}
    
    with patch("sys.stdout") as mock_stdout:
        main()
        output = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
        assert "repo1" in output
        assert "Cloned" in output

@patch("git_toolkit.cli.load_config")
@patch("git_toolkit.cli.get_repo_stats")
@patch("sys.argv", ["git-toolkit", "stats"])
def test_cli_stats_table(mock_stats, mock_load):
    mock_config = MagicMock()
    mock_repo = Repository(name="repo1", path=".")
    mock_config.repositories = [mock_repo]
    mock_config.hooks = {}
    mock_load.return_value = mock_config
    
    mock_stats.return_value = {
        "success": True,
        "name": "repo1",
        "active_branch": "main",
        "commit_count": 10,
        "contributor_count": 2,
        "stale_branches": [],
        "large_files": []
    }
    
    with patch("sys.stdout") as mock_stdout:
        main()
        output = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
        assert "repo1" in output
        assert "main" in output
        assert "10" in output
        assert "2" in output

@patch("git_toolkit.cli.load_config")
@patch("git_toolkit.cli.get_repo_stats")
@patch("git_toolkit.cli.PluginManager")
@patch("sys.argv", ["git-toolkit", "stats", "--format", "json"])
def test_cli_stats_json(mock_plugin_class, mock_stats, mock_load):
    # Mock PluginManager to avoid noise in stdout
    mock_plugin_mgr = mock_plugin_class.return_value
    mock_plugin_mgr.plugins = []
    
    mock_config = MagicMock()
    mock_repo = Repository(name="repo1", path=".")
    mock_config.repositories = [mock_repo]
    mock_config.hooks = {}
    mock_load.return_value = mock_config
    
    mock_stats.return_value = {
        "success": True,
        "name": "repo1",
        "active_branch": "main",
        "commit_count": 10,
        "contributor_count": 2,
        "stale_branches": [],
        "large_files": []
    }
    
    with patch("sys.stdout") as mock_stdout:
        main()
        output = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
        import json
        # Filter out potential warnings from PluginManager if they still occur
        json_start = output.find("[")
        if json_start != -1:
            output = output[json_start:]
        data = json.loads(output)
        assert data[0]["name"] == "repo1"
        assert data[0]["commit_count"] == 10

@patch("git_toolkit.cli.load_config")
@patch("git_toolkit.cli.get_repo_stats")
@patch("sys.argv", ["git-toolkit", "stats", "--format", "markdown"])
def test_cli_stats_markdown(mock_stats, mock_load):
    mock_config = MagicMock()
    mock_repo = Repository(name="repo1", path=".")
    mock_config.repositories = [mock_repo]
    mock_config.hooks = {}
    mock_load.return_value = mock_config
    
    mock_stats.return_value = {
        "success": True,
        "name": "repo1",
        "active_branch": "main",
        "commit_count": 10,
        "contributor_count": 2,
        "stale_branches": [{"name": "stale-feat", "days_old": 40, "last_author": "User"}],
        "large_files": [{"path": "big.bin", "size_kb": 200}]
    }
    
    with patch("sys.stdout") as mock_stdout:
        main()
        output = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
        assert "# Repository Analytics Report" in output
        assert "## repo1" in output
        assert "stale-feat" in output
        assert "big.bin" in output
