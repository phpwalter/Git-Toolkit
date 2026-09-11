from __future__ import annotations

import concurrent.futures
import json
import time
import urllib.request
from dataclasses import dataclass
from typing import Any

from .config import Config, Repository, Step, Workflow
from .git_wrapper import (
    checkout_repo,
    clone_repo,
    commit_repo,
    fetch_repo,
    get_repo_status,
    merge_repo,
    pull_repo,
    push_repo,
    rebase_repo,
    run_shell_command,
    sync_repo,
    tag_repo,
    update_submodules,
)
from .logging import logger


@dataclass(frozen=True)
class StepResult:
    repository: str
    step: str
    success: bool
    skipped: bool = False
    message: str = ""

    def render(self) -> str:
        if self.skipped:
            return f"{self.repository}: Skipped ({self.message})"
        state = "OK" if self.success else "FAILED"
        return f"{self.repository}: {state} - {self.message}"


def _condition_matches(condition: str | None, repo_config: Repository) -> tuple[bool, str]:
    if not condition:
        return True, ""
    status = get_repo_status(repo_config)
    normalized = condition.strip()
    predicates: dict[str, bool] = {
        "repo.clean": not bool(status.get("is_dirty")),
        "repo.dirty": bool(status.get("is_dirty")),
        "repo.exists": bool(status.get("exists")),
        "repo.detached": bool(status.get("detached")),
    }
    if normalized in predicates:
        return predicates[normalized], normalized
    if normalized.startswith("branch == "):
        expected = normalized.split(" == ", 1)[1].strip().strip("'\"")
        return status.get("branch") == expected, f"branch != {expected}"
    raise ValueError(f"Unsupported workflow condition: {condition}")


def _execute_builtin(step: Step, repo_config: Repository, config: Config, dry_run: bool) -> dict[str, Any]:
    command = step.command or ""
    args = step.args
    if command == "status":
        status = get_repo_status(repo_config)
        if status.get("error"):
            return {"success": False, "message": str(status["error"])}
        state = "Dirty" if status.get("is_dirty") else "Clean"
        return {"success": True, "message": f"{status.get('branch', 'N/A')} - {state}"}
    if command == "clone":
        return clone_repo(repo_config, config)
    if command == "fetch":
        return fetch_repo(repo_config, dry_run)
    if command == "pull":
        return pull_repo(repo_config, dry_run)
    if command == "push":
        return push_repo(repo_config, config, dry_run, force=bool(args.get("force", False)))
    if command == "checkout":
        branch = str(args.get("branch") or "")
        if not branch:
            return {"success": False, "message": "checkout requires args.branch"}
        return checkout_repo(repo_config, branch, config.safety, dry_run)
    if command == "commit":
        message = str(args.get("message") or "")
        if not message:
            return {"success": False, "message": "commit requires args.message"}
        return commit_repo(repo_config, message, dry_run)
    if command == "sync":
        return sync_repo(repo_config, config, dry_run)
    if command == "merge":
        source = str(args.get("source") or "")
        if not source:
            return {"success": False, "message": "merge requires args.source"}
        return merge_repo(repo_config, source, dry_run)
    if command == "rebase":
        onto = str(args.get("onto") or "")
        if not onto:
            return {"success": False, "message": "rebase requires args.onto"}
        return rebase_repo(repo_config, onto, dry_run)
    if command == "tag":
        tag = str(args.get("tag") or "")
        if not tag:
            return {"success": False, "message": "tag requires args.tag"}
        return tag_repo(repo_config, tag, dry_run)
    if command == "submodule-update":
        return update_submodules(repo_config, dry_run)
    return {"success": False, "message": f"Unknown command {command}"}


def execute_step(step: Step, repo_config: Repository, config: Config, dry_run: bool) -> str:
    """Execute one workflow step with condition, timeout and retry semantics."""
    matches, reason = _condition_matches(step.if_condition, repo_config)
    if not matches:
        return StepResult(repo_config.name, step.name or step.command or "step", True, True, reason).render()

    attempts = max(1, step.retries + 1)
    last: dict[str, Any] = {"success": False, "message": "not executed"}
    for attempt in range(1, attempts + 1):
        if step.command:
            last = _execute_builtin(step, repo_config, config, dry_run)
        elif step.script:
            last = run_shell_command(repo_config, step.script, dry_run, timeout=step.timeout)
        else:
            last = {"success": False, "message": "Empty step"}
        if last.get("success"):
            break
        if attempt < attempts:
            time.sleep(min(attempt, 3))

    return StepResult(
        repo_config.name,
        step.name or step.command or step.script or "step",
        bool(last.get("success")),
        False,
        str(last.get("message", "")),
    ).render()


def run_workflow(
    workflow: Workflow,
    config: Config,
    repositories: list[Repository] | None = None,
    parallel: bool = False,
    workers: int = 4,
    dry_run: bool = False,
) -> list[str]:
    """Run a workflow across selected repositories.

    ``failure_policy=stop`` stops scheduling later steps after a failed result.
    ``continue`` executes every step. Individual steps may also set
    ``continue_on_error``.
    """
    targets = repositories if repositories is not None else config.repositories
    all_results: list[str] = []

    for step in workflow.steps:
        logger.info("Running step: %s", step.name or step.command or "script")
        step_results: list[str] = []
        if parallel and len(targets) > 1:
            with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
                futures = [executor.submit(execute_step, step, repo, config, dry_run) for repo in targets]
                for future in concurrent.futures.as_completed(futures):
                    step_results.append(future.result())
        else:
            step_results = [execute_step(step, repo, config, dry_run) for repo in targets]

        all_results.extend(step_results)
        failed = any(": FAILED -" in result for result in step_results)
        if failed and workflow.failure_policy == "stop" and not step.continue_on_error:
            break

    return all_results


def send_webhook_notification(url: str, workflow_name: str, results: list[str]) -> None:
    payload = {
        "text": f"Git Toolkit Workflow '{workflow_name}' completed.",
        "workflow": workflow_name,
        "results": results,
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:  # nosec B310 - user-configured webhook
            if response.status >= 400:
                logger.error("Webhook failed with status: %s", response.status)
    except Exception as exc:
        logger.error("Error sending webhook notification: %s", exc)
