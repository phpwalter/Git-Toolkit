from pathlib import Path

import pytest
import yaml

from git_toolkit.config import (
    Config,
    explain_config_value,
    initialize_project_config,
    load_config,
)


def test_load_config_real(tmp_path: Path) -> None:
    config_file = tmp_path / ".git-toolkit.yml"
    global_file = tmp_path / "global.yml"
    config_file.write_text(
        """
project:
  name: test-project
repositories:
  - name: repo1
    path: ./repo1
    url: https://github.com/user/repo1.git
hooks:
  pre_status:
    script: echo "hello"
""",
        encoding="utf-8",
    )
    config = load_config(config_file, global_file)
    assert config.name == "test-project"
    assert len(config.repositories) == 1
    assert config.repositories[0].name == "repo1"
    assert "pre_status" in config.hooks
    assert config.hooks["pre_status"].script == 'echo "hello"'


def test_load_config_empty(tmp_path: Path) -> None:
    config_file = tmp_path / "empty.yml"
    global_file = tmp_path / "global.yml"
    config_file.touch()
    config = load_config(config_file, global_file)
    assert isinstance(config, Config)
    assert not config.repositories


def test_load_config_not_exists(tmp_path: Path) -> None:
    config = load_config(tmp_path / "missing.yml", tmp_path / "global.yml")
    assert isinstance(config, Config)
    assert not config.repositories


def test_project_configuration_overrides_global_configuration(tmp_path: Path) -> None:
    global_file = tmp_path / "global.yml"
    project_file = tmp_path / "project.yml"
    global_file.write_text(
        "safety:\n  prevent_force_push: false\nhealth:\n  stale_branch_days: 45\n",
        encoding="utf-8",
    )
    project_file.write_text(
        "safety:\n  prevent_force_push: true\n",
        encoding="utf-8",
    )

    config = load_config(project_file, global_file)

    assert config.safety.prevent_force_push is True
    assert config.health.stale_branch_days == 45


def test_explain_config_value_reports_project_global_and_default_sources(tmp_path: Path) -> None:
    global_file = tmp_path / "global.yml"
    project_file = tmp_path / "project.yml"
    global_file.write_text("health:\n  stale_branch_days: 60\n", encoding="utf-8")
    project_file.write_text("safety:\n  prevent_force_push: false\n", encoding="utf-8")

    value, source = explain_config_value(project_file, "safety.prevent_force_push", global_file)
    assert value is False
    assert source == str(project_file)

    value, source = explain_config_value(project_file, "health.stale_branch_days", global_file)
    assert value == 60
    assert source == str(global_file)

    value, source = explain_config_value(project_file, "security.allow_project_scripts", global_file)
    assert value is False
    assert source == "built-in default"


def test_explain_config_value_rejects_unknown_key(tmp_path: Path) -> None:
    with pytest.raises(KeyError, match="Unknown configuration key"):
        explain_config_value(
            tmp_path / "project.yml",
            "missing.value",
            tmp_path / "global.yml",
        )


def test_initialize_project_config_uses_conservative_defaults(tmp_path: Path) -> None:
    config_file = tmp_path / ".git-toolkit.yml"

    initialize_project_config(config_file)

    data = yaml.safe_load(config_file.read_text(encoding="utf-8"))
    assert data["repositories"] == [
        {"name": "main", "path": ".", "default_branch": "main"}
    ]
    assert data["safety"]["prevent_force_push"] is True
    assert data["security"]["allow_project_scripts"] is False
    assert data["security"]["allow_local_plugins"] is False


def test_initialize_project_config_refuses_overwrite_without_force(tmp_path: Path) -> None:
    config_file = tmp_path / ".git-toolkit.yml"
    config_file.write_text("project: {name: existing}\n", encoding="utf-8")

    with pytest.raises(FileExistsError):
        initialize_project_config(config_file)

    initialize_project_config(config_file, force=True)
    assert "prevent_force_push: true" in config_file.read_text(encoding="utf-8")
