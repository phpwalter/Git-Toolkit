# Git Toolkit Architecture

## Purpose

Git Toolkit is a deterministic Git workflow orchestration and policy-enforcement tool for individual repositories and multi-repository workspaces. The CLI is the supported 1.0 product surface; the web shell is experimental.

## Architectural principles

1. **Git remains authoritative.** Git Toolkit orchestrates Git; it does not replace repository semantics.
2. **Configuration is declarative and layered.** Built-in defaults are overridden by global configuration and then project configuration.
3. **Policy is explicit.** Mutating operations must be able to explain why they are allowed or denied.
4. **Credentials are never persisted in project configuration or injected into remote URLs.** Git/GCM or future credential-provider adapters own transport authentication.
5. **Workflow execution has one implementation.** The CLI delegates workflow behavior to `workflow_runner.py`.
6. **Dry-run must not mutate repository state.**
7. **Cross-platform behavior is a release requirement.** Linux, Windows, and macOS are exercised by CI.

## Component model

```text
CLI
 |
 +-- Config Resolver
 |
 +-- Workflow Runner -------- Hooks
 |          |                 Plugins
 |          +---- Step execution
 |
 +-- Git Adapter ------------ GitPython / native Git
 |
 +-- Runtime Services ------- Logging / history / cache
```

### CLI (`git_toolkit/cli.py`)

Owns argument parsing, repository selection, presentation, and exit codes. It does not implement Git algorithms or workflow orchestration.

### Configuration (`git_toolkit/config.py`)

Resolves configuration in this order, lowest precedence first:

1. model defaults;
2. `~/.git-toolkit/config.yml`;
3. project `.git-toolkit.yml`.

Secrets are not an accepted runtime source from version-controlled YAML. The legacy `auth.tokens` field may parse for migration compatibility but is excluded from effective serialized configuration and ignored by Git operations.

### Git adapter (`git_toolkit/git_wrapper.py`)

Provides repository state and core operations. Current supported operations include status, clone, fetch, pull, push, checkout, commit, sync, merge, rebase, tag, and submodule update.

Repository status includes branch/detached state, HEAD SHA, upstream, ahead/behind counts, dirty state, staged/unstaged changes, untracked files, and conflicts.

`sync` is intentionally conservative: it fetches/prunes and performs a fast-forward-only merge against the configured upstream. Divergent history is reported for manual resolution rather than guessed at.

### Workflow runner (`git_toolkit/workflow_runner.py`)

Owns workflow execution. It supports repository iteration, optional parallelism, conditions, retries, timeouts for scripts, failure policy, built-in Git operations, and webhook notifications.

### Hooks (`git_toolkit/hooks.py`)

Hooks are trusted executable project configuration. Pre-hooks may block an operation. Hook commands therefore require the same repository trust assumptions as project scripts.

### Plugins (`git_toolkit/plugins.py`)

Plugins can be discovered from Python package entry points or `.git-toolkit/plugins/*.py`. Plugins declare an API version and are rejected when incompatible. A local plugin module must expose `plugin` as either a Plugin instance or Plugin subclass.

### Authentication (`git_toolkit/auth.py`)

Git Toolkit does not rewrite repository remotes with embedded credentials. OS keyring support remains available for explicit credential management, while Git/GCM remains the transport authentication authority. Provider-specific adapters may be added later.

### Observability (`git_toolkit/logging.py`)

Execution history, logs, and cache are runtime state under `.git-toolkit/`. They are intentionally ignored by Git and must not be committed.

## Product boundaries

### Supported for 1.0

- CLI operation
- per-project and global configuration
- multi-repository orchestration
- hooks and plugins
- core Git lifecycle
- repository health/status
- safety enforcement
- execution history and caching
- CI/CD use

### Experimental / post-1.0

- web/GUI management
- OAuth browser flows
- non-Git VCS support
- advanced organization-wide analytics

## Release gates

A 1.0 release requires:

- supported behavior and documentation to agree;
- Linux, Windows, and macOS CI to pass;
- supported Python versions to pass;
- package build and CLI smoke test to pass;
- dependency and source security scans to pass;
- at least 80% automated coverage, with higher coverage expected for policy-critical paths;
- no committed runtime/build artifacts;
- no credentials in repository history.
