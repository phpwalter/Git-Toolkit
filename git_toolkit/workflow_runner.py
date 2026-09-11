import concurrent.futures
from typing import List, Dict, Any
from .config import Config, Workflow
from .git_wrapper import get_repo_status, clone_repo, push_repo, checkout_repo, update_submodules, get_repo_stats, run_shell_command
from .logging import logger

def execute_step(step, repo_config, config, dry_run):
    """
    Executes a single step for a specific repository and returns a status message.
    (This is a simplified version for now)
    """
    if step.command:
        if step.command == "status":
            status = get_repo_status(repo_config)
            return f"{repo_config.name}: {status.get('branch', 'N/A')} - {'Dirty' if status.get('is_dirty') else 'Clean'}"
        elif step.command == "push":
            result = push_repo(repo_config, config, dry_run)
            return f"{repo_config.name}: {result['message']}"
        # Add other built-in commands here...
    elif step.script:
        result = run_shell_command(repo_config, step.script, dry_run)
        return f"{repo_config.name}: {result['message']}"
    return f"{repo_config.name}: Unknown or empty step"

def run_workflow(workflow: Workflow, config: Config, parallel: bool = False, workers: int = 4, dry_run: bool = False) -> List[str]:
    """
    Runs a given workflow across all target repositories.
    """
    all_results = []
    target_repositories = config.repositories

    for step in workflow.steps:
        step_name = step.name or step.command or step.script or "unnamed step"
        logger.info(f"Running step: {step_name}")

        if parallel:
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                futures = {executor.submit(execute_step, step, repo, config, dry_run): repo for repo in target_repositories}
                for future in concurrent.futures.as_completed(futures):
                    res = future.result()
                    all_results.append(res)
        else:
            for repo_config in target_repositories:
                res = execute_step(step, repo_config, config, dry_run)
                all_results.append(res)
    
    return all_results
