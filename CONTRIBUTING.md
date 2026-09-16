# Contributing to Git Toolkit

Git Toolkit is designed around deterministic behavior, explicit policy, and cross-platform compatibility. Contributions should preserve those properties.

## Development environment

Use Python 3.11 or newer and install the development dependencies:

```bash
python -m venv .venv
python -m pip install -e ".[dev]"
```

Run the same mandatory checks used by CI before opening a pull request:

```bash
python -m ruff check git_toolkit --exclude git_toolkit/tests
python -m mypy git_toolkit --exclude "git_toolkit/tests/"
python -m bandit -r git_toolkit -ll -x git_toolkit/tests
python -m pytest --cov=git_toolkit --cov-report=term-missing --cov-fail-under=80
python -m pip_audit
python -m build
python -m git_toolkit.cli --version
```

## Contribution requirements

A pull request should:

- have one coherent purpose;
- include regression tests for behavior changes;
- preserve the configured coverage floor;
- keep Linux, Windows, and macOS behavior aligned;
- fail closed when invalid policy or security-sensitive input is encountered;
- avoid introducing hidden defaults or nondeterministic behavior;
- update documentation when public behavior changes.

Do not weaken a security, policy, package-integrity, coverage, or release gate to make a change pass.

## Shell execution and plugins

Prefer argv-based execution with `shell=False`. Shell execution must remain explicitly trust-gated. Project-local scripts and plugins must never become implicitly trusted.

## Compatibility

Supported runtime versions are Python 3.11, 3.12, and 3.13. A change that intentionally alters a public CLI, configuration, plugin, workflow, or policy contract should document the compatibility impact.

## Commit messages

Use concise, descriptive commit messages. Conventional-style subjects are preferred, for example:

```text
feat: add repository policy check
fix: preserve remote safety on fetch

test: cover protected branch rejection
```

## Pull requests

Keep pull requests reviewable. Describe the problem, the implementation, tests performed, and any follow-up work intentionally left out of scope. Draft pull requests are appropriate while CI or integration work remains incomplete.
