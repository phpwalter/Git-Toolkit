from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class Repository(BaseModel):
    name: str
    path: str
    url: str | None = None
    default_branch: str | None = None
    groups: list[str] = Field(default_factory=list)


class Command(BaseModel):
    description: str | None = None
    script: str | None = None
    steps: list[dict[str, Any]] | None = None


class Hook(BaseModel):
    description: str | None = None
    script: str | None = None


class Safety(BaseModel):
    prevent_force_push: bool = True
    protect_branches: list[str] = Field(default_factory=lambda: ["main", "master"])
    require_clean_worktree: bool = True


class Security(BaseModel):
    allow_project_scripts: bool = False
    allow_local_plugins: bool = False


class Health(BaseModel):
    stale_branch_days: int = 30
    large_file_kb: int = 1000


class Step(BaseModel):
    name: str | None = None
    command: str | None = None
    script: str | None = None
    if_condition: str | None = Field(None, alias="if")
    action: str | None = None
    args: dict[str, Any] = Field(default_factory=dict)
    continue_on_error: bool = False
    timeout: int | None = None
    retries: int = 0

    model_config = {"populate_by_name": True}


class Workflow(BaseModel):
    description: str | None = None
    steps: list[Step] = Field(default_factory=list)
    webhook_url: str | None = None
    failure_policy: str = "stop"


class AuthProvider(BaseModel):
    provider: str = "gcm"
    credential: str | None = None


class AuthConfig(BaseModel):
    providers: dict[str, AuthProvider] = Field(default_factory=dict)
    # Backward-compatible parse only. Runtime code intentionally ignores this field so
    # version-controlled YAML cannot become a credential source.
    tokens: dict[str, str] = Field(default_factory=dict, exclude=True)


class Config(BaseModel):
    name: str | None = Field(None, alias="project_name")
    repositories: list[Repository] = Field(default_factory=list)
    commands: dict[str, Command] = Field(default_factory=dict)
    workflows: dict[str, Workflow] = Field(default_factory=dict)
    hooks: dict[str, Hook] = Field(default_factory=dict)
    safety: Safety = Field(default_factory=Safety)
    security: Security = Field(default_factory=Security)
    health: Health = Field(default_factory=Health)
    auth: AuthConfig = Field(default_factory=AuthConfig)

    model_config = {"populate_by_name": True}


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return {}
    loaded = yaml.safe_load(text)
    if loaded is None:
        return {}
    if not isinstance(loaded, dict):
        raise ValueError(f"Configuration root must be a mapping: {path}")
    return loaded


def _normalize(data: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(data)
    project = result.pop("project", None)
    if isinstance(project, dict) and "name" in project:
        result["project_name"] = project["name"]
    return result


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged


def load_config(file_path: Path, global_path: Path | None = None) -> Config:
    """Load the effective configuration.

    Precedence, lowest to highest:
      1. model defaults
      2. ~/.git-toolkit/config.yml
      3. project configuration supplied by ``file_path``

    Project scripts and project-local plugins are disabled by default because
    both execute code from the checked-out repository. A trusted repository
    must opt in through the ``security`` section.
    """
    global_path = global_path or (Path.home() / ".git-toolkit" / "config.yml")
    try:
        global_data = _normalize(_read_yaml(global_path))
        project_data = _normalize(_read_yaml(file_path))
        effective = _deep_merge(global_data, project_data)
        return Config(**effective)
    except Exception as exc:
        raise ValueError(f"Configuration error in {file_path}: {exc}") from exc
