from __future__ import annotations

from unittest.mock import MagicMock, patch

from git_toolkit.config import Repository
from git_toolkit.git_wrapper import get_repo_stats, get_repo_status
from git_toolkit.logging import clear_cache, get_cache, set_cache


def test_cache_set_get(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("git_toolkit.logging.CACHE_DIR", tmp_path / "cache")
    set_cache("test_key", {"data": "value"}, ttl=10)
    assert get_cache("test_key") == {"data": "value"}


def test_cache_expiration(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("git_toolkit.logging.CACHE_DIR", tmp_path / "cache")
    set_cache("expired_key", {"data": "old"}, ttl=-1)
    assert get_cache("expired_key") is None


def test_clear_cache(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("git_toolkit.logging.CACHE_DIR", tmp_path / "cache")
    set_cache("key1", "val1")
    set_cache("key2", "val2")
    clear_cache()
    assert get_cache("key1") is None
    assert get_cache("key2") is None


@patch("git_toolkit.git_wrapper.Repo")
def test_get_repo_status_caching(mock_repo_class, tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("git_toolkit.logging.CACHE_DIR", tmp_path / "cache")
    repo = MagicMock()
    repo.head.is_detached = False
    repo.head.commit.hexsha = "a" * 40
    repo.active_branch.name = "main"
    repo.active_branch.tracking_branch.return_value = None
    repo.is_dirty.return_value = False
    repo.untracked_files = []
    repo.index.diff.return_value = []
    repo.index.unmerged_blobs.return_value = {}
    mock_repo_class.return_value = repo
    config = Repository(name="test-repo", path="fake/path")

    assert get_repo_status(config)["branch"] == "main"
    mock_repo_class.assert_called_once()

    mock_repo_class.reset_mock()
    assert get_repo_status(config)["branch"] == "main"
    mock_repo_class.assert_not_called()


@patch("git_toolkit.git_wrapper.Repo")
def test_get_repo_stats_caching(mock_repo_class, tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("git_toolkit.logging.CACHE_DIR", tmp_path / "cache")
    repo = MagicMock()
    repo.head.is_detached = False
    repo.active_branch.name = "main"
    first = MagicMock()
    first.author.email = "a@example.invalid"
    second = MagicMock()
    second.author.email = "b@example.invalid"
    repo.iter_commits.return_value = [first, second]
    mock_repo_class.return_value = repo
    config = Repository(name="test-stats-repo", path="fake/path")

    assert get_repo_stats(config)["commit_count"] == 2
    mock_repo_class.assert_called_once()

    mock_repo_class.reset_mock()
    assert get_repo_stats(config)["commit_count"] == 2
    mock_repo_class.assert_not_called()
