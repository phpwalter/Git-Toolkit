import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from git_toolkit.git_wrapper import get_repo_status, clone_repo, checkout_repo, push_repo, update_submodules, get_repo_stats
from git_toolkit.config import Repository, Safety, Health
from datetime import datetime, timedelta, timezone

@pytest.fixture
def mock_health_config():
    return Health(stale_branch_days=30, large_file_kb=100)

@pytest.fixture
def mock_repo_config():
    return Repository(name="test_repo", path="./test_repo", url="https://github.com/user/test_repo.git")

@pytest.fixture
def mock_safety_config():
    return Safety(prevent_force_push=True, protect_branches=["main", "release"])

@patch("git_toolkit.git_wrapper.Repo")
@patch("git_toolkit.git_wrapper.Path.exists")
def test_get_repo_status_exists(mock_exists, mock_repo_class, mock_repo_config):
    # Mock Path.exists to return True for both repo_path and repo_path / ".git"
    mock_exists.return_value = True
    
    mock_repo = MagicMock()
    mock_repo.active_branch.name = "main"
    mock_repo.is_dirty.return_value = False
    mock_repo_class.return_value = mock_repo
    
    status = get_repo_status(mock_repo_config)
    assert status["exists"] is True
    assert status["branch"] == "main"
    assert status["is_dirty"] is False

@patch("git_toolkit.git_wrapper.Path.exists")
def test_get_repo_status_not_exists(mock_exists, mock_repo_config):
    mock_exists.return_value = False
    status = get_repo_status(mock_repo_config)
    assert status["exists"] is False

@patch("git_toolkit.git_wrapper.Repo.clone_from")
@patch("git_toolkit.git_wrapper.Path.exists")
def test_clone_repo_success(mock_exists, mock_clone_from, mock_repo_config):
    # Path doesn't exist yet
    mock_exists.return_value = False
    
    result = clone_repo(mock_repo_config)
    assert result["success"] is True
    assert result["message"] == "Successfully cloned"
    mock_clone_from.assert_called_once()

@patch("git_toolkit.git_wrapper.Repo")
@patch("git_toolkit.git_wrapper.Path.exists")
def test_checkout_repo_success(mock_exists, mock_repo_class, mock_repo_config):
    mock_exists.return_value = True
    mock_repo = MagicMock()
    mock_repo_class.return_value = mock_repo
    
    result = checkout_repo(mock_repo_config, "develop")
    assert result["success"] is True
    assert result["message"] == "Switched to develop"
    mock_repo.git.checkout.assert_called_with("develop")

@patch("git_toolkit.git_wrapper.Repo")
@patch("git_toolkit.git_wrapper.Path.exists")
def test_push_repo_success(mock_exists, mock_repo_class, mock_repo_config):
    mock_exists.return_value = True
    mock_repo = MagicMock()
    mock_repo_class.return_value = mock_repo
    
    # Mock push to return success
    mock_push_info = MagicMock()
    mock_push_info.flags = 0 # No ERROR flag
    # Mocking the info[0].ERROR flag check
    mock_push_info.ERROR = 1 
    mock_repo.remotes.origin.push.return_value = [mock_push_info]
    
    result = push_repo(mock_repo_config)
    assert result["success"] is True
    assert result["message"] == "Successfully pushed"

@patch("git_toolkit.git_wrapper.Repo")
@patch("git_toolkit.git_wrapper.Path.exists")
def test_push_repo_protected(mock_exists, mock_repo_class, mock_repo_config, mock_safety_config):
    mock_exists.return_value = True
    mock_repo = MagicMock()
    mock_repo.active_branch.name = "main"
    mock_repo_class.return_value = mock_repo
    
    result = push_repo(mock_repo_config, safety=mock_safety_config)
    assert result["success"] is False
    assert "protected branch 'main' is blocked" in result["message"]
    mock_repo.remotes.origin.push.assert_not_called()

@patch("git_toolkit.git_wrapper.Repo")
@patch("git_toolkit.git_wrapper.Path.exists")
def test_push_repo_dry_run(mock_exists, mock_repo_class, mock_repo_config):
    mock_exists.return_value = True
    mock_repo = MagicMock()
    mock_repo.active_branch.name = "feature"
    mock_repo_class.return_value = mock_repo
    
    result = push_repo(mock_repo_config, dry_run=True)
    assert result["success"] is True
    assert "[DRY-RUN]" in result["message"]
    mock_repo.remotes.origin.push.assert_not_called()

@patch("git_toolkit.git_wrapper.Repo")
@patch("git_toolkit.git_wrapper.Path.exists")
def test_update_submodules_success(mock_exists, mock_repo_class, mock_repo_config):
    mock_exists.return_value = True
    mock_repo = MagicMock()
    mock_repo_class.return_value = mock_repo
    
    result = update_submodules(mock_repo_config)
    assert result["success"] is True
    assert result["message"] == "Submodules updated"
    mock_repo.git.submodule.assert_called_with('update', '--init', '--recursive')

@patch("git_toolkit.git_wrapper.Repo")
@patch("git_toolkit.git_wrapper.Path.exists")
def test_get_repo_stats_success(mock_exists, mock_repo_class, mock_repo_config):
    mock_exists.return_value = True
    mock_repo = MagicMock()
    mock_repo.active_branch.name = "main"
    
    # Mock commits
    commit1 = MagicMock()
    commit1.author.email = "user1@example.com"
    commit2 = MagicMock()
    commit2.author.email = "user2@example.com"
    commit3 = MagicMock()
    commit3.author.email = "user1@example.com"
    
    mock_repo.iter_commits.return_value = [commit1, commit2, commit3]
    mock_repo_class.return_value = mock_repo
    
    stats = get_repo_stats(mock_repo_config)
    assert stats["success"] is True
    assert stats["commit_count"] == 3
    assert stats["contributor_count"] == 2
    assert stats["active_branch"] == "main"

@patch("git_toolkit.git_wrapper.Repo")
@patch("git_toolkit.git_wrapper.Path.exists")
def test_get_repo_stats_with_health(mock_exists, mock_repo_class, mock_repo_config, mock_health_config):
    mock_exists.return_value = True
    mock_repo = MagicMock()
    mock_repo.active_branch.name = "main"
    
    # Mock branches for stale check
    now = datetime.now(timezone.utc)
    
    branch_main = MagicMock()
    branch_main.name = "main"
    branch_main.commit.committed_datetime = now - timedelta(days=10)
    branch_main.commit.author.name = "Author1"
    
    branch_stale = MagicMock()
    branch_stale.name = "stale-feature"
    branch_stale.commit.committed_datetime = now - timedelta(days=40)
    branch_stale.commit.author.name = "Author2"
    
    mock_repo.branches = [branch_main, branch_stale]
    
    # Mock tree for large file check
    file_small = MagicMock()
    file_small.type = 'blob'
    file_small.path = "small.txt"
    file_small.size = 50 * 1024 # 50 KB
    
    file_large = MagicMock()
    file_large.type = 'blob'
    file_large.path = "large.bin"
    file_large.size = 200 * 1024 # 200 KB
    
    mock_repo.tree().traverse.return_value = [file_small, file_large]
    
    # Other stats
    mock_repo.iter_commits.return_value = []
    mock_repo_class.return_value = mock_repo
    
    stats = get_repo_stats(mock_repo_config, health=mock_health_config)
    
    assert stats["success"] is True
    assert len(stats["stale_branches"]) == 1
    assert stats["stale_branches"][0]["name"] == "stale-feature"
    assert stats["stale_branches"][0]["days_old"] >= 40
    
    assert len(stats["large_files"]) == 1
    assert stats["large_files"][0]["path"] == "large.bin"
    assert stats["large_files"][0]["size_kb"] == 200.0
