import os
import sys
from typing import Optional, Dict
from urllib.parse import urlparse
import keyring

# Configuration for keyring
SERVICE_NAME = "git-toolkit"

def get_auth_url(url: str, pat: Optional[str] = None, config_tokens: Optional[Dict[str, str]] = None) -> str:
    """
    Constructs an authenticated URL.
    Order of precedence for PAT:
    1. Provided `pat` argument.
    2. Host-specific token from `config_tokens`.
    3. Host-specific token from system keyring.
    4. GIT_TOOLKIT_PAT environment variable.
    """
    if not url.startswith("https://"):
        return url

    parsed_url = urlparse(url)
    host = parsed_url.netloc

    # 1. Provided pat
    token = pat

    # 2. Host-specific token from config
    if not token and config_tokens:
        token = config_tokens.get(host)

    # 3. Host-specific token from keyring
    if not token:
        token = get_token(host)

    # 4. Fallback to environment variable
    if not token:
        token = get_pat_from_env()

    if not token:
        return url

    # Reconstruct URL with token
    # https://github.com/user/repo.git -> https://<token>@github.com/user/repo.git
    return f"https://{token}@{host}{parsed_url.path}{'?' + parsed_url.query if parsed_url.query else ''}"

def get_pat_from_env() -> Optional[str]:
    """
    Retrieves the Personal Access Token from environment variables.
    Checks for GIT_TOOLKIT_PAT.
    """
    return os.environ.get("GIT_TOOLKIT_PAT")

def set_token(host: str, token: str):
    """
    Stores a token in the system keyring for a specific host.
    """
    keyring.set_password(SERVICE_NAME, host, token)

def get_token(host: str) -> Optional[str]:
    """
    Retrieves a token from the system keyring for a specific host.
    """
    return keyring.get_password(SERVICE_NAME, host)

def delete_token(host: str):
    """
    Deletes a token from the system keyring for a specific host.
    """
    try:
        keyring.delete_password(SERVICE_NAME, host)
    except keyring.errors.PasswordDeleteError:
        pass
