from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse

_BRANCH_RE = re.compile(r"^(?!/)(?!.*(?:\.\.|//|@\{|\\))(?!.*[/.]$)[A-Za-z0-9._/-]+$")
_TAG_RE = re.compile(r"^(?!/)(?!.*(?:\.\.|//|@\{|\\))(?!.*[/.]$)[A-Za-z0-9._/-]+$")
_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def validate_branch_name(value: str) -> str:
    value = value.strip()
    if not value or value in {"HEAD", "@"} or not _BRANCH_RE.fullmatch(value):
        raise ValueError(f"Invalid branch name: {value!r}")
    if any(part.startswith(".") for part in value.split("/")):
        raise ValueError(f"Invalid branch name: {value!r}")
    return value


def validate_tag_name(value: str) -> str:
    value = value.strip()
    if not value or value in {"HEAD", "@"} or not _TAG_RE.fullmatch(value):
        raise ValueError(f"Invalid tag name: {value!r}")
    return value


def validate_identifier(value: str, *, kind: str = "name") -> str:
    value = value.strip()
    if not _NAME_RE.fullmatch(value):
        raise ValueError(f"Invalid {kind}: {value!r}")
    return value


def validate_workers(value: int) -> int:
    if value < 1 or value > 64:
        raise ValueError("workers must be between 1 and 64")
    return value


def validate_timeout(value: int | None) -> int | None:
    if value is not None and (value < 1 or value > 86400):
        raise ValueError("timeout must be between 1 and 86400 seconds")
    return value


def validate_repo_path(value: str) -> str:
    if not value.strip():
        raise ValueError("repository path must not be empty")
    Path(value)
    return value


def validate_remote_url(value: str) -> str:
    value = value.strip()
    if value.startswith("git@") and ":" in value:
        return value
    parsed = urlparse(value)
    if parsed.scheme not in {"https", "ssh", "git", "file"}:
        raise ValueError(f"Unsupported remote URL scheme: {parsed.scheme or 'missing'}")
    if parsed.scheme != "file" and not parsed.hostname:
        raise ValueError("remote URL must include a host")
    return value
