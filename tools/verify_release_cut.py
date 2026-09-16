from __future__ import annotations

import re
import subprocess
import tomllib
from pathlib import Path


TARGET_VERSION = "1.0.0"
TARGET_TAG = "v1.0.0"


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        check=True,
        capture_output=True,
        text=True,
        shell=False,
    )
    return result.stdout.strip()


def _runtime_version(path: Path) -> str:
    match = re.search(
        r'^__version__\s*=\s*["\']([^"\']+)["\']\s*$',
        path.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    if match is None:
        raise ValueError("runtime version not found")
    return match.group(1)


def verify(root: Path = Path(".")) -> list[str]:
    failures: list[str] = []

    branch = _git("branch", "--show-current")
    if branch != "main":
        failures.append(f"release cut must run on main, found {branch or 'detached HEAD'}")

    if _git("status", "--porcelain"):
        failures.append("working tree is not clean")

    with (root / "pyproject.toml").open("rb") as handle:
        package_version = tomllib.load(handle).get("project", {}).get("version")
    runtime_version = _runtime_version(root / "git_toolkit/version.py")
    if package_version != TARGET_VERSION:
        failures.append(f"pyproject version must be {TARGET_VERSION}, found {package_version!r}")
    if runtime_version != TARGET_VERSION:
        failures.append(f"runtime version must be {TARGET_VERSION}, found {runtime_version!r}")

    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    if not re.search(r"^##\s+1\.0\.0\s+-\s+\d{4}-\d{2}-\d{2}\s*$", changelog, re.MULTILINE):
        failures.append("CHANGELOG.md is missing a dated 1.0.0 release heading")

    tags = set(_git("tag", "--list", TARGET_TAG).splitlines())
    if TARGET_TAG in tags:
        failures.append(f"release tag already exists: {TARGET_TAG}")

    return failures


def main() -> None:
    failures = verify()
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print("1.0 release-cut preflight OK")


if __name__ == "__main__":
    main()
