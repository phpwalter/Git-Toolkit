# Git Toolkit Roadmap

**Current line:** `0.9.0.dev0`  
**Primary objective:** converge implementation, policy, tests, packaging, and documentation into a trustworthy `1.0.0` release.

## Product direction

Git Toolkit is a deterministic Git workflow orchestration and policy-enforcement CLI for individual repositories and multi-repository workspaces. The CLI is the supported 1.0 product surface. Web/GUI work remains experimental until the core release contract is stable.

## 0.9 Stabilization

### Repository hygiene

- [x] Remove committed coverage output.
- [x] Remove committed runtime history and logs.
- [x] Remove generated `*.egg-info` metadata.
- [x] Expand `.gitignore` for build, test, runtime, IDE, and secret-bearing local files.

### Versioning and packaging

- [x] Establish `git_toolkit/version.py` as the runtime version source.
- [x] Align package metadata on `0.9.0.dev0`.
- [x] Require Python 3.11+.
- [x] Separate experimental web dependencies from the core package.

### Core Git lifecycle

- [x] Rich repository status model.
- [x] Clone.
- [x] Fetch/prune.
- [x] Fast-forward-only pull.
- [x] Checkout with dirty-tree policy.
- [x] Commit.
- [x] Push.
- [x] Force-with-lease request with policy enforcement.
- [x] Deterministic sync.
- [x] Merge.
- [x] Rebase.
- [x] Tag.
- [x] Submodule update.

### Policy and safety

- [x] Dedicated structured policy decision engine.
- [x] Default force-push prevention.
- [x] Protected-branch force-push blocking.
- [x] Clean-worktree requirement for sensitive operations.
- [x] Policy rule/reason/remediation metadata.
- [x] No unconditional force-push option in the supported CLI.
- [x] Hosting-provider rules remain authoritative.
- [ ] Add branch-name policy enforcement.
- [ ] Add remote allow/deny policy.

### Configuration

- [x] Built-in defaults.
- [x] Global config at `~/.git-toolkit/config.yml`.
- [x] Project config at `.git-toolkit.yml`.
- [x] Deterministic global → project merge.
- [x] Effective-config inspection and validation commands.
- [x] Config-defined commands are executable from the CLI.
- [x] Version-controlled `auth.tokens` is ignored by runtime credential handling.
- [x] Project scripts are disabled by default and require explicit trust opt-in.
- [x] Project-local plugins are disabled by default and require explicit trust opt-in.
- [ ] Add explicit CLI/environment override reporting to `config show`.
- [ ] Add `config explain <path>` provenance reporting.

### Authentication

- [x] Stop embedding credentials in HTTPS remote URLs.
- [x] Keep explicit OS-keyring credential lifecycle commands.
- [x] Delegate transport authentication to Git/GCM/credential helpers.
- [ ] Add provider-specific credential adapters without remote mutation.
- [ ] Add OAuth only after the CLI 1.0 contract is stable.

### Workflows

- [x] One workflow execution engine.
- [x] Built-in Git workflow steps.
- [x] Trusted script steps.
- [x] Conditions.
- [x] Retries.
- [x] Script timeouts.
- [x] Failure policy.
- [x] Optional repository parallelism.
- [x] Webhook notification.
- [ ] Dependency DAGs (`depends_on`).
- [ ] Structured step outputs and output passing.
- [ ] Explicit rollback/compensation hooks.

### Plugins and hooks

- [x] Package entry-point plugin discovery.
- [x] Project-local plugin discovery behind explicit trust.
- [x] Plugin API compatibility checks.
- [x] Plugin diagnostics.
- [x] Plugin hook participation.
- [ ] Add plugin isolation guidance and capability declarations.

### CI and quality

- [x] Linux CI.
- [x] Windows CI.
- [x] macOS CI.
- [x] Python 3.11–3.13 matrix.
- [x] Ruff.
- [x] mypy.
- [x] Bandit.
- [x] dependency audit.
- [x] package build verification.
- [x] CLI smoke test.
- [x] 80% minimum coverage gate.
- [x] Direct policy-engine unit coverage.
- [ ] Raise policy/security critical paths toward 100% coverage.
- [ ] Add documentation-link validation.
- [ ] Add explicit secret-scanning regression test data rules.

### Documentation and governance

- [x] Architecture specification.
- [x] Functional requirements reconciled to the 0.9/1.0 contract.
- [x] Support policy.
- [x] CODEOWNERS.
- [x] README aligned with implemented behavior.
- [x] Experimental web boundary documented.
- [ ] Reconcile remaining historical milestone/technical-guide language with the 0.9 implementation.
- [ ] Complete localized-document parity after English source documents stabilize.

## 1.0 Release Gate

`1.0.0` is permitted only when all of the following are true:

1. Supported behavior and documentation agree.
2. Linux, Windows, and macOS CI are green.
3. Supported Python versions are green.
4. Package build and installed CLI smoke tests pass.
5. No committed runtime/build artifacts remain.
6. No credentials exist in repository history introduced by the release line.
7. Minimum repository coverage is 80% and safety-critical paths have substantially higher coverage.
8. Core Git operations fail safely on dirty, detached, divergent, or unauthorized states.
9. Workflow execution has deterministic stop/continue semantics.
10. Experimental web behavior is not represented as a supported 1.0 capability.

## Post-1.0

After 1.0, priority moves to richer policy modeling, workflow DAGs, provider authentication adapters, organization-level reporting, and eventually a supported web/GUI surface. Non-Git VCS support remains exploratory and is not part of the near-term product definition.
