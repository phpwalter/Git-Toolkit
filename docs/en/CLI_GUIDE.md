# Git Toolkit CLI Guide

Git Toolkit provides deterministic Git workflow orchestration across one or more repositories defined in `.git-toolkit.yml`.

## Install

```bash
python -m pip install -e .
git-toolkit --version
```

## Initialize configuration

```bash
git-toolkit config init
git-toolkit config validate
git-toolkit config show
```

Use `git-toolkit config explain safety.prevent_force_push` to see the effective value and the layer that supplied it.

## Repository status

```bash
git-toolkit status
git-toolkit status --group core
```

Status reports branch, dirty/clean state, and ahead/behind counts.

## Git lifecycle

```bash
git-toolkit clone
git-toolkit fetch
git-toolkit pull
git-toolkit sync
git-toolkit checkout feature/example
git-toolkit commit -m "feat: describe the change"
git-toolkit push
git-toolkit merge feature/example
git-toolkit rebase main
git-toolkit tag v1.0.0
git-toolkit submodule update
```

Mutating operations support the global `--dry-run` option where implemented.

## Force push

Git Toolkit never exposes an unconditional force push. The only supported rewrite request is:

```bash
git-toolkit push --force-with-lease
```

Project policy may still deny it.

## Workflows

```bash
git-toolkit run verify
git-toolkit run verify --parallel --workers 4
```

Workflow steps support conditions, retries, timeouts, and stop/continue failure policy.

## Analytics

```bash
git-toolkit stats
git-toolkit stats --format json
git-toolkit stats --format markdown
```

## Plugins

```bash
git-toolkit plugins list
git-toolkit plugins doctor
```

Local plugins are disabled unless the project explicitly opts in with `security.allow_local_plugins: true`.

## Credentials

Git Toolkit stores explicitly managed credentials in the OS keyring and never embeds credentials into remote URLs.

```bash
git-toolkit auth set github.com --token <value>
git-toolkit auth get github.com
git-toolkit auth delete github.com
```

Prefer Git Credential Manager for normal Git transport authentication.

## Exit behavior

- `0`: command succeeded.
- non-zero: at least one requested operation failed or the command/configuration was invalid.

Use `--verbose` for additional runtime logging during diagnosis.
