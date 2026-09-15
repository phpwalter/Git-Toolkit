from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any, Callable

from .config import Repository


@dataclass(frozen=True)
class RepoResult:
    index: int
    name: str
    success: bool
    payload: dict[str, Any]


def run_repositories(
    repositories: list[Repository],
    operation: Callable[[Repository], dict[str, Any]],
    *,
    parallel: bool = False,
    workers: int = 4,
    stop_on_failure: bool = False,
) -> list[dict[str, Any]]:
    if workers < 1:
        raise ValueError("workers must be >= 1")

    if not parallel:
        results: list[dict[str, Any]] = []
        for repo in repositories:
            result = operation(repo)
            results.append(result)
            if stop_on_failure and not result.get("success", False):
                break
        return results

    ordered: dict[int, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(operation, repo): (index, repo) for index, repo in enumerate(repositories)}
        for future in as_completed(futures):
            index, repo = futures[future]
            try:
                result = future.result()
            except Exception as exc:
                result = {"name": repo.name, "success": False, "message": str(exc)}
            ordered[index] = result
    return [ordered[index] for index in sorted(ordered)]


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    succeeded = sum(1 for result in results if result.get("success"))
    failed = len(results) - succeeded
    return {
        "total": len(results),
        "succeeded": succeeded,
        "failed": failed,
        "success": failed == 0,
        "failed_repositories": [result.get("name") for result in results if not result.get("success")],
    }
