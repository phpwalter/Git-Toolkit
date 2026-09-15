# Git Toolkit 1.0 Release Readiness

A 1.0 release candidate is ready only when every required gate is satisfied.

## Code quality

- Ruff passes on production code.
- mypy passes on production code.
- Bandit reports no release-blocking findings.
- `pip-audit` reports no untriaged release-blocking vulnerabilities.

## Tests

- Full test suite passes on Linux, Windows, and macOS.
- Python 3.11, 3.12, and 3.13 are covered by CI.
- Coverage is at least 80% without lowering or bypassing the configured threshold.
- New policy/error paths have regression coverage.

## Package

- Wheel and source distribution build successfully.
- `twine check` succeeds.
- Wheel installs into a fresh virtual environment.
- Installed `git-toolkit --version` and `--help` work outside the repository checkout.

## Runtime acceptance

- `config init` creates a conservative configuration.
- `config validate` succeeds for the generated configuration.
- `status` operates correctly in a valid Git repository.
- Dry-run behavior performs no mutation.
- Protected-branch, force-with-lease, remote-host, and script/plugin trust policies behave as documented.

## Documentation

- README, architecture, CLI guide, configuration reference, developer guide, security/support policy, release procedure, and changelog agree with runtime behavior.
- Historical Python/tooling references are reconciled.
- Experimental/post-1.0 features are clearly identified.

## Repository state

- Release commit is on `main`.
- CI is green for that exact commit.
- Working tree used to prepare the release is clean.
- No generated runtime artifacts are tracked.
- Version, tag, package metadata, release notes, and changelog all agree.

## Release decision

Any failed mandatory gate blocks `1.0.0`. There is no manual override for coverage, security, package integrity, or version/tag identity failures.
