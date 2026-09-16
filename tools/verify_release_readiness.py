from __future__ import annotations

import re
import subprocess
import tomllib
from pathlib import Path


REQUIRED_FILES = (
    "README.md",
    "docs/en/ARCHITECTURE.md",
    "docs/en/CLI_GUIDE.md",
    "docs/en/DEVELOPER_GUIDE.md",
    "docs/en/RELEASE_READINESS.md",
    "CHANGELOG.md",
    ".github/workflows/ci.yml",
)

FORBIDDEN_TRACKED_SUFFIXES = (".coverage", ".pyc")
FORBIDDEN_TRACKED_PARTS = ("__pycache__", ".egg-info", ".pytest_cache", ".mypy_cache", ".ruff_cache")


def _runtime_version(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r'^__version__\s*=\s*["\']([^"\']+)["\']\s*$', text, re.MULTILINE)
    if match is None:
        raise ValueError("runtime version not found")
    return match.group(1)


def _tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        check=True,
        capture_output=True,
        text=True,
        shell=False,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def verify(root: Path = Path(".")) -> list[str]:
    failures: list[str] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).exists():
            failures.append(f"missing required release file: {relative}")

    with (root / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    package_version = pyproject.get("project", {}).get("version")
    runtime_version = _runtime_version(root / "git_toolkit/version.py")
    if package_version != runtime_version:
        failures.append(
            f"version mismatch: pyproject={package_version}, runtime={runtime_version}"
        )

    coverage = pyproject.get("tool", {}).get("coverage", {}).get("report", {}).get("fail_under")
    if coverage is None or float(coverage) < 80:
        failures.append(f"coverage threshold must be >= 80, found {coverage!r}")

    python_requirement = pyproject.get("project", {}).get("requires-python")
    if python_requirement != ">=3.11":
        failures.append(f"requires-python must be >=3.11, found {python_requirement!r}")

    for tracked in _tracked_files():
        if tracked.endswith(FORBIDDEN_TRACKED_SUFFIXES) or any(
            part in tracked for part in FORBIDDEN_TRACKED_PARTS
        ):
            failures.append(f"forbidden generated artifact is tracked: {tracked}")

    return failures


def main() -> None:
    failures = verify()
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print("release readiness preflight OK")


if __name__ == "__main__":
    main()
