import pytest
from pathlib import Path
from git_toolkit.config import load_config, Config, Repository, Hook

def test_load_config_real(tmp_path):
    config_file = tmp_path / ".git-toolkit.yml"
    config_file.write_text("""
project:
  name: test-project
repositories:
  - name: repo1
    path: ./repo1
    url: https://github.com/user/repo1.git
hooks:
  pre_status:
    script: echo "hello"
""")
    config = load_config(config_file)
    assert config.name == "test-project"
    assert len(config.repositories) == 1
    assert config.repositories[0].name == "repo1"
    assert "pre_status" in config.hooks
    assert config.hooks["pre_status"].script == 'echo "hello"'

def test_load_config_empty(tmp_path):
    config_file = tmp_path / "empty.yml"
    config_file.touch()
    config = load_config(config_file)
    assert isinstance(config, Config)
    assert not config.repositories

def test_load_config_not_exists():
    config = load_config(Path("non_existent.yml"))
    assert isinstance(config, Config)
    assert not config.repositories
