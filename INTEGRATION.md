<!--
 file: INTEGRATION.md
 path: L:/var/www/Git-Toolkit/INTEGRATION.md
 version: 1.0.0
 date: 2026-03-13
 author: Walter Torres
 copyright: Copyright 2026, Git-Toolkit.
 license: MIT
 maintainer: Git-Toolkit Team
 status: dev

 Guide on how Git Toolkit integrates into various development workflows, CI/CD pipelines, and team environments.
-->

![toolkit-logo-banner.png](../docs/assets/toolkit-logo-banner.png)
# <img src="../docs/assets/toolkit-icon.png" alt="Description" width="30"/> Integration Guide – Git Toolkit

This guide outlines how **Git Toolkit** integrates into various development workflows, CI/CD pipelines, and team environments to automate and standardize Git operations.

---

## 🚀 Core Integration Concept: Per-Project Submodule

Git Toolkit's primary integration model is as a **Git submodule** within each project. This ensures:
*   **Version Control**: The toolkit's version and configuration are tied directly to your project's repository.
*   **Per-Project Customization**: Each project can define its unique Git workflows and automation rules via `.git-toolkit.yml`.
*   **Zero-Touch Setup**: New contributors automatically get the correct toolkit version and configuration when cloning the project.

### Adding Git Toolkit to Your Project

```bash
# From your project root
git submodule add https://github.com/phpwalter/git-toolkit.git .git-toolkit
cp .git-toolkit/.git-toolkit.example.yml .git-toolkit.yml
pip install -r .git-toolkit/requirements.txt
```

---

## 🖥 Local Development Workflow

Git Toolkit streamlines local development by providing a consistent interface for common Git tasks and enforcing project-specific policies.

### ⚙️ Configuration (`.git-toolkit.yml`)

Your project's `.git-toolkit.yml` file is the central hub for defining custom commands, hooks, and safety rules. This allows developers to run project-specific Git workflows with simple, high-level commands.

**Example: Custom Release Command**
```yaml
# .git-toolkit.yml
commands:
  release:
    steps:
      - tag: v{{ version }}
      - push-tags: true
```
Developers can then run:
```bash
./.git-toolkit/git-toolkit release
```

### 🔌 Hooks System

Integrate custom scripts or logic at various points in the Git lifecycle (e.g., `pre_commit`, `post_push`). This is powerful for:
*   **Pre-commit checks**: Enforcing code style, linting, or commit message formats.
*   **Post-merge actions**: Triggering notifications or build processes.

### 🔐 Authentication

Git Toolkit integrates with standard Git authentication mechanisms:
*   **Git Credential Manager (GCM)**: Uses your OS-integrated credential manager by default.
*   **Personal Access Tokens (PATs)**: Can be configured via OS keyring or environment variables for automated environments.

---

## 🤖 CI/CD Pipeline Integration

Git Toolkit is designed to be CI/CD ready, enabling you to enforce Git workflows and automate tasks within your build and deployment pipelines.

### Generic CI/CD Example

```yaml
# .github/workflows/ci.yml (or similar for GitLab CI, Jenkins, etc.)
name: Git Toolkit CI Workflow

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
        with:
          submodules: true # Important: Checkout submodules

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install Git Toolkit dependencies
        run: pip install -r .git-toolkit/requirements.txt

      - name: Run Git Toolkit command (e.g., validate branch name)
        run: ./.git-toolkit/git-toolkit validate-branch-name # Custom command
        # This custom command could be defined in .git-toolkit.yml to check branch naming guidelines

      - name: Run Git Toolkit release command (on specific branches/tags)
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        run: ./.git-toolkit/git-toolkit release --auto-version
        env:
          GIT_TOOLKIT_PAT: ${{ secrets.GITHUB_TOKEN }} # Use GitHub token for auth
```

### Benefits in CI/CD:
*   **Policy Enforcement**: Automatically validate branch names, commit messages, or prevent force pushes.
*   **Automated Releases**: Streamline version tagging, changelog generation, and pushing release artifacts.
*   **Multi-Repo Orchestration**: Coordinate actions across multiple repositories in a monorepo setup.

---

## 🧩 Extensibility & Plugin System

Beyond YAML configuration, Git Toolkit supports deeper integration through its plugin system:
*   **Python Entry Points**: Develop and integrate custom Python modules that extend Git Toolkit's functionality.
*   **Drop-in Scripts**: Easily add custom Bash, Python, or other scripts to be executed as part of your defined commands or hooks.

This allows integration with virtually any external tool or custom logic required by your team.

---

## 🗂 Multi-Repository Management

For projects with multiple Git repositories (e.g., microservices, shared libraries, or submodules), Git Toolkit provides a unified way to manage them. Define all relevant repositories in your `.git-toolkit.yml` and run commands that operate across them.

**Example: Status across multiple repos**
```yaml
# .git-toolkit.yml
repositories:
  - name: frontend
    path: ./frontend-app
  - name: backend
    path: ./backend-service

commands:
  status-all:
    script: |
      for repo in {{ repositories }}; do
        echo "Status for $repo.name:"
        git -C $repo.path status
      done
```

---

## 🔗 Related Policies & References

*   [README.md](../README.md)
*   [PROPOSAL.md](../PROPOSAL.md)
*   [CONTRIBUTING.md](./.github/CONTRIBUTING.md)
*   [SECURITY.md](./.github/SECURITY.md)
*   [GOVERNANCE.md](./.github/GOVERNANCE.md)
*   [Branch Naming Guidelines](../docs/en/branch-naming-guidelines.md)

---

_Last updated: 2025-07-16_<br>
_Next review: 2026-07-01_
