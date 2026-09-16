from unittest.mock import patch

from git_toolkit.auth import delete_token, get_auth_url, get_credential, get_token, set_token


def test_compat_auth_url_does_not_embed_credentials() -> None:
    url = "https://github.com/user/repo.git"
    assert get_auth_url(url, pat="secret") == url
    assert get_auth_url(url, config_tokens={"github.com": "secret"}) == url


@patch("keyring.set_password")
def test_set_token(mock_set) -> None:
    set_token("host.com", "secret")
    mock_set.assert_called_with("git-toolkit", "host.com", "secret")


@patch("keyring.get_password")
def test_get_token(mock_get) -> None:
    mock_get.return_value = "secret"
    assert get_token("host.com") == "secret"
    mock_get.assert_called_with("git-toolkit", "host.com")


@patch("keyring.delete_password")
def test_delete_token(mock_delete) -> None:
    delete_token("host.com")
    mock_delete.assert_called_with("git-toolkit", "host.com")


@patch("git_toolkit.auth.get_pat_from_env")
@patch("git_toolkit.auth.get_token")
def test_keyring_precedes_environment(mock_get_token, mock_get_env) -> None:
    mock_get_token.return_value = "keyring-secret"
    mock_get_env.return_value = "env-secret"
    assert get_credential("host.com") == "keyring-secret"


@patch("git_toolkit.auth.get_pat_from_env")
@patch("git_toolkit.auth.get_token")
def test_environment_is_fallback(mock_get_token, mock_get_env) -> None:
    mock_get_token.return_value = None
    mock_get_env.return_value = "env-secret"
    assert get_credential("host.com") == "env-secret"
