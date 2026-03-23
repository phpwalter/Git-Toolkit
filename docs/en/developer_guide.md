<!--
 file: developer_guide.md
 path: L:/var/www/Git-Toolkit/docs/en/developer_guide.md
 version: 1.0.0
 date: 2026-03-13
 author: Walter Torres
 copyright: Copyright 2026, Git-Toolkit.
 license: MIT
 maintainer: Git-Toolkit Team
 status: dev

 Comprehensive guide for developers and contributors interested in understanding, developing, and extending the Git Toolkit project.
-->

![toolkit-logo-banner.png](../assets/toolkit-logo-banner.png)
# <img src="../assets/toolkit-icon.png" alt="Description" width="30"/> Developer Guide – Git Toolkit

This guide provides comprehensive information for developers and contributors interested in understanding, developing, and extending the **Git Toolkit** project. Whether you're setting up your development environment, contributing new features, or integrating the toolkit into your workflows, this guide is for you.

---

## 1. 💡 Project Overview

**Git Toolkit** is a lightweight, per-project CLI utility designed to automate and standardize Git workflows across development teams and repositories. It's built with Python using GitPython and configured via YAML.

### Core Philosophy
*   **Per-Project Automation**: Integrated as a Git submodule, allowing each project to define its own `.git-toolkit.yml` configuration.
*   **Standardization**: Promotes consistent Git practices across teams and repositories.
*   **Extensibility**: Supports custom commands, lifecycle hooks, and Python plugins for tailored workflows.
*   **CI/CD Ready**: Designed for seamless integration into automated pipelines.

---

## 2. 🚀 Getting Started: Development Setup

To contribute to Git Toolkit itself, or to understand its internal workings, follow these steps to set up your development environment.

### Prerequisites
*   **Git**: Version control system.
*   **Python 3.7+**: The language Git Toolkit is built with.
*   **pip**: Python package installer (usually comes with Python).

### Cloning the Repository
First, clone the Git Toolkit source repository:
```bash
git clone https://github.com/phpwalter/Git-Toolkit.git
cd Git-Toolkit
```

### Installing Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### Running Tests
Ensure your setup is correct and all existing tests pass:
```bash
pytest
```

### Linting and Formatting
We use `black` for code formatting and `flake8` for linting. It's good practice to run these before committing:
```bash
black .
flake8 .
```

---

## 3. 🧠 Core Concepts

Understanding these core concepts is crucial for developing with and for Git Toolkit.

### 3.1. The `.git-toolkit.yml` Configuration
This YAML file, located in your project's root, defines how Git Toolkit behaves for that specific project. It's the heart of per-project customization.

**Key Sections:**
*   `repositories`: Defines the Git repositories the toolkit manages (e.g., monorepo components).
*   `commands`: Custom Git commands and workflows with defined steps.
*   `safety`: Rules like preventing force pushes or protecting branches.

**Example:**
```yaml
# .git-toolkit.yml
repositories:
  - name: main
    path: .
  - name: ui
    path: ./packages/ui

commands:
  release:
    steps:
      - tag: v{{ version }}
      - push-tags: true

safety:
  prevent_force_push: true
  protect_branches:
    - main
    - release/*
```

### 3.2. Custom Commands
You can define custom commands in `.git-toolkit.yml` that orchestrate multiple Git operations or scripts. These simplify complex workflows into single, memorable commands.

### 3.3. Hooks System
Git Toolkit provides a powerful hook system to execute custom logic `pre_` or `post_` standard Git operations. This allows for advanced automation and policy enforcement.

**Supported Hook Events:**
*   `pre_clone`, `post_clone`
*   `pre_checkout`, `post_checkout`
*   `pre_commit`, `post_commit`
*   `pre_push`, `post_push`
*   ...and more.

Hooks can be defined in your `.git-toolkit.yml` or implemented as Python plugins.

### 3.4. Plugin System
For more complex or reusable logic, Git Toolkit supports Python plugins. These are Python modules that can extend the toolkit's functionality, register new commands, or implement sophisticated hooks.

### 3.5. Multi-Repository Support
Git Toolkit is designed to manage actions across multiple Git repositories, making it ideal for monorepos, microservices architectures, or projects heavily relying on Git submodules. Repositories are defined in the `repositories` section of `.git-toolkit.yml`.

---

## 4. 🤝 Contribution Workflow

We welcome contributions! Please refer to the [CONTRIBUTING.md](../../.github/CONTRIBUTING.md) guide for detailed steps on how to submit bug fixes, features, or documentation improvements.

**Key aspects to remember:**
*   Follow our [Branch Naming Guidelines](../branch-naming-guidelines.md).
*   Adhere to the [Code of Conduct](../../.github/CODE_OF_CONDUCT.md).

---

## 5. 🧪 Testing

Git Toolkit emphasizes robust testing to ensure reliability and correctness.

### Running Tests
As mentioned in the setup, `pytest` is used for running tests:
```bash
pytest
```

### Writing Tests
*   Tests are located in the `git_toolkit/tests/` directory.
*   Aim for high test coverage, especially for new features and bug fixes.
*   Write clear, isolated tests that cover expected behavior and edge cases.

---

## 6. 🎨 Code Style and Quality

Maintaining a consistent code style and high quality is important for project maintainability.

*   **Python Style**: We adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines.
*   **Tools**: `black` is used for automated formatting, and `flake8` for linting. These are integrated into our CI/CD pipeline.

---

## 7. 📚 Documentation

Clear and up-to-date documentation is vital.

### Contributing to Documentation
*   Documentation files are primarily in Markdown (`.md`) format within the `docs/` directory.
*   If you add a new document, ensure it's linked in the [Documentation Summary (SUMMARY.md)](./SUMMARY.md).
*   Keep your language clear, concise, and technically accurate.

### Internationalization (i18n)
Git Toolkit supports multilingual documentation. If you're interested in contributing translations or understanding the process, please refer to the [Internationalization Tools (i18n) Guide](../tools/i18n/README.md).

---

## 8. 🔐 Security Considerations

Security is a top priority. When developing, always consider potential security implications of your changes.

*   **Secure Coding Practices**: Follow best practices to prevent vulnerabilities like injection flaws or insecure defaults.
*   **Reporting Vulnerabilities**: If you discover a security issue, please report it privately as outlined in our [SECURITY.md](../../.github/SECURITY.md) policy.

---

## 9. 🐛 Troubleshooting and Debugging

If you encounter issues while developing or using Git Toolkit:

*   **Check Logs**: The toolkit may provide verbose output or logs that can help diagnose problems.
*   **Review Configuration**: Double-check your `.git-toolkit.yml` for syntax errors or incorrect paths.
*   **Consult Documentation**: The [FAQ.md](../../FAQ.md) and other guides might have answers.
*   **Seek Support**: If you can't resolve the issue, refer to our [SUPPORT.md](../../.github/SUPPORT.md) for how to get help.

---

## 10. 🔗 Related Documents

*   [README.md](../../README.md) – Project overview.
*   [PROPOSAL.md](../../PROPOSAL.md) – Project vision and initial scope.
*   [CONTRIBUTING.md](../../.github/CONTRIBUTING.md) – Guidelines for contributing.
*   [INTEGRATION.md](../../INTEGRATION.md) – How to integrate Git Toolkit.
*   [MAINTAINERS.md](../../.github/MAINTAINERS.md) – Project maintainers and governance.
*   [MILESTONES.md](../../MILESTONES.md) – Key project objectives and timelines.
*   [RELEASE.md](../../RELEASE.md) – Release process and versioning strategy.
*   [ROADMAP.md](../../ROADMAP.md) – High-level plan for project evolution.
*   [SECURITY.md](../../.github/SECURITY.md) – Vulnerability disclosure policy.
*   [SUPPORT.md](../../.github/SUPPORT.md) – How to get help.
*   [TRANSLATIONS.md](../../TRANSLATIONS.md) – Overview of translation efforts.
*   [FAQ.md](../../FAQ.md) – Frequently asked questions.
*   [Branch Naming Guidelines](../branch-naming-guidelines.md) – Policy for branch names.
*   [Internationalization Tools (i18n) Guide](../tools/i18n/README.md) – Details on translation process.

---

_Last updated: 2025-07-16_<br>
_Next review: 2026-07-01_
