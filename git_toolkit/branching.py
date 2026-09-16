from __future__ import annotations

from typing import Any

from git import Repo

from .config import Repository, Safety
from .policy import evaluate_branch_name


def list_branches(repo_config: Repository) -> dict[str, Any]:
    repo = Repo(repo_config.path, search_parent_directories=False)
    active = None if repo.head.is_detached else repo.active_branch.name
    return {
        "name": repo_config.name,
        "success": True,
        "active": active,
        "branches": [branch.name for branch in repo.branches],
    }


def create_branch(
    repo_config: Repository,
    branch: str,
    *,
    start_point: str | None = None,
    safety: Safety | None = None,
    checkout: bool = False,
) -> dict[str, Any]:
    decision = evaluate_branch_name(branch, safety)
    if not decision.allowed:
        return {"name": repo_config.name, "success": False, "message": decision.reason, "policy_rule": decision.rule}
    repo = Repo(repo_config.path, search_parent_directories=False)
    if branch in [item.name for item in repo.branches]:
        return {"name": repo_config.name, "success": False, "message": f"Branch already exists: {branch}"}
    new_branch = repo.create_head(branch, start_point or "HEAD")
    if checkout:
        new_branch.checkout()
    return {"name": repo_config.name, "success": True, "message": f"Created branch {branch}"}


def delete_branch(
    repo_config: Repository,
    branch: str,
    *,
    safety: Safety | None = None,
    force: bool = False,
) -> dict[str, Any]:
    if safety and branch in safety.protect_branches:
        return {
            "name": repo_config.name,
            "success": False,
            "message": f"Cannot delete protected branch '{branch}'.",
            "policy_rule": "branch.delete.protected",
        }
    repo = Repo(repo_config.path, search_parent_directories=False)
    if not repo.head.is_detached and repo.active_branch.name == branch:
        return {"name": repo_config.name, "success": False, "message": "Cannot delete the active branch"}
    repo.delete_head(branch, force=force)
    return {"name": repo_config.name, "success": True, "message": f"Deleted branch {branch}"}
