from __future__ import annotations

import os

import keyring

SERVICE_NAME = "git-toolkit"


def get_pat_from_env() -> str | None:
    """Return the process-scoped fallback PAT, if explicitly supplied."""
    return os.environ.get("GIT_TOOLKIT_PAT")


def set_token(host: str, token: str) -> None:
    """Store a host credential in the operating-system keyring."""
    if not host.strip():
        raise ValueError("host is required")
    if not token:
        raise ValueError("token is required")
    keyring.set_password(SERVICE_NAME, host, token)


def get_token(host: str) -> str | None:
    """Retrieve a host credential from the operating-system keyring."""
    return keyring.get_password(SERVICE_NAME, host)


def delete_token(host: str) -> None:
    """Delete a host credential from the operating-system keyring."""
    try:
        keyring.delete_password(SERVICE_NAME, host)
    except keyring.errors.PasswordDeleteError:
        pass


def get_credential(host: str) -> str | None:
    """Resolve an explicit Git Toolkit credential without exposing it in URLs.

    Keyring takes precedence over the process environment. Git operations do
    not rewrite remotes with this value; transport authentication is delegated
    to Git Credential Manager/credential helpers until provider adapters are
    introduced.
    """
    return get_token(host) or get_pat_from_env()


def get_auth_url(
    url: str,
    pat: str | None = None,
    config_tokens: dict[str, str] | None = None,
) -> str:
    """Compatibility shim that deliberately never injects credentials.

    Older Git Toolkit releases returned URLs containing PATs. That could leak
    secrets through process listings, exception messages, logs, remote config,
    and shell history. Callers may still import this function during migration,
    but the remote URL is now always returned unchanged.
    """
    del pat, config_tokens
    return url
