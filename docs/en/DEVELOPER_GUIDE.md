# Git Toolkit Developer Guide

## Development environment

Git Toolkit supports Python 3.11 through 3.13.

```bash
python -m venv .venv
. .venv/bin/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Quality gates

Run the same core checks used by CI:

```bash
python -m ruff check git_toolkit --exclude git_toolkit/tests
python -m mypy git_toolkit --exclude "git_toolkit/tests/"
python -m bandit -r git_toolkit -ll -x git_toolkit/tests
python -m pytest --cov=git_toolkit --cov-report=term-missing --cov-fail-under=80
python -m build
```

## Architecture

Core modules are intentionally separated by responsibility:

- `config.py`: schema, layering, initialization, provenance.
- `policy.py`: deterministic allow/deny decisions.
- `git_wrapper.py`: Git adapter boundary.
- `workflow_runner.py`: workflow execution.
- `hooks.py`: lifecycle hooks.
- `plugins.py`: plugin discovery and API compatibility.
- `logging.py`: runtime history/cache/logging.
- `cli.py`: argument parsing and routing.

## Test-writing guidelines

Tests should assert public behavior and policy rules rather than implementation details. Prefer deterministic mocks around Git/network boundaries. Every defect fix should include a regression test. Avoid test-order dependencies and clear/patch caches explicitly when testing cached paths.

## Plugin development

Package plugins are discovered through the `git_toolkit.plugins` entry-point group. Plugins must inherit from `Plugin` and expose an API version compatible with `PLUGIN_API_VERSION`.

Local plugins are intentionally disabled by default. A project must explicitly set `security.allow_local_plugins: true` before `.git-toolkit/plugins/*.py` files are loaded.

## Hooks and scripts

Project scripts and configured hook scripts are trust boundaries. They are disabled by default and require `security.allow_project_scripts: true`.

Do not place credentials in configuration, scripts, logs, tests, fixtures, or remote URLs.

## Documentation contributions

English source documentation under `docs/en/` is authoritative until translation synchronization is enabled. Preserve command names, paths, configuration keys, code, and identifiers exactly in translated documentation.
