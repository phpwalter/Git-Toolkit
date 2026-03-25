import pytest
import os
from git_toolkit.auth import get_auth_url, get_pat_from_env

def test_get_auth_url_no_pat():
    url = "https://github.com/user/repo.git"
    assert get_auth_url(url, None) == url
    assert get_auth_url(url, "") == url

def test_get_auth_url_with_pat():
    url = "https://github.com/user/repo.git"
    pat = "ghp_12345"
    expected = "https://ghp_12345@github.com/user/repo.git"
    assert get_auth_url(url, pat) == expected

def test_get_auth_url_ssh():
    url = "git@github.com:user/repo.git"
    pat = "ghp_12345"
    assert get_auth_url(url, pat) == url

def test_get_pat_from_env(monkeypatch):
    monkeypatch.setenv("GIT_TOOLKIT_PAT", "ghp_test_token")
    assert get_pat_from_env() == "ghp_test_token"

def test_get_pat_from_env_missing(monkeypatch):
    monkeypatch.delenv("GIT_TOOLKIT_PAT", raising=False)
    assert get_pat_from_env() is None
