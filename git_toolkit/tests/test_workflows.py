import pytest
import yaml
from pathlib import Path
from git_toolkit.cli import main
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_config(tmp_path):
    config_path = tmp_path / ".git-toolkit.yml"
    config_data = {
        "repositories": [
            {"name": "repo1", "path": str(tmp_path / "repo1")},
            {"name": "repo2", "path": str(tmp_path / "repo2")}
        ],
        "workflows": {
            "test_workflow": {
                "description": "A test workflow",
                "steps": [
                    {"name": "check status", "command": "status"},
                    {"name": "custom script", "script": "echo hello", "if": "branch == main"}
                ]
            }
        }
    }
    config_path.write_text(yaml.dump(config_data))
    return config_path

@patch("git_toolkit.cli.load_config")
@patch("git_toolkit.cli.get_repo_status")
@patch("git_toolkit.cli.run_shell_command")
def test_run_workflow(mock_run_shell, mock_status, mock_load, mock_config):
    from git_toolkit.config import Config
    with open(mock_config) as f:
        data = yaml.safe_load(f)
    mock_load.return_value = Config(**data)
    
    # Mock status for both repos
    mock_status.side_effect = [
        {"branch": "main", "is_dirty": False, "exists": True},
        {"branch": "develop", "is_dirty": True, "exists": True},
        {"branch": "main", "is_dirty": False, "exists": True}, # For the second step repo1
        {"branch": "develop", "is_dirty": True, "exists": True} # For the second step repo2
    ]
    
    mock_run_shell.return_value = {"success": True, "message": "Command succeeded."}
    
    with patch("sys.argv", ["git-toolkit", "--config", str(mock_config), "run", "test_workflow"]):
        with patch("sys.exit") as mock_exit:
            main()
            mock_exit.assert_not_called()

    # Verify that run_shell_command was called only once (for repo1 which is on 'main')
    assert mock_run_shell.call_count == 1
    # Verify that get_repo_status was called for each repo in each step (4 times total + 2 for status command = 6)
    # Actually: 
    # Step 1 (status command): calls get_repo_status for repo1 and repo2.
    # Step 2 (script with if): calls get_repo_status for repo1 and repo2.
    # Total 4 calls to get_repo_status.
    assert mock_status.call_count == 4

@patch("git_toolkit.cli.load_config")
@patch("git_toolkit.cli.execute_step")
def test_run_workflow_parallel(mock_execute, mock_load, mock_config):
    from git_toolkit.config import Config
    with open(mock_config) as f:
        data = yaml.safe_load(f)
    mock_load.return_value = Config(**data)
    
    mock_execute.return_value = "Success"
    
    with patch("sys.argv", ["git-toolkit", "--config", str(mock_config), "run", "test_workflow", "--parallel"]):
        with patch("sys.exit") as mock_exit:
            main()
            mock_exit.assert_not_called()

    # 2 steps * 2 repos = 4 executions
    assert mock_execute.call_count == 4
