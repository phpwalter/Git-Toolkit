import pytest
from unittest.mock import patch, MagicMock
from git_toolkit.auth import get_auth_url, set_token, get_token, delete_token

def test_get_auth_url_no_token():
    url = "https://github.com/user/repo.git"
    assert get_auth_url(url) == url

def test_get_auth_url_with_arg_token():
    url = "https://github.com/user/repo.git"
    token = "my-token"
    expected = "https://my-token@github.com/user/repo.git"
    assert get_auth_url(url, pat=token) == expected

def test_get_auth_url_with_config_token():
    url = "https://github.com/user/repo.git"
    config_tokens = {"github.com": "config-token"}
    expected = "https://config-token@github.com/user/repo.git"
    assert get_auth_url(url, config_tokens=config_tokens) == expected

@patch("git_toolkit.auth.get_token")
def test_get_auth_url_with_keyring_token(mock_get_token):
    url = "https://github.com/user/repo.git"
    mock_get_token.return_value = "keyring-token"
    expected = "https://keyring-token@github.com/user/repo.git"
    assert get_auth_url(url) == expected
    mock_get_token.assert_called_with("github.com")

@patch("git_toolkit.auth.get_pat_from_env")
def test_get_auth_url_with_env_token(mock_get_env):
    url = "https://github.com/user/repo.git"
    mock_get_env.return_value = "env-token"
    expected = "https://env-token@github.com/user/repo.git"
    assert get_auth_url(url) == expected

def test_get_auth_url_non_https():
    url = "http://github.com/user/repo.git"
    assert get_auth_url(url, pat="token") == url

@patch("keyring.set_password")
def test_set_token(mock_set):
    set_token("host.com", "secret")
    mock_set.assert_called_with("git-toolkit", "host.com", "secret")

@patch("keyring.get_password")
def test_get_token(mock_get):
    mock_get.return_value = "secret"
    assert get_token("host.com") == "secret"
    mock_get.assert_called_with("git-toolkit", "host.com")

@patch("keyring.delete_password")
def test_delete_token(mock_delete):
    delete_token("host.com")
    mock_delete.assert_called_with("git-toolkit", "host.com")
