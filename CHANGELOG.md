# Changelog

All notable changes to Git Toolkit are documented here.

The project follows Semantic Versioning and keeps unreleased work under `Unreleased` until a release tag is created.

## Unreleased

### Added

- Deterministic Git workflow orchestration across configured repositories.
- Rich repository status including dirty state and ahead/behind tracking.
- Core Git lifecycle commands: clone, fetch, pull, sync, checkout, commit, push, merge, rebase, tag, and submodule update.
- Structured safety policy for force-with-lease, protected branches, branch naming, clean worktrees, and remote-host governance.
- Layered global/project configuration with validation, initialization, display, and provenance explanation.
- Workflow execution with conditions, retries, timeouts, parallel execution, and stop/continue failure policy.
- Plugin discovery through package entry points and explicitly trusted local plugins.
- Trust gates for project scripts and hook scripts.
- OS-keyring credential management without credentialized remote URLs.
- Cross-platform CI on Linux, Windows, and macOS for Python 3.11-3.13.
- Ruff, mypy, Bandit, dependency-audit, coverage, build, and CLI smoke gates.

### Changed

- Canonical development version is `0.9.0.dev0` pending the 1.0 release cut.
- Python 3.11 is the supported minimum.
- The CLI is the supported 1.0 product surface; the web package is experimental.

### Security

- Removed PAT injection into Git remote URLs.
- Added explicit trust boundaries around project code execution.
- Restricted force-push support to force-with-lease and policy enforcement.
- Added dependency and static security scanning to CI.

## 1.0.0

This section will be finalized by the release-cut branch after all 1.0 readiness gates are integrated and green.
