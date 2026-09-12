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


def default_global_config_path() -> Path:
    return Path.home() / ".git-toolkit" / "config.yml"


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


def _lookup_dotted(data: dict[str, Any], dotted_key: str) -> tuple[bool, Any]:
    current: Any = data
    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            return False, None
        current = current[part]
    return True, current


def load_config(file_path: Path, global_path: Path | None = None) -> Config:
    """Load effective configuration using global then project precedence."""
    global_path = global_path or default_global_config_path()
    try:
        global_data = _normalize(_read_yaml(global_path))
        project_data = _normalize(_read_yaml(file_path))
        effective = _deep_merge(global_data, project_data)
        return Config(**effective)
    except Exception as exc:
        raise ValueError(f"Configuration error in {file_path}: {exc}") from exc


def explain_config_value(
    file_path: Path,
    dotted_key: str,
    global_path: Path | None = None,
) -> tuple[Any, str]:
    """Return an effective configuration value and the layer that supplied it."""
    global_path = global_path or default_global_config_path()
    global_data = _normalize(_read_yaml(global_path))
    project_data = _normalize(_read_yaml(file_path))

    project_found, _ = _lookup_dotted(project_data, dotted_key)
    global_found, _ = _lookup_dotted(global_data, dotted_key)

    config = load_config(file_path, global_path)
    effective = config.model_dump(by_alias=False, exclude={"auth": {"tokens"}})
    found, value = _lookup_dotted(effective, dotted_key)
    if not found:
        raise KeyError(f"Unknown configuration key: {dotted_key}")

    if project_found:
        source = str(file_path)
    elif global_found:
        source = str(global_path)
    else:
        source = "built-in default"
    return value, source


def initialize_project_config(file_path: Path, *, force: bool = False) -> Path:
    """Create a conservative project configuration without executable project code."""
    if file_path.exists() and not force:
        raise FileExistsError(f"Configuration already exists: {file_path}")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    template = {
        "project": {"name": file_path.parent.name or "project"},
        "repositories": [{"name": "main", "path": ".", "default_branch": "main"}],
        "safety": {
            "prevent_force_push": True,
            "protect_branches": ["main", "master"],
            "require_clean_worktree": True,
        },
        "security": {
            "allow_project_scripts": False,
            "allow_local_plugins": False,
        },
    }
    file_path.write_text(yaml.safe_dump(template, sort_keys=False), encoding="utf-8")
    return file_path
