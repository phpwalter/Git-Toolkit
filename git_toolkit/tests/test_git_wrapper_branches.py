from __future__ import annotations

from unittest.mock import MagicMock, patch

from git import InvalidGitRepositoryError

from git_toolkit.config import Config, Health, Repository, Safety
from git_toolkit.git_wrapper import (
    checkout_repo,
    clone_repo,
    commit_repo,
    fetch_repo,
    get_repo_stats,
    get_repo_status,
    merge_repo,
    pull_repo,
    push_repo,
    rebase_repo,
    sync_repo,
    tag_repo,
    update_submodules,
)


def _repo_config() -> Repository:
    return Repository(name="repo", path=".", url="https://github.com/example/repo.git")


def _mock_repo() -> MagicMock:
    repo = MagicMock()
    repo.head.is_detached = False
    repo.active_branch.name = "feature"
    repo.active_branch.tracking_branch.return_value = None
    repo.is_dirty.return_value = False
    repo.remotes.origin.url = "https://github.com/example/repo.git"
    repo.untracked_files = []
    repo.index.diff.return_value = []
    repo.index.unmerged_blobs.return_value = {}
    return repo


def test_status_invalid_repository_and_tracking_counts() -> None:
    config = _repo_config()
    with patch("git_toolkit.git_wrapper.get_cache", return_value=None), patch(
        "git_toolkit.git_wrapper._open_repo", side_effect=InvalidGitRepositoryError("bad")
    ):
        status = get_repo_status(config)
        assert status["exists"] is False
        assert status["error"] == "Invalid Git repository"

    repo = _mock_repo()
    tracking = MagicMock()
    tracking.name = "origin/feature"
    repo.active_branch.tracking_branch.return_value = tracking
    repo.head.commit.hexsha = "a" * 40
    repo.git.rev_list.return_value = "2 3"
    with patch("git_toolkit.git_wrapper._open_repo", return_value=repo), patch(
        "git_toolkit.git_wrapper.get_cache", return_value=None
    ), patch("git_toolkit.git_wrapper.set_cache"):
        status = get_repo_status(config)
        assert status["behind"] == 2
        assert status["ahead"] == 3
        assert status["upstream"] == "origin/feature"


def test_clone_missing_url_existing_repo_and_nonrepo_destination(tmp_path) -> None:
    config = Repository(name="repo", path=str(tmp_path / "repo"))
    assert clone_repo(config)["success"] is False

    config.url = "https://github.com/example/repo.git"
    path = tmp_path / "repo"
    path.mkdir()
    with patch("git_toolkit.git_wrapper._open_repo", return_value=MagicMock()):
        assert clone_repo(config)["success"] is True

    file = path / "existing.txt"
    file.write_text("x", encoding="utf-8")
    with patch("git_toolkit.git_wrapper._open_repo", side_effect=InvalidGitRepositoryError("bad")):
        result = clone_repo(config)
        assert result["success"] is False
        assert "not a Git repository" in result["message"]


def test_push_detached_remote_denied_and_remote_failure() -> None:
    config = _repo_config()
    repo = _mock_repo()
    repo.head.is_detached = True
    with patch("git_toolkit.git_wrapper._open_repo", return_value=repo):
        assert push_repo(config)["message"] == "Cannot push detached HEAD"

    repo = _mock_repo()
    policy_config = Config(safety=Safety(denied_remote_hosts=["github.com"]))
    with patch("git_toolkit.git_wrapper._open_repo", return_value=repo):
        result = push_repo(config, policy_config)
        assert result["policy_rule"] == "remote.host.denied"

    info = MagicMock()
    info.flags = 1
    info.ERROR = 1
    info.summary = "rejected"
    repo = _mock_repo()
    repo.remotes.origin.push.return_value = [info]
    with patch("git_toolkit.git_wrapper._open_repo", return_value=repo):
        result = push_repo(config, Config())
        assert result["success"] is False
        assert "rejected" in result["message"]


def test_fetch_pull_and_sync_error_paths() -> None:
    config = _repo_config()
    repo = _mock_repo()
    with patch("git_toolkit.git_wrapper._open_repo", return_value=repo):
        assert fetch_repo(config, dry_run=True)["success"] is True

    repo = _mock_repo()
    repo.head.is_detached = True
    with patch("git_toolkit.git_wrapper._open_repo", return_value=repo):
        assert pull_repo(config)["message"] == "Cannot pull detached HEAD"

    repo = _mock_repo()
    with patch("git_toolkit.git_wrapper._open_repo", return_value=repo):
        result = sync_repo(config, Config())
        assert result["success"] is False
        assert "no upstream" in result["message"]


def test_commit_merge_rebase_tag_and_submodule_dry_run_paths() -> None:
    config = _repo_config()
    repo = _mock_repo()
    with patch("git_toolkit.git_wrapper._open_repo", return_value=repo):
        assert commit_repo(config, "msg")["message"] == "Nothing to commit"
        assert merge_repo(config, "feature", dry_run=True)["success"] is True
        assert rebase_repo(config, "main", dry_run=True)["success"] is True
        assert tag_repo(config, "v1", dry_run=True)["success"] is True
        assert update_submodules(config, dry_run=True)["success"] is True


def test_checkout_policy_and_stats_health_paths() -> None:
    config = _repo_config()
    repo = _mock_repo()
    repo.is_dirty.return_value = True
    safety = Safety(require_clean_worktree=True)
    with patch("git_toolkit.git_wrapper._open_repo", return_value=repo):
        result = checkout_repo(config, "feature", safety)
        assert result["success"] is False
        assert result["policy_rule"] == "checkout.dirty.blocked"

    repo = _mock_repo()
    repo.head.is_detached = False
    repo.active_branch.name = "main"
    commit = MagicMock()
    commit.author.email = "a@example.invalid"
    repo.iter_commits.return_value = [commit]
    branch = MagicMock()
    branch.name = "old"
    branch.commit.committed_datetime = __import__("datetime").datetime.now(__import__("datetime").UTC)
    branch.commit.author.name = "A"
    repo.branches = [branch]
    repo.tree.return_value.traverse.return_value = []
    health = Health(stale_branch_days=30, large_file_kb=100)
    with patch("git_toolkit.git_wrapper._open_repo", return_value=repo), patch(
        "git_toolkit.git_wrapper.get_cache", return_value=None
    ), patch("git_toolkit.git_wrapper.set_cache"):
        stats = get_repo_stats(config, health)
        assert stats["success"] is True
        assert stats["commit_count"] == 1
        assert stats["contributor_count"] == 1
