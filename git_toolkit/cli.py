import argparse
import sys
import concurrent.futures
import json
import urllib.request
from pathlib import Path
from typing import Any
from .config import load_config, Config, Step
from .git_wrapper import get_repo_status, clone_repo, push_repo, checkout_repo, update_submodules, get_repo_stats, run_shell_command
from .hooks import HookManager
from .plugins import PluginManager
from .auth import set_token, delete_token, get_token
from .logging import logger, log_execution, get_history, clear_cache

__version__ = "1.8.0-dev"

def execute_step(step: Step, repo_config: Any, config: Config, dry_run: bool) -> str:
    """
    Executes a single step for a specific repository and returns a status message.
    """
    # Basic 'if' condition check (just checks for branch name for now)
    if step.if_condition:
        status = get_repo_status(repo_config)
        if step.if_condition.startswith("branch == "):
            target_branch = step.if_condition.split(" == ")[1]
            if status.get("branch") != target_branch:
                return f"{repo_config.name}: Skipped (branch mismatch: {status.get('branch')} != {target_branch})"

    if step.command:
        # Built-in commands
        if step.command == "status":
            status = get_repo_status(repo_config)
            return f"{repo_config.name}: {status.get('branch', 'N/A')} - {'Dirty' if status.get('is_dirty') else 'Clean'}"
        elif step.command == "push":
            result = push_repo(repo_config, config, dry_run)
            return f"{repo_config.name}: {result['message']}"
        elif step.command == "clone":
            result = clone_repo(repo_config, config)
            return f"{repo_config.name}: {result['message']}"
        # Add more built-in commands as needed
        return f"{repo_config.name}: Unknown command {step.command}"
    elif step.script:
        result = run_shell_command(repo_config, step.script, dry_run)
        msg = f"{repo_config.name}: {result['message']}"
        if not result["success"] and not dry_run:
            if "stderr" in result:
                msg += f"\n  Error: {result['stderr']}"
        return msg
    return f"{repo_config.name}: Empty step"

def send_webhook_notification(url: str, workflow_name: str, results: list):
    """
    Sends a POST request to a webhook URL with the workflow results.
    """
    data = {
        "text": f"Git Toolkit Workflow '{workflow_name}' completed.",
        "workflow": workflow_name,
        "results": results
    }
    try:
        req = urllib.request.Request(
            url, 
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req) as response:
            if response.status >= 400:
                print(f"Webhook failed with status: {response.status}", file=sys.stderr)
    except Exception as e:
        print(f"Error sending webhook notification: {e}", file=sys.stderr)

def main():
    plugin_mgr = PluginManager()
    parser = argparse.ArgumentParser(
        description="Git Toolkit: A lightweight, per-project CLI utility for automating Git workflows."
    )
    parser.add_argument(
        "--config", 
        type=Path, 
        default=Path(".git-toolkit.yml"),
        help="Path to the .git-toolkit.yml configuration file."
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version=f"Git Toolkit v{__version__}"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the execution of commands without making any changes."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed debug logs."
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Placeholder for 'status' command
    status_parser = subparsers.add_parser("status", help="Show the status of repositories.")
    status_parser.add_argument("--group", help="Filter repositories by group.")
    
    # Placeholder for 'clone' command
    clone_parser = subparsers.add_parser("clone", help="Clone repositories defined in the config.")
    clone_parser.add_argument("--group", help="Filter repositories by group.")

    # New 'push' command
    push_parser = subparsers.add_parser("push", help="Push changes for all repositories.")
    push_parser.add_argument("--group", help="Filter repositories by group.")

    # New 'checkout' command
    checkout_parser = subparsers.add_parser("checkout", help="Checkout a specific branch for all repositories.")
    checkout_parser.add_argument("branch", help="The branch name to checkout.")
    checkout_parser.add_argument("--group", help="Filter repositories by group.")

    # New 'submodule' command
    submodule_parser = subparsers.add_parser("submodule", help="Update submodules for all repositories.")
    submodule_parser.add_argument("action", choices=["update"], help="Action to perform (e.g., update).")
    submodule_parser.add_argument("--group", help="Filter repositories by group.")

    # New 'stats' command
    stats_parser = subparsers.add_parser("stats", help="Display repository analytics and statistics.")
    stats_parser.add_argument("--format", choices=["table", "json", "markdown"], default="table", help="Output format (default: table).")
    stats_parser.add_argument("--group", help="Filter repositories by group.")

    # New 'run' command
    run_parser = subparsers.add_parser("run", help="Run a predefined workflow.")
    run_parser.add_argument("workflow", help="Name of the workflow to run.")
    run_parser.add_argument("--parallel", action="store_true", help="Run tasks in parallel.")
    run_parser.add_argument("--workers", type=int, default=4, help="Number of parallel workers (default: 4).")
    run_parser.add_argument("--group", help="Filter repositories by group.")

    # New 'auth' command
    auth_parser = subparsers.add_parser("auth", help="Manage authentication tokens.")
    auth_subparsers = auth_parser.add_subparsers(dest="auth_command", help="Authentication subcommands")
    
    auth_set_parser = auth_subparsers.add_parser("set", help="Set a token for a host.")
    auth_set_parser.add_argument("host", help="The host to set the token for (e.g., github.com).")
    auth_set_parser.add_argument("--token", required=True, help="The personal access token.")
    
    auth_delete_parser = auth_subparsers.add_parser("delete", help="Delete a token for a host.")
    auth_delete_parser.add_argument("host", help="The host to delete the token for.")

    auth_get_parser = auth_subparsers.add_parser("get", help="Get a token for a host (masked).")
    auth_get_parser.add_argument("host", help="The host to get the token for.")

    # New 'history' command
    history_parser = subparsers.add_parser("history", help="Show execution history.")
    history_parser.add_argument("--limit", type=int, default=10, help="Number of entries to show (default: 10).")

    # New 'clear-cache' command
    subparsers.add_parser("clear-cache", help="Clear the local metadata cache.")

    # Register all plugins' commands
    plugin_mgr.register_all_commands(subparsers)

    args = parser.parse_args()

    if args.verbose:
        logger.set_level(10) # logging.DEBUG

    # Load configuration
    try:
        config = load_config(args.config)
    except Exception as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        sys.exit(1)

    # Filter repositories by group if provided
    target_repositories = config.repositories
    if hasattr(args, 'group') and args.group:
        target_repositories = [r for r in config.repositories if args.group in r.groups]
        if not target_repositories:
            print(f"No repositories found for group: {args.group}", file=sys.stderr)
            sys.exit(1)

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Initialize hook manager
    hook_mgr = HookManager(config.hooks, plugin_mgr)

    # Command routing
    if args.command == "status":
        if not hook_mgr.run_hook("pre_status"):
            sys.exit(1)
        
        print(f"{'Repository':<20} {'Branch':<15} {'Status':<10}")
        print("-" * 45)
        for repo_config in target_repositories:
            status = get_repo_status(repo_config)
            if not status["exists"]:
                display_status = "Not Cloned"
                branch = "N/A"
            else:
                display_status = "Dirty" if status["is_dirty"] else "Clean"
                branch = status["branch"]
            
            if status["error"]:
                display_status = f"Error: {status['error']}"

            print(f"{repo_config.name:<20} {branch:<15} {display_status:<10}")
        
        hook_mgr.run_hook("post_status")

    elif args.command == "clone":
        if not hook_mgr.run_hook("pre_clone"):
            sys.exit(1)
            
        print(f"{'Repository':<20} {'Status':<30}")
        print("-" * 50)
        for repo_config in target_repositories:
            result = clone_repo(repo_config, config)
            status_msg = result["message"]
            print(f"{repo_config.name:<20} {status_msg:<30}")

        hook_mgr.run_hook("post_clone")
    elif args.command == "push":
        if not hook_mgr.run_hook("pre_push"):
            sys.exit(1)
        print(f"{'Repository':<20} {'Status':<30}")
        print("-" * 50)
        for repo_config in target_repositories:
            result = push_repo(repo_config, config, args.dry_run)
            print(f"{repo_config.name:<20} {result['message']:<30}")
        hook_mgr.run_hook("post_push")
    elif args.command == "checkout":
        if not hook_mgr.run_hook("pre_checkout"):
            sys.exit(1)
        print(f"{'Repository':<20} {'Status':<30}")
        print("-" * 50)
        for repo_config in target_repositories:
            result = checkout_repo(repo_config, args.branch, config.safety, args.dry_run)
            print(f"{repo_config.name:<20} {result['message']:<30}")
        hook_mgr.run_hook("post_checkout")
    elif args.command == "submodule":
        if args.action == "update":
            if not hook_mgr.run_hook("pre_submodule_update"):
                sys.exit(1)
            print(f"{'Repository':<20} {'Status':<30}")
            print("-" * 50)
            for repo_config in target_repositories:
                result = update_submodules(repo_config, args.dry_run)
                print(f"{repo_config.name:<20} {result['message']:<30}")
            hook_mgr.run_hook("post_submodule_update")
    elif args.command == "stats":
        if args.format == "json":
            import json
            stats_list = []
            for repo_config in target_repositories:
                stats_list.append(get_repo_stats(repo_config, config.health))
            print(json.dumps(stats_list, indent=2))
        elif args.format == "markdown":
            print("# Repository Analytics Report")
            print(f"Generated on: {Path('.').absolute()}\n")
            for repo_config in target_repositories:
                stats = get_repo_stats(repo_config, config.health)
                print(f"## {repo_config.name}")
                if not stats["success"]:
                    print(f"**Error:** {stats['message']}\n")
                    continue
                
                print(f"- **Active Branch:** {stats['active_branch']}")
                print(f"- **Total Commits:** {stats['commit_count']}")
                print(f"- **Contributors:** {stats['contributor_count']}")
                
                if stats["stale_branches"]:
                    print("\n### ⚠️ Stale Branches")
                    print("| Branch | Days Old | Last Author |")
                    print("| --- | --- | --- |")
                    for b in stats["stale_branches"]:
                        print(f"| {b['name']} | {b['days_old']} | {b['last_author']} |")
                
                if stats["large_files"]:
                    print("\n### ⚠️ Large Files")
                    print("| File Path | Size (KB) |")
                    print("| --- | --- |")
                    for f in stats["large_files"]:
                        print(f"| {f['path']} | {f['size_kb']} |")
                print("")
        else:
            print(f"{'Repository':<20} {'Branch':<15} {'Commits':<10} {'Authors':<10} {'Health':<10}")
            print("-" * 75)
            for repo_config in target_repositories:
                stats = get_repo_stats(repo_config, config.health)
                if not stats["success"]:
                    print(f"{repo_config.name:<20} {'Error':<15} {stats['message']:<30}")
                else:
                    health_status = "OK"
                    if stats["stale_branches"] or stats["large_files"]:
                        warnings = []
                        if stats["stale_branches"]: warnings.append(f"{len(stats['stale_branches'])} stale")
                        if stats["large_files"]: warnings.append(f"{len(stats['large_files'])} large")
                        health_status = "⚠️ " + ", ".join(warnings)
                    
                    print(f"{repo_config.name:<20} {stats['active_branch']:<15} {stats['commit_count']:<10} {stats['contributor_count']:<10} {health_status:<10}")
    elif args.command == "run":
        if args.workflow not in config.workflows:
            print(f"Workflow '{args.workflow}' not found in configuration.", file=sys.stderr)
            sys.exit(1)
        
        workflow = config.workflows[args.workflow]
        print(f"Running workflow: {args.workflow}")
        if workflow.description:
            print(f"Description: {workflow.description}")
        print("-" * 50)

        all_results = []
        # Basic implementation: execution across all repositories
        for step in workflow.steps:
            step_name = step.name or step.command or step.script or "unnamed step"
            print(f"\n[Step] {step_name}")
            
            if args.parallel:
                with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
                    futures = {executor.submit(execute_step, step, repo, config, args.dry_run): repo for repo in target_repositories}
                    for future in concurrent.futures.as_completed(futures):
                        res = future.result()
                        print(res)
                        all_results.append(res)
            else:
                for repo_config in target_repositories:
                    res = execute_step(step, repo_config, config, args.dry_run)
                    print(res)
                    all_results.append(res)

        if workflow.webhook_url and not args.dry_run:
            print(f"\nSending notification to webhook...")
            send_webhook_notification(workflow.webhook_url, args.workflow, all_results)

    elif args.command == "auth":
        if args.auth_command == "set":
            set_token(args.host, args.token)
            print(f"Token for {args.host} stored successfully.")
        elif args.auth_command == "delete":
            delete_token(args.host)
            print(f"Token for {args.host} deleted successfully.")
        elif args.auth_command == "get":
            token = get_token(args.host)
            if token:
                masked = token[:4] + "*" * (len(token) - 8) + token[-4:] if len(token) > 8 else "****"
                print(f"Token for {args.host}: {masked}")
            else:
                print(f"No token found for {args.host}.")
        else:
            auth_parser.print_help()

    elif args.command == "history":
        history = get_history(args.limit)
        if not history:
            print("No execution history found.")
        else:
            print(f"{'Timestamp':<25} {'Command':<15} {'Status':<10}")
            print("-" * 55)
            for entry in history:
                timestamp = entry['timestamp'][:19].replace('T', ' ')
                print(f"{timestamp:<25} {entry['command']:<15} {entry['status']:<10}")

    elif args.command == "clear-cache":
        clear_cache()
        print("Metadata cache cleared successfully.")

    elif plugin_mgr.handle_command(args):
        pass # Plugin handled the command
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        sys.exit(1)

    # Log successful execution
    if args.command and args.command != "history":
        log_execution(args.command, vars(args), "SUCCESS")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Get args if possible
        import sys
        command = "unknown"
        if len(sys.argv) > 1:
            command = sys.argv[1]
        
        log_execution(command, {"args": sys.argv[2:]}, "FAILED", str(e))
        logger.error(f"Execution failed: {e}")
        sys.exit(1)
