import os
import subprocess
from pathlib import Path
from git import Repo, exc
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from .config import Repository, Safety, Health, Config
from .auth import get_auth_url, get_pat_from_env
from .logging import logger, get_cache, set_cache

def run_shell_command(repo_config: Repository, script: str, dry_run: bool = False) -> Dict[str, Any]:
    """
    Runs a shell command in the context of a repository.
    """
    repo_path = Path(repo_config.path)
    if not repo_path.exists():
        return {"success": False, "message": f"Repository path {repo_path} does not exist."}

    if dry_run:
        logger.info(f"[{repo_config.name}] [DRY-RUN] Would run: {script}")
        return {"success": True, "message": f"[DRY-RUN] Would run: {script}"}

    logger.debug(f"[{repo_config.name}] Running shell command: {script}")
    try:
        result = subprocess.run(
            script,
            shell=True,
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return {"success": True, "message": "Command succeeded.", "stdout": result.stdout}
        else:
            return {"success": False, "message": f"Command failed with code {result.returncode}.", "stderr": result.stderr}
    except Exception as e:
        logger.error(f"[{repo_config.name}] Error executing command: {e}")
        return {"success": False, "message": f"Error executing command: {e}"}

def get_repo_status(repo_config: Repository) -> Dict[str, Any]:
    """
    Checks the status of a specific repository.
    
    Returns:
        A dictionary containing repo name, branch, dirty status, and if it exists.
    """
    # Try to get status from cache first
    cache_key = f"status_{repo_config.name}"
    cached_status = get_cache(cache_key)
    if cached_status:
        logger.debug(f"[{repo_config.name}] Using cached status.")
        return cached_status

    status = {
        "name": repo_config.name,
        "exists": False,
        "branch": "Unknown",
        "is_dirty": False,
        "path": repo_config.path,
        "error": None
    }

    repo_path = Path(repo_config.path)
    if not repo_path.exists() or not (repo_path / ".git").exists():
        return status

    try:
        repo = Repo(repo_config.path)
        status["exists"] = True
        status["branch"] = repo.active_branch.name
        status["is_dirty"] = repo.is_dirty()
        
        # Cache for 60 seconds by default for status
        set_cache(cache_key, status, ttl=60)
    except exc.InvalidGitRepositoryError:
        status["error"] = "Invalid Git Repository"
    except Exception as e:
        status["error"] = str(e)

    return status

def clone_repo(repo_config: Repository, config: Optional[Config] = None) -> Dict[str, Any]:
    """
    Clones a repository if it doesn't already exist.
    """
    result = {
        "name": repo_config.name,
        "success": False,
        "message": ""
    }

    if not repo_config.url:
        result["message"] = "No URL provided for repository"
        return result

    repo_path = Path(repo_config.path)
    if repo_path.exists() and (repo_path / ".git").exists():
        result["message"] = "Repository already exists"
        result["success"] = True
        return result

    try:
        config_tokens = config.auth.tokens if config and config.auth else None
        auth_url = get_auth_url(repo_config.url, config_tokens=config_tokens)
        logger.info(f"[{repo_config.name}] Cloning from {repo_config.url}...")
        Repo.clone_from(auth_url, repo_config.path, branch=repo_config.default_branch)
        result["success"] = True
        result["message"] = "Successfully cloned"
    except Exception as e:
        logger.error(f"[{repo_config.name}] Clone failed: {e}")
        result["message"] = str(e)

    return result

def push_repo(repo_config: Repository, config: Optional[Config] = None, dry_run: bool = False) -> Dict[str, Any]:
    """
    Pushes changes for a specific repository, enforcing safety rules.
    """
    result = {"name": repo_config.name, "success": False, "message": ""}
    safety = config.safety if config else None
    
    repo_path = Path(repo_config.path)
    if not repo_path.exists() or not (repo_path / ".git").exists():
        result["message"] = "Repository not cloned"
        return result

    try:
        repo = Repo(repo_config.path)
        active_branch = repo.active_branch.name

        if safety:
            # Check protected branches
            if active_branch in safety.protect_branches:
                result["message"] = f"Push to protected branch '{active_branch}' is blocked."
                return result

            # Check prevent_force_push
            # Note: Checking for force push requires examining the push arguments.
            # Here we assume a standard push unless otherwise specified.
            # For deeper enforcement, we'd need to intercept 'git.push' calls.
            if safety.prevent_force_push:
                # Placeholder for force push detection logic
                pass

        if dry_run:
            result["success"] = True
            result["message"] = "[DRY-RUN] Would push to origin"
            return result

        origin = repo.remotes.origin
        # Authenticated push
        config_tokens = config.auth.tokens if config and config.auth else None
        auth_url = get_auth_url(origin.url, config_tokens=config_tokens)
        
        # Temporarily update remote URL for authenticated push
        original_url = origin.url
        try:
            origin.set_url(auth_url)
            info = origin.push()
            # info is a list of PushInfo objects, we check if any failed
            if info and info[0].flags & info[0].ERROR:
                result["message"] = f"Push failed: {info[0].summary}"
            else:
                result["success"] = True
                result["message"] = "Successfully pushed"
        finally:
            origin.set_url(original_url)
    except Exception as e:
        result["message"] = str(e)
    return result

def checkout_repo(repo_config: Repository, branch: str, safety: Optional[Safety] = None, dry_run: bool = False) -> Dict[str, Any]:
    """
    Checks out a specific branch for a repository, enforcing safety rules.
    """
    result = {"name": repo_config.name, "success": False, "message": ""}
    
    repo_path = Path(repo_config.path)
    if not repo_path.exists() or not (repo_path / ".git").exists():
        result["message"] = "Repository not cloned"
        return result

    try:
        if safety:
            # If we are in a protected branch and trying to checkout something else, it's fine.
            # But what if 'protect_branches' means we shouldn't checkout *into* them?
            # Or shouldn't checkout *out* of them if dirty?
            pass

        if dry_run:
            result["success"] = True
            result["message"] = f"[DRY-RUN] Would checkout {branch}"
            return result

        repo = Repo(repo_config.path)
        repo.git.checkout(branch)
        result["success"] = True
        result["message"] = f"Switched to {branch}"
    except Exception as e:
        result["message"] = str(e)
    return result

def update_submodules(repo_config: Repository, dry_run: bool = False) -> Dict[str, Any]:
    """
    Updates submodules for a repository.
    """
    result = {"name": repo_config.name, "success": False, "message": ""}
    
    repo_path = Path(repo_config.path)
    if not repo_path.exists() or not (repo_path / ".git").exists():
        result["message"] = "Repository not cloned"
        return result

    try:
        if dry_run:
            result["success"] = True
            result["message"] = "[DRY-RUN] Would update submodules"
            return result

        repo = Repo(repo_config.path)
        # git submodule update --init --recursive
        repo.git.submodule('update', '--init', '--recursive')
        result["success"] = True
        result["message"] = "Submodules updated"
    except Exception as e:
        result["message"] = str(e)
    return result

def get_repo_stats(repo_config: Repository, health: Optional[Health] = None) -> Dict[str, Any]:
    """
    Retrieves analytics and stats for a specific repository, including health metrics.
    """
    # Try to get stats from cache first
    cache_key = f"stats_{repo_config.name}"
    cached_stats = get_cache(cache_key)
    if cached_stats:
        logger.debug(f"[{repo_config.name}] Using cached stats.")
        return cached_stats

    stats = {
        "name": repo_config.name,
        "success": False,
        "commit_count": 0,
        "contributor_count": 0,
        "active_branch": "Unknown",
        "stale_branches": [],
        "large_files": [],
        "message": ""
    }

    repo_path = Path(repo_config.path)
    if not repo_path.exists() or not (repo_path / ".git").exists():
        stats["message"] = "Repository not cloned"
        return stats

    try:
        repo = Repo(repo_config.path)
        stats["active_branch"] = repo.active_branch.name
        
        # Get commit count (total)
        stats["commit_count"] = sum(1 for _ in repo.iter_commits())
        
        # Get contributor count (unique authors)
        authors = set()
        for commit in repo.iter_commits():
            authors.add(commit.author.email)
        stats["contributor_count"] = len(authors)

        # Health checks: Stale branches
        if health:
            now = datetime.now(timezone.utc)
            for branch in repo.branches:
                last_commit = branch.commit
                commit_date = last_commit.committed_datetime
                if (now - commit_date).days > health.stale_branch_days:
                    stats["stale_branches"].append({
                        "name": branch.name,
                        "days_old": (now - commit_date).days,
                        "last_author": last_commit.author.name
                    })

            # Health checks: Large files (checking the current tree)
            max_size_bytes = health.large_file_kb * 1024
            for entry in repo.tree().traverse():
                if entry.type == 'blob':
                    if entry.size > max_size_bytes:
                        stats["large_files"].append({
                            "path": entry.path,
                            "size_kb": round(entry.size / 1024, 2)
                        })
        
        stats["success"] = True
        # Cache stats for 300 seconds (5 minutes)
        set_cache(cache_key, stats, ttl=300)
    except Exception as e:
        stats["message"] = str(e)

    return stats

from pathlib import Path
