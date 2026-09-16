from __future__ import annotations

import re
import tarfile
import zipfile
from pathlib import Path

_VERSION_RE = re.compile(r"git_toolkit-(?P<version>[^/\\-]+(?:\.[^/\\-]+)*)")


def _version_from_name(name: str) -> str:
    match = _VERSION_RE.search(name.replace("-py3-none-any.whl", "").replace(".tar.gz", ""))
    if match is None:
        raise ValueError(f"Could not determine package version from {name}")
    return match.group("version")


def verify_dist(dist: Path = Path("dist")) -> str:
    wheels = sorted(dist.glob("*.whl"))
    sdists = sorted(dist.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        raise ValueError("Expected exactly one wheel and one source distribution")

    wheel_version = _version_from_name(wheels[0].name)
    sdist_version = _version_from_name(sdists[0].name)
    if wheel_version != sdist_version:
        raise ValueError(f"Artifact version mismatch: wheel={wheel_version}, sdist={sdist_version}")

    with zipfile.ZipFile(wheels[0]) as archive:
        names = set(archive.namelist())
        if "git_toolkit/__init__.py" not in names:
            raise ValueError("Wheel is missing git_toolkit/__init__.py")
        entry_points = [name for name in names if name.endswith(".dist-info/entry_points.txt")]
        if len(entry_points) != 1:
            raise ValueError("Wheel must contain exactly one entry_points.txt")
        text = archive.read(entry_points[0]).decode("utf-8")
        if "git-toolkit = git_toolkit.cli:main" not in text:
            raise ValueError("Wheel does not expose the git-toolkit CLI entry point")

    with tarfile.open(sdists[0], "r:gz") as archive:
        names = archive.getnames()
        if not any(name.endswith("/pyproject.toml") for name in names):
            raise ValueError("Source distribution is missing pyproject.toml")

    return wheel_version


def main() -> None:
    version = verify_dist()
    print(f"distribution structure OK: {version}")


if __name__ == "__main__":
    main()
