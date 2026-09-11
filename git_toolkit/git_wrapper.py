from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from git import GitCommandError, InvalidGitRepositoryError, NoSuchPathError, Repo

from .config import Config, Health, Repository, Safety
from .logging import get_cache, set_cache
from .policy import evaluate_clean_worktree, evaluate_force_push


def _open_repo(repo_config: Repository) -> Repo:
    return Repo(repo_config.path, search_parent_directories=False)


def _denied_message(reason: str, remediation: str | None) -> str:
    return f"{reason} Remediation: {remediation}" if remediation else reason


def run_shell_command(
    repo_config: Repository,
    script: str,
    dry_run: bool = False,
    timeout: int | None = None,
) -> dict[str, Any]:
    repo_path = Path(repo_config.path)
    if not repo_path.exists():
        return {"success": False, "message": f"Repository path {repo_path} does not exist."}
    if dry_run:
        return {"success": True, "message": f"[DRY-RUN] Would run: {script}"}
    try:
        result = subprocess.run(  # nosec B602 - explicit trusted workflow feature
            script,
            shell=True,
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"success": False, "message": f"Command timed out after {timeout}s."}
    if result.returncode == 0:
        return {"success": True, "message": "Command succeeded.", "stdout": result.stdout}
    return {
        "success": False,
        "message": f"Command failed with code {result.returncode}.",
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def get_repo_status(repo_config: Repository) -> dict[str, Any]:
    cache_key = f"status_{repo_config.name}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    status: dict[str, Any] = {
        "name": repo_config.name,
        "exists": False,
        "branch": "Unknown",
        "detached": False,
        "head_sha": None,
        "upstream": None,
        "ahead": 0,
        "behind": 0,
        "is_dirty": False,
        "staged": False,
        "unstaged": False,
        "untracked": 0,
        "conflicted": 0,
        "path": repo_config.path,
        "error": None,
    }
    try:
        repo = _open_repo(repo_config)
        status["exists"] = True
        status["detached"] = repo.head.is_detached
        status["head_sha"] = repo.head.commit.hexsha
        status["branch"] = "DETACHED" if repo.head.is_detached else repo.active_branch.name
        status["is_dirty"] = repo.is_dirty(untracked_files=True)
        status["untracked"] = len(repo.untracked_files)
        status["staged"] = bool(repo.index.diff("HEAD"))
        status["unstaged"] = bool(repo.index.diff(None))
        status["conflicted"] = len(repo.index.unmerged_blobs())

        if not repo.head.is_detached:
            tracking = repo.active_branch.tracking_branch()
            if tracking is not None:
                status["upstream"] = tracking.name
                counts = repo.git.rev_list("--left-right", "--count", f"{tracking.name}...HEAD")
                behind, ahead = (int(value) for value in counts.split())
                status["ahead"] = ahead
                status["behind"] = behind
        set_cache(cache_key, status, ttl=30)
    except (InvalidGitRepositoryError, NoSuchPathError):
        status["error"] = "Invalid Git repository"
    except Exception as exc:
        status["error"] = str(exc)
    return status


def clone_repo(repo_config: Repository, config: Config | None = None) -> dict[str, Any]:
    del config
    if not repo_config.url:
        return {"name": repo_config.name, "success": False, "message": "No URL provided"}
    path = Path(repo_config.path)
    if path.exists():
        try:
            _open_repo(repo_config)
            return {"name": repo_config.name, "success": True, "message": "Repository already exists"}
        except Exception:
            if any(path.iterdir()):
                return {
                    "name": repo_config.name,
                    "success": False,
                    "message": "Destination exists and is not a Git repository",
                }
    try:
        kwargs: dict[str, Any] = {}
        if repo_config.default_branch:
            kwargs["branch"] = repo_config.default_branch
        Repo.clone_from(repo_config.url, repo_config.path, **kwargs)
        return {"name": repo_config.name, "success": True, "message": "Successfully cloned"}
    except Exception as exc:
        return {"name": repo_config.name, "success": False, "message": str(exc)}


def push_repo(
    repo_config: Repository,
    config: Config | None = None,
    dry_run: bool = False,
    force: bool = False,
) -> dict[str, Any]:
    safety = config.safety if config else None
    try:
        repo = _open_repo(repo_config)
        if repo.head.is_detached:
            return {"name": repo_config.name, "success": False, "message": "Cannot push detached HEAD"}
        branch = repo.active_branch.name
        decision = evaluate_force_push(branch, force, safety)
        if not decision.allowed:
            return {
                "name": repo_config.name,
                "success": False,
                "message": _denied_message(decision.reason, decision.remediation),
                "policy_rule": decision.rule,
            }
        if dry_run:
            mode = "force-with-lease" if force else "normal"
            return {"name": repo_config.name, "success": True, "message": f"[DRY-RUN] Would perform {mode} push"}

        args = ["--force-with-lease"] if force else []
        infos = repo.remotes.origin.push(*args)
        failures = [info.summary for info in infos if info.flags & info.ERROR]
        if failures:
            return {"name": repo_config.name, "success": False, "message": "; ".join(failures)}
        return {"name": repo_config.name, "success": True, "message": "Successfully pushed"}
    except Exception as exc:
        return {"name": repo_config.name, "success": False, "message": str(exc)}


def fetch_repo(repo_config: Repository, dry_run: bool = False) -> dict[str, Any]:
    try:
        repo = _open_repo(repo_config)
        if dry_run:
            return {"name": repo_config.name, "success": True, "message": "[DRY-RUN] Would fetch --prune"}
        repo.remotes.origin.fetch(prune=True)
        return {"name": repo_config.name, "success": True, "message": "Fetched origin"}
    except Exception as exc:
        return {"name": repo_config.name, "success": False, "message": str(exc)}


def pull_repo(repo_config: Repository, dry_run: bool = False) -> dict[str, Any]:
    try:
        repo = _open_repo(repo_config)
        if repo.is_dirty(untracked_files=True):
            return {"name": repo_config.name, "success": False, "message": "Working tree is dirty"}
        if dry_run:
            return {"name": repo_config.name, "success": True, "message": "[DRY-RUN] Would pull --ff-only"}
        repo.git.pull("--ff-only")
        return {"name": repo_config.name, "success": True, "message": "Fast-forward pull complete"}
    except Exception as exc:
        return {"name": repo_config.name, "success": False, "message": str(exc)}


def commit_repo(repo_config: Repository, message: str, dry_run: bool = False) -> dict[str, Any]:
    try:
        repo = _open_repo(repo_config)
        if not repo.is_dirty(untracked_files=True):
            return {"name": repo_config.name, "success": False, "message": "Nothing to commit"}
        if dry_run:
            return {"name": repo_config.name, "success": True, "message": f"[DRY-RUN] Would commit: {message}"}
        repo.git.add("-A")
        commit = repo.index.commit(message)
        return {"name": repo_config.name, "success": True, "message": f"Committed {commit.hexsha[:12]}"}
    except Exception as exc:
        return {"name": repo_config.name, "success": False, "message": str(exc)}


def sync_repo(repo_config: Repository, config: Config | None = None, dry_run: bool = False) -> dict[str, Any]:
    safety = config.safety if config else None
    try:
        repo = _open_repo(repo_config)
        if repo.head.is_detached:
            return {"name": repo_config.name, "success": False, "message": "Cannot sync detached HEAD"}
        decision = evaluate_clean_worktree(
            is_dirty=repo.is_dirty(untracked_files=True),
            safety=safety,
            operation="sync",
        )
        if not decision.allowed:
            return {
                "name": repo_config.name,
                "success": False,
                "message": _denied_message(decision.reason, decision.remediation),
                "policy_rule": decision.rule,
            }
        if dry_run:
            return {"name": repo_config.name, "success": True, "message": "[DRY-RUN] Would fetch and fast-forward"}
        repo.remotes.origin.fetch(prune=True)
        tracking = repo.active_branch.tracking_branch()
        if tracking is None:
            return {"name": repo_config.name, "success": False, "message": "Current branch has no upstream"}
        repo.git.merge("--ff-only", tracking.name)
        return {"name": repo_config.name, "success": True, "message": f"Synchronized with {tracking.name}"}
    except GitCommandError as exc:
        return {"name": repo_config.name, "success": False, "message": f"Sync requires manual resolution: {exc}"}
    except Exception as exc:
        return {"name": repo_config.name, "success": False, "message": str(exc)}


def checkout_repo(
    repo_config: Repository,
    branch: str,
    safety: Safety | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    try:
        repo = _open_repo(repo_config)
        decision = evaluate_clean_worktree(
            is_dirty=repo.is_dirty(untracked_files=True),
            safety=safety,
            operation="checkout",
        )
        if not decision.allowed:
            return {
                "name": repo_config.name,
                "success": False,
                "message": _denied_message(decision.reason, decision.remediation),
                "policy_rule": decision.rule,
            }
        if dry_run:
            return {"name": repo_config.name, "success": True, "message": f"[DRY-RUN] Would checkout {branch}"}
        repo.git.checkout(branch)
        return {"name": repo_config.name, "success": True, "message": f"Switched to {branch}"}
    except Exception as exc:
        return {"name": repo_config.name, "success": False, "message": str(exc)}


def merge_repo(repo_config: Repository, source: str, dry_run: bool = False) -> dict[str, Any]:
    try:
        repo = _open_repo(repo_config)
        if repo.is_dirty(untracked_files=True):
            return {"name": repo_config.name, "success": False, "message": "Working tree is dirty"}
        if dry_run:
            return {"name": repo_config.name, "success": True, "message": f"[DRY-RUN] Would merge {source}"}
        repo.git.merge("--no-ff", source)
        return {"name": repo_config.name, "success": True, "message": f"Merged {source}"}
    except Exception as exc:
        return {"name": repo_config.name, "success": False, "message": str(exc)}


def rebase_repo(repo_config: Repository, onto: str, dry_run: bool = False) -> dict[str, Any]:
    try:
        repo = _open_repo(repo_config)
        if repo.is_dirty(untracked_files=True):
            return {"name": repo_config.name, "success": False, "message": "Working tree is dirty"}
        if dry_run:
            return {"name": repo_config.name, "success": True, "message": f"[DRY-RUN] Would rebase onto {onto}"}
        repo.git.rebase(onto)
        return {"name": repo_config.name, "success": True, "message": f"Rebased onto {onto}"}
    except Exception as exc:
        return {"name": repo_config.name, "success": False, "message": str(exc)}


def tag_repo(repo_config: Repository, tag: str, dry_run: bool = False) -> dict[str, Any]:
    try:
        repo = _open_repo(repo_config)
        if dry_run:
            return {"name": repo_config.name, "success": True, "message": f"[DRY-RUN] Would create tag {tag}"}
        repo.create_tag(tag)
        return {"name": repo_config.name, "success": True, "message": f"Created tag {tag}"}
    except Exception as exc:
        return {"name": repo_config.name, "success": False, "message": str(exc)}


def update_submodules(repo_config: Repository, dry_run: bool = False) -> dict[str, Any]:
    try:
        repo = _open_repo(repo_config)
        if dry_run:
            return {"name": repo_config.name, "success": True, "message": "[DRY-RUN] Would update submodules"}
        repo.git.submodule("update", "--init", "--recursive")
        return {"name": repo_config.name, "success": True, "message": "Submodules updated"}
    except Exception as exc:
        return {"name": repo_config.name, "success": False, "message": str(exc)}


def get_repo_stats(repo_config: Repository, health: Health | None = None) -> dict[str, Any]:
    cache_key = f"stats_{repo_config.name}"
    cached = get_cache(cache_key)
    if cached:
        return cached
    stats: dict[str, Any] = {
        "name": repo_config.name,
        "success": False,
        "commit_count": 0,
        "contributor_count": 0,
        "active_branch": "Unknown",
        "stale_branches": [],
        "large_files": [],
        "message": "",
    }
    try:
        repo = _open_repo(repo_config)
        stats["active_branch"] = "DETACHED" if repo.head.is_detached else repo.active_branch.name
        commits = list(repo.iter_commits())
        stats["commit_count"] = len(commits)
        stats["contributor_count"] = len({commit.author.email for commit in commits})
        if health:
            now = datetime.now(timezone.utc)
            for branch in repo.branches:
                age = (now - branch.commit.committed_datetime).days
                if age > health.stale_branch_days:
                    stats["stale_branches"].append(
                        {"name": branch.name, "days_old": age, "last_author": branch.commit.author.name}
                    )
            maximum = health.large_file_kb * 1024
            for entry in repo.tree().traverse():
                if entry.type == "blob" and entry.size > maximum:
                    stats["large_files"].append(
                        {"path": entry.path, "size_kb": round(entry.size / 1024, 2)}
                    )
        stats["success"] = True
        set_cache(cache_key, stats, ttl=300)
    except Exception as exc:
        stats["message"] = str(exc)
    return stats
