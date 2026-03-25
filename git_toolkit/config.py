from pathlib import Path
from typing import List, Dict, Any, Optional
import yaml
from pydantic import BaseModel, Field, ValidationError

# Pydantic Models for Configuration Structure

class Repository(BaseModel):
    name: str
    path: str
    url: Optional[str] = None
    default_branch: Optional[str] = None
    groups: List[str] = Field(default_factory=list)

class Command(BaseModel):
    description: Optional[str] = None
    script: Optional[str] = None
    steps: Optional[List[Dict[str, Any]]] = None # Flexible for various step types

class Hook(BaseModel):
    description: Optional[str] = None
    script: Optional[str] = None
    # Add more specific hook properties as needed

class Safety(BaseModel):
    prevent_force_push: bool = False
    protect_branches: List[str] = Field(default_factory=list)

class Health(BaseModel):
    stale_branch_days: int = 30
    large_file_kb: int = 1000

class Step(BaseModel):
    name: Optional[str] = None
    command: Optional[str] = None
    script: Optional[str] = None
    if_condition: Optional[str] = Field(None, alias="if")
    # Added for extensibility, e.g., steps from plugins
    action: Optional[str] = None
    args: Dict[str, Any] = Field(default_factory=dict)

    model_config = {
        "populate_by_name": True
    }

class Workflow(BaseModel):
    description: Optional[str] = None
    steps: List[Step] = Field(default_factory=list)
    webhook_url: Optional[str] = None

class AuthConfig(BaseModel):
    tokens: Dict[str, str] = Field(default_factory=dict)

class Config(BaseModel):
    name: Optional[str] = Field(None, alias="project_name")
    repositories: List[Repository] = Field(default_factory=list)
    commands: Dict[str, Command] = Field(default_factory=dict)
    workflows: Dict[str, Workflow] = Field(default_factory=dict)
    hooks: Dict[str, Hook] = Field(default_factory=dict)
    safety: Safety = Field(default_factory=Safety)
    health: Health = Field(default_factory=Health)
    auth: AuthConfig = Field(default_factory=AuthConfig)

    model_config = {
        "populate_by_name": True
    }

def load_config(file_path: Path) -> Config:
    """
    Loads and validates the Git Toolkit configuration from a YAML file.
    """
    if not file_path.exists():
        return Config()

    try:
        content = file_path.read_text()
        if not content.strip():
            return Config()
        
        data = yaml.safe_load(content)
        if data is None:
            return Config()

        # Handle 'project' section if present
        if 'project' in data and isinstance(data['project'], dict):
            project_data = data.pop('project')
            if 'name' in project_data:
                data['project_name'] = project_data['name']

        return Config(**data)
    except Exception as e:
        raise ValueError(f"Configuration error in {file_path}: {e}") from e

# Example usage (for demonstration, not part of the module's core logic)
if __name__ == "__main__":
    # Create a dummy config file for testing
    dummy_config_path = Path("temp_git-toolkit.yml")
    dummy_config_path.write_text("""
repositories:
  - name: main_app
    path: .
    default_branch: main
  - name: shared_ui_lib
    path: ./packages/ui-library

commands:
  status:
    script: "git status"
  release:
    steps:
      - tag: "v1.0.0"
      - push-tags: true

hooks:
  pre_push:
    script: "echo 'Running pre-push hook'"

safety:
  prevent_force_push: true
  protect_branches:
    - main
    - develop
""")

    try:
        config = load_config(dummy_config_path)
        print("Configuration loaded successfully:")
        print(config.json(indent=2))

        # Test non-existent file
        non_existent_path = Path("non_existent.yml")
        empty_config = load_config(non_existent_path)
        print(f"\nLoaded from non-existent file: {empty_config.json(indent=2)}")

        # Test empty file
        empty_file_path = Path("empty_config.yml")
        empty_file_path.touch()
        empty_config_from_file = load_config(empty_file_path)
        print(f"\nLoaded from empty file: {empty_config_from_file.json(indent=2)}")

    except (ValueError, FileNotFoundError) as e:
        print(f"Error loading configuration: {e}")
    finally:
        # Clean up dummy files
        if dummy_config_path.exists():
            dummy_config_path.unlink()
        if empty_file_path.exists():
            empty_file_path.unlink()
