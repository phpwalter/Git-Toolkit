from unittest.mock import MagicMock, patch

from git_toolkit.branching import create_branch, delete_branch, list_branches
from git_toolkit.config import Repository, Safety


def _config() -> Repository:
    return Repository(name="repo", path=".")


def test_list_branches_reports_active_branch() -> None:
    repo = MagicMock()
    repo.head.is_detached = False
    repo.active_branch.name = "main"
    repo.branches = [MagicMock(name="ignored"), MagicMock(name="ignored")]
    repo.branches[0].name = "main"
    repo.branches[1].name = "feature/test"
    with patch("git_toolkit.branching.Repo", return_value=repo):
        result = list_branches(_config())
    assert result["active"] == "main"
    assert result["branches"] == ["main", "feature/test"]


def test_create_branch_respects_name_policy() -> None:
    safety = Safety(branch_name_pattern=r"feature/.+")
    result = create_branch(_config(), "main", safety=safety)
    assert result["success"] is False
    assert result["policy_rule"] == "branch.name.invalid"


def test_create_branch_can_checkout_new_branch() -> None:
    repo = MagicMock()
    repo.branches = []
    created = MagicMock()
    repo.create_head.return_value = created
    with patch("git_toolkit.branching.Repo", return_value=repo):
        result = create_branch(_config(), "feature/test", checkout=True)
    assert result["success"] is True
    created.checkout.assert_called_once()


def test_delete_branch_blocks_protected_and_active() -> None:
    protected = delete_branch(_config(), "main", safety=Safety())
    assert protected["success"] is False

    repo = MagicMock()
    repo.head.is_detached = False
    repo.active_branch.name = "feature/test"
    with patch("git_toolkit.branching.Repo", return_value=repo):
        active = delete_branch(_config(), "feature/test")
    assert active["success"] is False
    repo.delete_head.assert_not_called()
