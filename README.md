# Git Toolkit

Git Toolkit is a deterministic Git workflow orchestration and policy-enforcement CLI for individual repositories and multi-repository workspaces.

The project standardizes repetitive Git operations through version-controlled configuration while keeping Git itself authoritative. It is designed for development teams, release managers, DevOps workflows, and repositories that need repeatable Git behavior without replacing native Git semantics.

**Current development version:** `0.9.0.dev0`

## Core capabilities

- Repository status with branch, HEAD, dirty state, upstream, ahead/behind, staged/unstaged, untracked, and conflict information.
- Core Git lifecycle: `clone`, `fetch`, `pull`, `push`, `checkout`, `commit`, `sync`, `merge`, `rebase`, `tag`, and submodule updates.
- Multi-repository execution and group selection.
- Declarative project configuration via `.git-toolkit.yml`.
- Optional global configuration via `~/.git-toolkit/config.yml`.
- Reusable workflows with conditions, retries, script timeouts, failure policy, and optional parallel execution.
- Lifecycle hooks and Python plugins.
- Project-local plugins under `.git-toolkit/plugins/` plus Python package entry-point plugins.
- Dry-run support for mutating operations.
- Repository analytics, execution history, and metadata caching.
- Cross-platform CI targeting Linux, Windows, and macOS.
- OS-keyring credential management without embedding credentials in Git remote URLs.

## Installation

For development:

```bash
python -m pip install -e ".[dev]"
```

For normal package use:

```bash
python -m pip install .
```

The command-line entry point is:

```bash
git-toolkit --help
```

## Configuration

Create `.git-toolkit.yml` in the project root:

```yaml
project:
  name: example

repositories:
  - name: app
    path: .
    groups: [core]

safety:
  prevent_force_push: true
  protect_branches:
    - main
    - master
  require_clean_worktree: true

workflows:
  verify-and-sync:
    failure_policy: stop
    steps:
      - name: status
        command: status
      - name: update
        command: sync
        if: repo.clean
      - name: tests
        script: python -m pytest
        timeout: 300
        retries: 1
```

Configuration precedence is:

```text
built-in defaults
       ↓
~/.git-toolkit/config.yml
       ↓
project .git-toolkit.yml
```

Inspect the effective configuration with:

```bash
git-toolkit config show
git-toolkit config validate
```

## Core commands

```text
git-toolkit status
git-toolkit clone
git-toolkit fetch
git-toolkit pull
git-toolkit sync
git-toolkit checkout <branch>
git-toolkit commit -m "message"
git-toolkit push
git-toolkit push --force-with-lease
git-toolkit merge <source>
git-toolkit rebase <onto>
git-toolkit tag <tag>
git-toolkit submodule update
git-toolkit stats
git-toolkit run <workflow>
git-toolkit history
git-toolkit clear-cache
```

Most repository commands accept `--group <name>` to operate on a configured subset.

## Sync semantics

`git-toolkit sync` is intentionally conservative. It:

1. requires a non-detached branch;
2. requires a clean working tree when policy requires it;
3. fetches and prunes `origin`;
4. resolves the current upstream;
5. performs a fast-forward-only merge.

Divergent history is reported for explicit resolution rather than silently rebased or merged.

## Push safety

Git Toolkit distinguishes a normal push from a requested force update. When force is requested it uses `--force-with-lease`, never an unconditional `--force` operation from the supported CLI.

Project policy may block force updates entirely or block them for protected branches. Hosting-provider policy remains authoritative: Git Toolkit does not bypass GitHub Push Protection, branch rules, required checks, or organization policy.

## Credentials

Git Toolkit does not inject PATs into HTTPS remote URLs. This avoids leaking credentials through logs, process output, exception messages, shell history, or repository remote configuration.

Git transport authentication is delegated to Git and the configured credential helper/Git Credential Manager. `git-toolkit auth` can manage host credentials in the operating-system keyring for explicit use and future provider adapters.

Do not place credentials in `.git-toolkit.yml`.

## Workflows

Workflow steps may use built-in Git commands or project scripts. Supported conditions currently include:

```text
repo.clean
repo.dirty
repo.exists
repo.detached
branch == <name>
```

Steps may define:

```yaml
continue_on_error: false
timeout: 300
retries: 2
```

Workflows may run repository work in parallel:

```bash
git-toolkit run verify --parallel --workers 4
```

## Plugins

Plugins are discovered from:

- the `git_toolkit.plugins` Python entry-point group;
- `.git-toolkit/plugins/*.py`.

Local plugin modules expose `plugin` as either a `Plugin` instance or a `Plugin` subclass. Plugins must declare a compatible plugin API version.

List loaded plugins with:

```bash
git-toolkit plugins list
```

## Runtime state

Logs, execution history, and cache data live under `.git-toolkit/` and are runtime artifacts. They are ignored by Git and must not be committed.

## Experimental web shell

The `web/` directory is experimental and is not part of the supported 1.0 interface. Optional dependencies can be installed with:

```bash
python -m pip install -e ".[web]"
uvicorn web.main:app --reload
```

The CLI remains the product surface until the core architecture and release gates are stable.

## Quality gates

The stabilization line requires:

- Linux, Windows, and macOS CI;
- Python 3.11, 3.12, and 3.13 coverage;
- Ruff linting;
- mypy type checking;
- Bandit source scanning;
- dependency auditing;
- package build verification;
- CLI smoke testing;
- minimum automated coverage of 80%.

Policy/security-critical paths should exceed the repository-wide minimum.

## Documentation

- [Architecture](docs/en/ARCHITECTURE.md)
- [Functional Requirements](docs/en/functional_requirements.md)
- [Technical Specifications](docs/en/Technical_specifications.md)
- [Developer Guide](docs/en/developer_guide.md)
- [How-To Guide](docs/en/how-to-guide.md)
- [Roadmap](ROADMAP.md)
- [Milestones](MILESTONES.md)
- [Security Policy](.github/SECURITY.md)
- [Contribution Guide](.github/CONTRIBUTING.md)

## License

MIT. See [LICENSE](LICENSE).
