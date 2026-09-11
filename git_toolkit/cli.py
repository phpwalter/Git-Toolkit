from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Callable

from .auth import delete_token, get_token, set_token
from .config import Command, Config, load_config
from .git_wrapper import (
    checkout_repo,
    clone_repo,
    commit_repo,
    fetch_repo,
    get_repo_stats,
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
from .hooks import HookManager
from .logging import clear_cache, get_history, log_execution, logger
from .plugins import PluginManager
from .version import __version__
from .workflow_runner import execute_step, run_workflow, send_webhook_notification


def _bootstrap_config(argv: list[str]) -> Path:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--config", type=Path, default=Path(".git-toolkit.yml"))
    known, _ = parser.parse_known_args(argv)
    return known.config


def _add_repo_filter(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--group", help="Operate only on repositories in this group.")


def _build_parser(config: Config, plugin_mgr: PluginManager) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="git-toolkit",
        description="Deterministic Git workflow orchestration and policy enforcement.",
    )
    parser.add_argument("--config", type=Path, default=Path(".git-toolkit.yml"))
    parser.add_argument("--version", action="version", version=f"Git Toolkit v{__version__}")
    parser.add_argument("--dry-run", action="store_true", help="Describe mutations without applying them.")
    parser.add_argument("--verbose", action="store_true")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    for name, help_text in (
        ("status", "Show repository state."),
        ("clone", "Clone configured repositories."),
        ("fetch", "Fetch and prune configured repositories."),
        ("pull", "Fast-forward configured repositories."),
        ("sync", "Fetch and fast-forward configured repositories deterministically."),
    ):
        child = subparsers.add_parser(name, help=help_text)
        _add_repo_filter(child)

    push = subparsers.add_parser("push", help="Push configured repositories.")
    push.add_argument(
        "--force-with-lease",
        action="store_true",
        help="Request a force-with-lease push; policy may still block it.",
    )
    _add_repo_filter(push)

    checkout = subparsers.add_parser("checkout", help="Checkout a branch.")
    checkout.add_argument("branch")
    _add_repo_filter(checkout)

    commit = subparsers.add_parser("commit", help="Stage all changes and commit them.")
    commit.add_argument("-m", "--message", required=True)
    _add_repo_filter(commit)

    merge = subparsers.add_parser("merge", help="Merge a source branch/ref using --no-ff.")
    merge.add_argument("source")
    _add_repo_filter(merge)

    rebase = subparsers.add_parser("rebase", help="Rebase onto a branch/ref.")
    rebase.add_argument("onto")
    _add_repo_filter(rebase)

    tag = subparsers.add_parser("tag", help="Create a local tag.")
    tag.add_argument("tag")
    _add_repo_filter(tag)

    submodule = subparsers.add_parser("submodule", help="Manage submodules.")
    submodule.add_argument("action", choices=["update"])
    _add_repo_filter(submodule)

    stats = subparsers.add_parser("stats", help="Display repository analytics.")
    stats.add_argument("--format", choices=["table", "json", "markdown"], default="table")
    _add_repo_filter(stats)

    run = subparsers.add_parser("run", help="Run a configured workflow.")
    run.add_argument("workflow")
    run.add_argument("--parallel", action="store_true")
    run.add_argument("--workers", type=int, default=4)
    _add_repo_filter(run)

    auth = subparsers.add_parser("auth", help="Manage credentials in the OS keyring.")
    auth_sub = auth.add_subparsers(dest="auth_command")
    auth_set = auth_sub.add_parser("set")
    auth_set.add_argument("host")
    auth_set.add_argument("--token", required=True)
    auth_get = auth_sub.add_parser("get")
    auth_get.add_argument("host")
    auth_delete = auth_sub.add_parser("delete")
    auth_delete.add_argument("host")

    config_cmd = subparsers.add_parser("config", help="Inspect effective configuration.")
    config_sub = config_cmd.add_subparsers(dest="config_command")
    config_sub.add_parser("validate")
    config_show = config_sub.add_parser("show")
    config_show.add_argument("--format", choices=["json", "yaml"], default="json")

    plugins = subparsers.add_parser("plugins", help="Inspect installed plugins.")
    plugin_sub = plugins.add_subparsers(dest="plugin_command")
    plugin_sub.add_parser("list")
    plugin_sub.add_parser("doctor")

    history = subparsers.add_parser("history", help="Show execution history.")
    history.add_argument("--limit", type=int, default=10)
    subparsers.add_parser("clear-cache", help="Clear Git Toolkit metadata cache.")

    reserved = set(subparsers.choices)
    for name, command in config.commands.items():
        if name in reserved:
            raise ValueError(f"Custom command '{name}' conflicts with a built-in command")
        custom = subparsers.add_parser(name, help=command.description or "Configured command")
        _add_repo_filter(custom)
        custom.set_defaults(_custom_command=name)

    plugin_mgr.register_all_commands(subparsers)
    return parser


def _targets(config: Config, group: str | None) -> list[Any]:
    if not group:
        return config.repositories
    repositories = [repo for repo in config.repositories if group in repo.groups]
    if not repositories:
        raise ValueError(f"No repositories found for group: {group}")
    return repositories


def _print_results(results: list[dict[str, Any]]) -> int:
    failed = False
    print(f"{'Repository':<24} Status")
    print("-" * 72)
    for result in results:
        failed = failed or not bool(result.get("success"))
        print(f"{result.get('name', 'unknown'):<24} {result.get('message', '')}")
    return 1 if failed else 0


def _run_repo_operation(
    targets: list[Any],
    operation: Callable[[Any], dict[str, Any]],
) -> int:
    return _print_results([operation(repo) for repo in targets])


def _status(targets: list[Any]) -> int:
    failed = False
    print(f"{'Repository':<20} {'Branch':<18} {'State':<8} {'Ahead':>5} {'Behind':>6}")
    print("-" * 68)
    for repo in targets:
        state = get_repo_status(repo)
        if state.get("error"):
            failed = True
            print(f"{repo.name:<20} {'N/A':<18} ERROR    {state['error']}")
            continue
        label = "Dirty" if state.get("is_dirty") else "Clean"
        print(
            f"{repo.name:<20} {state.get('branch', 'N/A'):<18} {label:<8} "
            f"{state.get('ahead', 0):>5} {state.get('behind', 0):>6}"
        )
    return 1 if failed else 0


def _stats(config: Config, targets: list[Any], output_format: str) -> int:
    values = [get_repo_stats(repo, config.health) for repo in targets]
    if output_format == "json":
        print(json.dumps(values, indent=2))
        return 1 if any(not value.get("success") for value in values) else 0
    if output_format == "markdown":
        print("# Repository Analytics Report")
        for value in values:
            print(f"\n## {value['name']}")
            if not value.get("success"):
                print(f"**Error:** {value.get('message', '')}")
                continue
            print(f"- **Active Branch:** {value['active_branch']}")
            print(f"- **Total Commits:** {value['commit_count']}")
            print(f"- **Contributors:** {value['contributor_count']}")
            for branch in value.get("stale_branches", []):
                print(f"- Stale branch: `{branch['name']}` ({branch['days_old']} days)")
            for file in value.get("large_files", []):
                print(f"- Large file: `{file['path']}` ({file['size_kb']} KB)")
        return 1 if any(not value.get("success") for value in values) else 0

    print(f"{'Repository':<20} {'Branch':<18} {'Commits':>8} {'Authors':>8} {'Health':<18}")
    print("-" * 80)
    for value in values:
        if not value.get("success"):
            print(f"{value['name']:<20} ERROR: {value.get('message', '')}")
            continue
        warnings: list[str] = []
        if value.get("stale_branches"):
            warnings.append(f"{len(value['stale_branches'])} stale")
        if value.get("large_files"):
            warnings.append(f"{len(value['large_files'])} large")
        health = ", ".join(warnings) or "OK"
        print(
            f"{value['name']:<20} {value['active_branch']:<18} "
            f"{value['commit_count']:>8} {value['contributor_count']:>8} {health:<18}"
        )
    return 1 if any(not value.get("success") for value in values) else 0


def _run_custom(command: Command, config: Config, targets: list[Any], dry_run: bool) -> int:
    if not command.script:
        print("Configured command has no executable script.", file=sys.stderr)
        return 2
    if not config.security.allow_project_scripts:
        print(
            "Configured script is blocked. Set security.allow_project_scripts: true only "
            "for trusted repositories.",
            file=sys.stderr,
        )
        return 1
    return _print_results(
        [
            {"name": repo.name, **run_shell_command(repo, command.script, dry_run)}
            for repo in targets
        ]
    )


def _dispatch(args: argparse.Namespace, config: Config, plugin_mgr: PluginManager) -> int:
    group = getattr(args, "group", None)
    targets = _targets(config, group) if config.repositories else []
    hook_mgr = HookManager(
        config.hooks,
        plugin_mgr,
        allow_project_scripts=config.security.allow_project_scripts,
    )

    if args.command == "status":
        return _status(targets)
    if args.command == "clone":
        return _run_repo_operation(targets, lambda repo: clone_repo(repo, config))
    if args.command == "fetch":
        return _run_repo_operation(targets, lambda repo: fetch_repo(repo, args.dry_run))
    if args.command == "pull":
        return _run_repo_operation(targets, lambda repo: pull_repo(repo, args.dry_run))
    if args.command == "sync":
        return _run_repo_operation(targets, lambda repo: sync_repo(repo, config, args.dry_run))
    if args.command == "push":
        if not hook_mgr.run_hook("pre_push"):
            return 1
        code = _run_repo_operation(
            targets,
            lambda repo: push_repo(repo, config, args.dry_run, args.force_with_lease),
        )
        hook_mgr.run_hook("post_push")
        return code
    if args.command == "checkout":
        return _run_repo_operation(
            targets,
            lambda repo: checkout_repo(repo, args.branch, config.safety, args.dry_run),
        )
    if args.command == "commit":
        return _run_repo_operation(targets, lambda repo: commit_repo(repo, args.message, args.dry_run))
    if args.command == "merge":
        return _run_repo_operation(targets, lambda repo: merge_repo(repo, args.source, args.dry_run))
    if args.command == "rebase":
        return _run_repo_operation(targets, lambda repo: rebase_repo(repo, args.onto, args.dry_run))
    if args.command == "tag":
        return _run_repo_operation(targets, lambda repo: tag_repo(repo, args.tag, args.dry_run))
    if args.command == "submodule":
        return _run_repo_operation(targets, lambda repo: update_submodules(repo, args.dry_run))
    if args.command == "stats":
        return _stats(config, targets, args.format)
    if args.command == "run":
        workflow = config.workflows.get(args.workflow)
        if workflow is None:
            print(f"Workflow '{args.workflow}' not found.", file=sys.stderr)
            return 2
        results = run_workflow(workflow, config, targets, args.parallel, args.workers, args.dry_run)
        for result in results:
            print(result)
        if workflow.webhook_url and not args.dry_run:
            send_webhook_notification(workflow.webhook_url, args.workflow, results)
        return 1 if any(": FAILED -" in result for result in results) else 0
    if args.command == "auth":
        if args.auth_command == "set":
            set_token(args.host, args.token)
            print(f"Credential for {args.host} stored in OS keyring.")
            return 0
        if args.auth_command == "get":
            token = get_token(args.host)
            print("configured" if token else "not configured")
            return 0
        if args.auth_command == "delete":
            delete_token(args.host)
            print(f"Credential for {args.host} deleted.")
            return 0
        return 2
    if args.command == "config":
        if args.config_command == "validate":
            print("Configuration is valid.")
            return 0
        if args.config_command == "show":
            data = config.model_dump(by_alias=True, exclude={"auth": {"tokens"}})
            if args.format == "json":
                print(json.dumps(data, indent=2, default=str))
            else:
                import yaml

                print(yaml.safe_dump(data, sort_keys=False))
            return 0
        return 2
    if args.command == "plugins":
        diagnostics = plugin_mgr.diagnostics()
        if args.plugin_command == "list":
            for plugin in diagnostics["plugins"]:
                print(plugin)
            return 0
        if args.plugin_command == "doctor":
            print(json.dumps(diagnostics, indent=2))
            return 1 if diagnostics["errors"] else 0
        return 2
    if args.command == "history":
        print(json.dumps(get_history(args.limit), indent=2))
        return 0
    if args.command == "clear-cache":
        clear_cache()
        print("Cache cleared.")
        return 0
    if hasattr(args, "_custom_command"):
        return _run_custom(config.commands[args._custom_command], config, targets, args.dry_run)
    if plugin_mgr.handle_command(args):
        return 0
    return 2


def main() -> None:
    argv = sys.argv[1:]
    config_path = _bootstrap_config(argv)
    try:
        config = load_config(config_path)
        plugin_mgr = PluginManager(allow_local_plugins=config.security.allow_local_plugins)
        parser = _build_parser(config, plugin_mgr)
        args = parser.parse_args(argv)
        if args.verbose:
            logger.set_level(10)
        if not args.command:
            parser.print_help()
            return
        code = _dispatch(args, config, plugin_mgr)
        log_execution(args.command, vars(args), "success" if code == 0 else "failure")
        if code:
            raise SystemExit(code)
    except (ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
