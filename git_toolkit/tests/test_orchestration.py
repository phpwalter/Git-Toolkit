from __future__ import annotations

from git_toolkit.config import Repository
from git_toolkit.orchestration import run_repositories, summarize


def _repos() -> list[Repository]:
    return [Repository(name="a", path="."), Repository(name="b", path=".")]


def test_sequential_stop_on_failure() -> None:
    calls: list[str] = []

    def operation(repo: Repository) -> dict[str, object]:
        calls.append(repo.name)
        return {"name": repo.name, "success": repo.name != "a"}

    results = run_repositories(_repos(), operation, stop_on_failure=True)
    assert [result["name"] for result in results] == ["a"]
    assert calls == ["a"]


def test_parallel_results_preserve_repository_order() -> None:
    results = run_repositories(
        _repos(),
        lambda repo: {"name": repo.name, "success": True},
        parallel=True,
        workers=2,
    )
    assert [result["name"] for result in results] == ["a", "b"]


def test_parallel_exception_becomes_failure_result() -> None:
    def operation(repo: Repository) -> dict[str, object]:
        if repo.name == "b":
            raise RuntimeError("boom")
        return {"name": repo.name, "success": True}

    results = run_repositories(_repos(), operation, parallel=True, workers=2)
    assert results[1]["success"] is False
    assert results[1]["message"] == "boom"


def test_summary_reports_aggregate_failure() -> None:
    summary = summarize([
        {"name": "a", "success": True},
        {"name": "b", "success": False},
    ])
    assert summary == {
        "total": 2,
        "succeeded": 1,
        "failed": 1,
        "success": False,
        "failed_repositories": ["b"],
    }
