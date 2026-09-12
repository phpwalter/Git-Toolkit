from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from git_toolkit.config import Config, Repository, Safety
from git_toolkit.git_wrapper import (
    checkout_repo,
    clone_repo,
    commit_repo,
    fetch_repo,
    get_repo_status,
    merge_repo,
    pull_repo,
    push_repo,
    rebase_repo,
    sync_repo,
    tag_repo,
    update_submodules,
)


@pytest.fixture
def repo_config() -> Repository:
    return Repository(name="repo", path="/tmp/repo", url="https://github.com/example/repo.git")


@pytest.fixture
def safety_config() -> Safety:
    return Safety(prevent_force_push=True, protect_branches=["main"], require_clean_worktree=True)


def _mock_repo(branch: str = "feature") -> MagicMock:
    repo = MagicMock()
    repo.head.is_detached = False
    repo.active_branch.name = branch
    repo.is_dirty.return_value = False
    repo.untracked_files = []
    repo.index.diff.return_value = []
    repo.index.unmerged_blobs.return_value = {}
    repo.active_branch.tracking_branch.return_value = None
    repo.remotes.origin.url = "https://github.com/example/repo.git"
    return repo


@patch("git_toolkit.git_wrapper.Repo")
def test_get_repo_status_reports_rich_state(mock_repo_class: MagicMock, repo_config: Repository) -> None:
    repo = _mock_repo("main")
    repo.head.commit.hexsha = "a" * 40
    mock_repo_class.return_value = repo

    status = get_repo_status(repo_config)

    assert status["exists"] is True
    assert status["branch"] == "main"
    assert status["head_sha"] == "a" * 40
    assert status["ahead"] == 0
    assert status["behind"] == 0


@patch("git_toolkit.git_wrapper.Repo.clone_from")
def test_clone_repo_success(mock_clone: MagicMock, repo_config: Repository, tmp_path) -> None:
    repo_config.path = str(tmp_path / "clone")
    result = clone_repo(repo_config)
    assert result["success"] is True
    mock_clone.assert_called_once()


@patch("git_toolkit.git_wrapper.Repo.clone_from")
def test_clone_repo_respects_remote_allowlist(
    mock_clone: MagicMock,
    repo_config: Repository,
    tmp_path,
) -> None:
    repo_config.path = str(tmp_path / "clone")
    config = Config(safety=Safety(allowed_remote_hosts=["gitlab.com"]))

    result = clone_repo(repo_config, config)

    assert result["success"] is False
    assert result["policy_rule"] == "remote.host.not_allowed"
    mock_clone.assert_not_called()


@patch("git_toolkit.git_wrapper._open_repo")
def test_fetch_repo(mock_open: MagicMock, repo_config: Repository) -> None:
    repo = _mock_repo()
    mock_open.return_value = repo
    result = fetch_repo(repo_config)
    assert result["success"] is True
    repo.remotes.origin.fetch.assert_called_once_with(prune=True)


@patch("git_toolkit.git_wrapper._open_repo")
def test_fetch_repo_respects_remote_policy(mock_open: MagicMock, repo_config: Repository) -> None:
    repo = _mock_repo()
    mock_open.return_value = repo
    safety = Safety(denied_remote_hosts=["github.com"])

    result = fetch_repo(repo_config, safety=safety)

    assert result["success"] is False
    assert result["policy_rule"] == "remote.host.denied"
    repo.remotes.origin.fetch.assert_not_called()


@patch("git_toolkit.git_wrapper._open_repo")
def test_pull_is_fast_forward_only(mock_open: MagicMock, repo_config: Repository) -> None:
    repo = _mock_repo()
    mock_open.return_value = repo
    result = pull_repo(repo_config)
    assert result["success"] is True
    repo.git.pull.assert_called_once_with("--ff-only")


@patch("git_toolkit.git_wrapper._open_repo")
def test_commit_stages_all(mock_open: MagicMock, repo_config: Repository) -> None:
    repo = _mock_repo()
    repo.is_dirty.return_value = True
    repo.index.commit.return_value.hexsha = "1234567890abcdef"
    mock_open.return_value = repo
    result = commit_repo(repo_config, "test commit")
    assert result["success"] is True
    repo.git.add.assert_called_once_with("-A")
    repo.index.commit.assert_called_once_with("test commit")


@patch("git_toolkit.git_wrapper._open_repo")
def test_force_push_blocked_by_policy(
    mock_open: MagicMock, repo_config: Repository, safety_config: Safety
) -> None:
    repo = _mock_repo("feature")
    mock_open.return_value = repo
    config = Config(repositories=[repo_config], safety=safety_config)
    result = push_repo(repo_config, config=config, force=True)
    assert result["success"] is False
    assert result["policy_rule"] == "push.force.disabled"
    assert "Force push is disabled" in result["message"]
    repo.remotes.origin.push.assert_not_called()


@patch("git_toolkit.git_wrapper._open_repo")
def test_push_blocks_invalid_branch_name(mock_open: MagicMock, repo_config: Repository) -> None:
    repo = _mock_repo("BadBranch")
    mock_open.return_value = repo
    config = Config(safety=Safety(branch_name_pattern=r"feature/[a-z0-9-]+"))

    result = push_repo(repo_config, config=config)

    assert result["success"] is False
    assert result["policy_rule"] == "branch.name.invalid"
    repo.remotes.origin.push.assert_not_called()


@patch("git_toolkit.git_wrapper._open_repo")
def test_force_push_uses_force_with_lease_when_allowed(
    mock_open: MagicMock, repo_config: Repository
) -> None:
    repo = _mock_repo("feature")
    info = MagicMock()
    info.flags = 0
    info.ERROR = 1
    repo.remotes.origin.push.return_value = [info]
    mock_open.return_value = repo
    config = Config(safety=Safety(prevent_force_push=False, protect_branches=["main"]))
    result = push_repo(repo_config, config=config, force=True)
    assert result["success"] is True
    repo.remotes.origin.push.assert_called_once_with("--force-with-lease")


@patch("git_toolkit.git_wrapper._open_repo")
def test_sync_requires_clean_tree(mock_open: MagicMock, repo_config: Repository) -> None:
    repo = _mock_repo()
    repo.is_dirty.return_value = True
    mock_open.return_value = repo
    result = sync_repo(repo_config, Config(safety=Safety(require_clean_worktree=True)))
    assert result["success"] is False
    assert result["policy_rule"] == "sync.dirty.blocked"
    assert "requires a clean working tree" in result["message"]


@patch("git_toolkit.git_wrapper._open_repo")
def test_checkout_requires_clean_tree(mock_open: MagicMock, repo_config: Repository) -> None:
    repo = _mock_repo()
    repo.is_dirty.return_value = True
    mock_open.return_value = repo
    result = checkout_repo(repo_config, "main", Safety(require_clean_worktree=True))
    assert result["success"] is False
    assert result["policy_rule"] == "checkout.dirty.blocked"


@patch("git_toolkit.git_wrapper._open_repo")
def test_checkout_enforces_branch_naming_policy(mock_open: MagicMock, repo_config: Repository) -> None:
    repo = _mock_repo()
    mock_open.return_value = repo
    safety = Safety(branch_name_pattern=r"(main|feature/[a-z0-9-]+)")

    result = checkout_repo(repo_config, "invalid name", safety)

    assert result["success"] is False
    assert result["policy_rule"] == "branch.name.invalid"
    repo.git.checkout.assert_not_called()


@patch("git_toolkit.git_wrapper._open_repo")
def test_merge_rebase_tag_and_submodules(mock_open: MagicMock, repo_config: Repository) -> None:
    repo = _mock_repo()
    mock_open.return_value = repo

    assert merge_repo(repo_config, "feature")["success"] is True
    repo.git.merge.assert_called_with("--no-ff", "feature")

    assert rebase_repo(repo_config, "main")["success"] is True
    repo.git.rebase.assert_called_with("main")

    assert tag_repo(repo_config, "v1.0.0")["success"] is True
    repo.create_tag.assert_called_with("v1.0.0")

    assert update_submodules(repo_config)["success"] is True
    repo.git.submodule.assert_called_with("update", "--init", "--recursive")
