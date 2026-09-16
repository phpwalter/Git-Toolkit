from __future__ import annotations

from unittest.mock import patch

import pytest

from git_toolkit.cli import _stats, _status, _targets
from git_toolkit.config import Config, Repository


def test_targets_group_filtering() -> None:
    config = Config(
        repositories=[
            Repository(name="a", path=".", groups=["core"]),
            Repository(name="b", path=".", groups=["other"]),
        ]
    )
    assert [repo.name for repo in _targets(config, "core")] == ["a"]
    assert len(_targets(config, None)) == 2
    with pytest.raises(ValueError, match="No repositories found"):
        _targets(config, "missing")


def test_status_error_and_dirty_paths(capsys) -> None:
    repos = [Repository(name="bad", path="."), Repository(name="dirty", path=".")]
    with patch("git_toolkit.cli.get_repo_status") as status:
        status.side_effect = [
            {"error": "broken"},
            {"error": None, "branch": "dev", "is_dirty": True, "ahead": 1, "behind": 2},
        ]
        assert _status(repos) == 1
    output = capsys.readouterr().out
    assert "ERROR" in output
    assert "Dirty" in output


def test_stats_table_and_markdown(capsys) -> None:
    config = Config(repositories=[Repository(name="repo", path=".")])
    value = {
        "success": True,
        "name": "repo",
        "active_branch": "main",
        "commit_count": 3,
        "contributor_count": 2,
        "stale_branches": [{"name": "old", "days_old": 90}],
        "large_files": [{"path": "big.bin", "size_kb": 2048}],
    }
    with patch("git_toolkit.cli.get_repo_stats", return_value=value):
        assert _stats(config, config.repositories, "table") == 0
        assert _stats(config, config.repositories, "markdown") == 0
    output = capsys.readouterr().out
    assert "1 stale" in output
    assert "Stale branch" in output
    assert "Large file" in output


def test_stats_failure_paths(capsys) -> None:
    config = Config(repositories=[Repository(name="repo", path=".")])
    value = {"success": False, "name": "repo", "message": "unavailable"}
    with patch("git_toolkit.cli.get_repo_stats", return_value=value):
        assert _stats(config, config.repositories, "markdown") == 1
        assert _stats(config, config.repositories, "table") == 1
    output = capsys.readouterr().out
    assert "unavailable" in output
