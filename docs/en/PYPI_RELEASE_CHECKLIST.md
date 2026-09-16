# PyPI Distribution Readiness

A release candidate is publishable only when all checks below pass from a clean checkout.

## Package metadata

- `pyproject.toml` is authoritative for name, version, Python requirement, dependencies, entry points, and optional extras.
- Package version matches `git_toolkit.version.__version__`.
- README and license metadata are present in the distribution.
- Runtime dependencies exclude development-only tooling.

## Build

```bash
python -m pip install --upgrade build twine
python -m build
python -m twine check dist/*
```

Both `.tar.gz` and `.whl` artifacts must be produced.

## Clean install

Create a fresh virtual environment and install the wheel directly:

```bash
python -m venv .release-venv
python -m pip install dist/*.whl
git-toolkit --version
git-toolkit --help
```

The package must not depend on the repository working directory or editable-install behavior.

## Publish policy

Production publication occurs only from an approved release workflow tied to a green `main` commit and immutable version tag. Manual workstation publication is not the normal release path.

## Failure policy

Any metadata error, dependency-audit failure, package-content defect, CLI entry-point failure, or clean-install failure blocks publication.
