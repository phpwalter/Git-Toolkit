from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse

_BRANCH_RE = re.compile(r"^(?!/)(?!.*(?:\.\.|//|@\{|\\))(?!.*[/.]$)[A-Za-z0-9._/-]+$")
_TAG_RE = re.compile(r"^(?!/)(?!.*(?:\.\.|//|@\{|\\))(?!.*[/.]$)[A-Za-z0-9._/-]+$")
_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_HOST_RE = re.compile(
    r"^(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,62}[A-Za-z0-9])?)"
    r"(?:\.(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,62}[A-Za-z0-9])?))*$"
)


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


def validate_host(value: str) -> str:
    host = value.strip().lower().rstrip(".")
    if not host or len(host) > 253 or not _HOST_RE.fullmatch(host):
        raise ValueError(f"Invalid host: {value!r}")
    return host


def validate_positive_int(value: int, *, field: str = "value", maximum: int | None = None) -> int:
    if value < 1:
        raise ValueError(f"{field} must be a positive integer")
    if maximum is not None and value > maximum:
        raise ValueError(f"{field} must be <= {maximum}")
    return value


def validate_workers(value: int) -> int:
    return validate_positive_int(value, field="workers", maximum=64)


def validate_timeout(value: int | None) -> int | None:
    if value is None:
        return None
    return validate_positive_int(value, field="timeout", maximum=86400)


def validate_repo_path(value: str) -> str:
    if not value.strip():
        raise ValueError("repository path must not be empty")
    Path(value)
    return value


def validate_remote_url(value: str) -> str:
    value = value.strip()
    if value.startswith("git@") and ":" in value:
        host = value.split("@", 1)[1].split(":", 1)[0]
        validate_host(host)
        return value
    parsed = urlparse(value)
    if parsed.scheme not in {"https", "ssh", "git", "file"}:
        raise ValueError(f"Unsupported remote URL scheme: {parsed.scheme or 'missing'}")
    if parsed.scheme != "file":
        if not parsed.hostname:
            raise ValueError("remote URL must include a host")
        validate_host(parsed.hostname)
    return value
