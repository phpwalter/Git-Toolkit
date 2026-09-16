from __future__ import annotations

import argparse
import re
import tomllib
from pathlib import Path


_VERSION_RE = re.compile(r'^__version__\s*=\s*["\'](?P<version>[^"\']+)["\']\s*$', re.MULTILINE)
_TAG_RE = re.compile(r'^v(?P<version>\d+\.\d+\.\d+(?:[A-Za-z0-9.+-]*)?)$')


def runtime_version(path: Path) -> str:
    match = _VERSION_RE.search(path.read_text(encoding="utf-8"))
    if match is None:
        raise ValueError(f"Could not find __version__ in {path}")
    return match.group("version")


def package_version(path: Path) -> str:
    with path.open("rb") as handle:
        data = tomllib.load(handle)
    version = data.get("project", {}).get("version")
    if not isinstance(version, str) or not version:
        raise ValueError(f"Missing [project].version in {path}")
    return version


def tag_version(tag: str) -> str:
    match = _TAG_RE.fullmatch(tag)
    if match is None:
        raise ValueError(f"Release tag must use vMAJOR.MINOR.PATCH syntax: {tag}")
    return match.group("version")


def verify(pyproject: Path, version_file: Path, tag: str | None = None) -> str:
    package = package_version(pyproject)
    runtime = runtime_version(version_file)
    if package != runtime:
        raise ValueError(f"Version mismatch: pyproject={package}, runtime={runtime}")
    if tag is not None:
        tagged = tag_version(tag)
        if tagged != package:
            raise ValueError(f"Tag/version mismatch: tag={tagged}, package={package}")
    return package


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify Git Toolkit version consistency.")
    parser.add_argument("--pyproject", type=Path, default=Path("pyproject.toml"))
    parser.add_argument("--version-file", type=Path, default=Path("git_toolkit/version.py"))
    parser.add_argument("--tag", default=None)
    args = parser.parse_args()

    version = verify(args.pyproject, args.version_file, args.tag)
    print(f"version consistency OK: {version}")


if __name__ == "__main__":
    main()
