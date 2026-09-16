# Development Tooling

Git Toolkit uses one canonical Python quality toolchain.

## Linting and style

Ruff is the project linter and style gate. Historical references to `flake8` and Black are obsolete for the current 1.0 line.

```bash
python -m ruff check git_toolkit --exclude git_toolkit/tests
```

Do not add a second formatting/linting stack unless there is a documented gap Ruff cannot cover.

## Type checking

```bash
python -m mypy git_toolkit --exclude "git_toolkit/tests/"
```

Production modules must remain type-check clean across the supported Python range.

## Security scanning

```bash
python -m bandit -r git_toolkit -ll -x git_toolkit/tests
python -m pip_audit
```

Bandit exceptions must be narrow, local, and justified in source. Dependency audit failures are release blockers unless formally triaged.

## Tests and coverage

```bash
python -m pytest --cov=git_toolkit --cov-report=term-missing --cov-fail-under=80
```

The 80% floor is a minimum release gate, not a target to game. Add tests around meaningful behavior and branch/error paths.

## Build

```bash
python -m build
```

A release candidate must produce both source and wheel distributions successfully.
