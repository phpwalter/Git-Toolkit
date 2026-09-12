# Functional Requirements — Git Toolkit

**Status:** Active specification for the 0.9 stabilization line and 1.0 release gate.

## 1. Purpose

Git Toolkit provides deterministic Git workflow orchestration and policy enforcement for individual repositories and multi-repository workspaces. The supported 1.0 product surface is the CLI. The web shell is experimental.

## 2. Supported environment

- Python 3.11, 3.12, and 3.13.
- Standard Git installations.
- Windows, macOS, and Linux.
- Interactive developer environments and CI/CD systems.

## 3. Core CLI requirements

The system SHALL provide first-class commands for:

- `status`
- `clone`
- `fetch`
- `pull`
- `checkout`
- `commit`
- `push`
- `sync`
- `merge`
- `rebase`
- `tag`
- `submodule update`
- `stats`
- `run`
- `auth`
- `config`
- `plugins`
- `history`
- `clear-cache`

Configured project commands SHALL also be executable by name when their execution requirements are satisfied.

## 4. Repository-state requirements

`status` SHALL report enough information for safe automation, including:

- repository existence;
- active branch or detached HEAD;
- HEAD SHA;
- upstream branch;
- ahead/behind counts;
- dirty state;
- staged and unstaged state;
- untracked-file count;
- conflict state.

The implementation SHALL use Git repository semantics rather than relying solely on the presence of a `.git/` directory.

## 5. Configuration requirements

Configuration SHALL resolve deterministically in this order, lowest precedence first:

1. built-in defaults;
2. `~/.git-toolkit/config.yml`;
3. project `.git-toolkit.yml`.

The system SHALL validate the effective configuration and SHALL provide commands to inspect it.

Version-controlled configuration SHALL NOT be treated as a source of runtime credentials.

## 6. Git-operation safety requirements

The system SHALL:

- use fast-forward-only behavior for deterministic pull/sync operations unless an explicit merge/rebase operation is requested;
- refuse unsafe operations on detached HEAD where appropriate;
- enforce configured clean-worktree requirements;
- distinguish normal push from history-rewriting push;
- use `--force-with-lease`, not unconditional `--force`, for supported history-rewriting pushes;
- allow policy to prohibit force push globally;
- prohibit force push to configured protected branches;
- return an explicit policy rule, reason, and remediation for policy denials where supported.

Hosting-provider policy remains authoritative. Git Toolkit SHALL NOT attempt to bypass repository rules, secret scanning, required checks, or organization policy.

## 7. Workflow requirements

The workflow engine SHALL be implemented once and consumed by the CLI.

Workflows SHALL support:

- ordered steps;
- built-in Git steps;
- trusted script steps;
- repository selection;
- optional parallel repository execution;
- branch and repository-state conditions;
- retries;
- script timeouts;
- stop/continue failure policy;
- per-step `continue_on_error`;
- optional webhook notification.

Future workflow DAG/output-passing features are not required for 1.0 unless promoted into the active release gate.

## 8. Script and hook trust requirements

Project scripts and project hook scripts execute checked-out repository content and SHALL therefore be disabled by default.

A trusted repository MAY explicitly opt in with:

```yaml
security:
  allow_project_scripts: true
```

Pre-hooks SHALL be able to block the associated operation when they fail.

## 9. Plugin requirements

The system SHALL support:

- Python package entry-point plugins;
- project-local plugins only after explicit trust opt-in;
- plugin API version compatibility checks;
- command registration;
- hook participation;
- plugin diagnostics.

Project-local plugins SHALL be disabled by default.

## 10. Authentication requirements

The system SHALL NOT embed credentials in Git remote URLs.

Git transport authentication SHALL be delegated to Git/Git Credential Manager/credential helpers until provider-specific adapters are introduced.

Git Toolkit MAY store explicitly managed host credentials in the operating-system keyring. Credential values SHALL NOT be emitted by status or inspection commands.

## 11. Observability requirements

The system SHALL provide:

- execution history;
- runtime logging;
- bounded metadata caching;
- secret-aware argument scrubbing for execution history.

Runtime logs, cache, history, coverage data, and package-build metadata SHALL NOT be committed to the repository.

## 12. Quality requirements

Before `1.0.0`:

- Linux, Windows, and macOS CI SHALL pass;
- supported Python versions SHALL pass;
- linting SHALL pass;
- type checking SHALL pass;
- source security scanning SHALL pass;
- dependency audit SHALL pass;
- package build SHALL pass;
- CLI smoke test SHALL pass;
- automated code coverage SHALL be at least 80% repository-wide;
- policy/security-critical paths SHOULD approach complete branch coverage.

## 13. Documentation requirements

Documentation SHALL distinguish implemented, experimental, planned, and deprecated behavior. User-facing documentation SHALL not describe planned functionality as currently supported.

The architecture, README, security/support guidance, roadmap, and release requirements SHALL agree before the 1.0 release.

## 14. Explicitly experimental/post-1.0

The following are not supported 1.0 guarantees:

- full GUI/web management;
- browser OAuth flows;
- non-Git VCS support;
- organization-wide advanced analytics;
- workflow dependency DAGs and cross-step output passing.
