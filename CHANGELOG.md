# Changelog

All notable changes to Git Toolkit are documented here.

The project follows Semantic Versioning and keeps unreleased work under `Unreleased` until a release tag is created.

## Unreleased

### Added

### Changed

### Security

## 1.0.0 - 2026-09-23

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

- Version finalized as `1.0.0`.
- Python 3.11 is the supported minimum.
- The CLI is the supported 1.0 product surface; the web package is experimental.

### Security

- Removed PAT injection into Git remote URLs.
- Added explicit trust boundaries around project code execution.
- Restricted force-push support to force-with-lease and policy enforcement.
- Added dependency and static security scanning to CI.
