from __future__ import annotations

from unittest.mock import patch

import pytest

from git_toolkit.config import Config, Repository, Step
from git_toolkit.workflow_runner import _condition_matches, _execute_builtin


def _repo() -> Repository:
    return Repository(name="repo", path=".")


def test_condition_predicates_and_invalid_condition() -> None:
    repo = _repo()
    with patch("git_toolkit.workflow_runner.get_repo_status") as status:
        status.return_value = {
            "is_dirty": False,
            "exists": True,
            "detached": False,
            "branch": "main",
        }
        assert _condition_matches("repo.clean", repo)[0] is True
        assert _condition_matches("repo.dirty", repo)[0] is False
        assert _condition_matches("repo.exists", repo)[0] is True
        assert _condition_matches("repo.detached", repo)[0] is False
        assert _condition_matches("branch == main", repo)[0] is True
        assert _condition_matches(None, repo) == (True, "")
    with pytest.raises(ValueError, match="Unsupported workflow condition"):
        _condition_matches("unsupported", repo)


def test_builtin_status_paths() -> None:
    repo = _repo()
    config = Config(repositories=[repo])
    with patch("git_toolkit.workflow_runner.get_repo_status") as status:
        status.return_value = {"error": None, "branch": "main", "is_dirty": False}
        result = _execute_builtin(Step(command="status"), repo, config, False)
        assert result["success"] is True
        assert "main" in result["message"]

        status.return_value = {"error": "broken"}
        result = _execute_builtin(Step(command="status"), repo, config, False)
        assert result == {"success": False, "message": "broken"}


@pytest.mark.parametrize(
    ("command", "target"),
    [
        ("clone", "clone_repo"),
        ("fetch", "fetch_repo"),
        ("pull", "pull_repo"),
        ("push", "push_repo"),
        ("sync", "sync_repo"),
        ("submodule-update", "update_submodules"),
    ],
)
def test_builtin_simple_commands(command: str, target: str) -> None:
    repo = _repo()
    config = Config(repositories=[repo])
    with patch(f"git_toolkit.workflow_runner.{target}") as operation:
        operation.return_value = {"success": True, "message": "ok"}
        result = _execute_builtin(Step(command=command), repo, config, False)
        assert result["success"] is True
        operation.assert_called_once()


def test_builtin_commands_with_required_arguments() -> None:
    repo = _repo()
    config = Config(repositories=[repo])
    cases = [
        (Step(command="checkout", args={"branch": "dev"}), "checkout_repo"),
        (Step(command="commit", args={"message": "msg"}), "commit_repo"),
        (Step(command="merge", args={"source": "feature"}), "merge_repo"),
        (Step(command="rebase", args={"onto": "main"}), "rebase_repo"),
        (Step(command="tag", args={"tag": "v1"}), "tag_repo"),
    ]
    for step, target in cases:
        with patch(f"git_toolkit.workflow_runner.{target}") as operation:
            operation.return_value = {"success": True, "message": "ok"}
            result = _execute_builtin(step, repo, config, False)
            assert result["success"] is True
            operation.assert_called_once()


def test_builtin_missing_required_arguments_and_unknown_command() -> None:
    repo = _repo()
    config = Config(repositories=[repo])
    for command, text in [
        ("checkout", "checkout requires args.branch"),
        ("commit", "commit requires args.message"),
        ("merge", "merge requires args.source"),
        ("rebase", "rebase requires args.onto"),
        ("tag", "tag requires args.tag"),
    ]:
        result = _execute_builtin(Step(command=command), repo, config, False)
        assert result == {"success": False, "message": text}

    result = _execute_builtin(Step(command="mystery"), repo, config, False)
    assert result["success"] is False
    assert "Unknown command" in result["message"]
