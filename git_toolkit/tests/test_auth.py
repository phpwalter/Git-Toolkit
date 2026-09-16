from git_toolkit.auth import get_auth_url, get_pat_from_env


def test_get_auth_url_never_embeds_pat() -> None:
    url = "https://github.com/user/repo.git"
    assert get_auth_url(url, None) == url
    assert get_auth_url(url, "secret-token") == url


def test_get_auth_url_preserves_ssh() -> None:
    url = "git@github.com:user/repo.git"
    assert get_auth_url(url, "secret-token") == url


def test_get_pat_from_env(monkeypatch) -> None:
    monkeypatch.setenv("GIT_TOOLKIT_PAT", "test-token")
    assert get_pat_from_env() == "test-token"


def test_get_pat_from_env_missing(monkeypatch) -> None:
    monkeypatch.delenv("GIT_TOOLKIT_PAT", raising=False)
    assert get_pat_from_env() is None
