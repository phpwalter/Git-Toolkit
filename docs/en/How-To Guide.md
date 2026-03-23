![toolkit-logo-banner.png](../../docs/assets/toolkit-logo-banner.png)
# <img src="../../docs/assets/toolkit-icon.png" alt="Description" width="30"/> How-To Guide – Git Toolkit

This guide provides practical, step-by-step instructions for common tasks when using, configuring, and contributing to the **Git Toolkit** project.

---

## 1. 🚀 How to Get Started with Git Toolkit

### 1.1. How to Install Git Toolkit in Your Project

Git Toolkit is designed to be added as a Git submodule to your project.

1.  **Navigate to your project's root directory**:
    ```bash
    cd /path/to/your-project
    ```
2.  **Add Git Toolkit as a submodule**:
    ```bash
    git submodule add https://github.com/phpwalter/git-toolkit.git .git-toolkit
    ```
3.  **Copy the example configuration file**:
    ```bash
    cp .git-toolkit/.git-toolkit.example.yml .git-toolkit.yml
    ```
4.  **Install Python dependencies**:
    ```bash
    pip install -r .git-toolkit/requirements.txt
    ```
    *(Note: It's recommended to do this within a Python virtual environment.)*

### 1.2. How to Run Git Toolkit Commands

Once installed, you can run Git Toolkit commands from your project root.

1.  **Run a command directly**:
    ```bash
    ./.git-toolkit/git-toolkit <command> [args]
    ```
    *Example: Check the status of your repositories:*
    ```bash
    ./.git-toolkit/git-toolkit status
    ```
2.  **Create a symlink for easier access (optional but recommended)**:
    ```bash
    ln -s .git-toolkit/git-toolkit git-toolkit
    ./git-toolkit status
    ```

---

## 2. ⚙️ How to Configure Git Toolkit

### 2.1. How to Define Repositories in `.git-toolkit.yml`

The `.git-toolkit.yml` file allows you to define multiple repositories that Git Toolkit should manage, useful for monorepos or projects with submodules.

1.  **Open your `.git-toolkit.yml` file**.
2.  **Add a `repositories` section** (if it doesn't exist) and define your repositories:
    ```yaml
    # .git-toolkit.yml
    repositories:
      - name: main_app
        path: . # Refers to the project root
        default_branch: main
      - name: shared_ui_lib
        path: ./packages/ui-library
        default_branch: develop
      - name: backend_service
        path: ./services/api
    ```
    *   `name`: A unique identifier for the repository.
    *   `path`: The relative path from your project root to the repository.
    *   `default_branch`: (Optional) The default branch for this repository.

### 2.2. How to Create a Custom Command

Custom commands allow you to define high-level workflows that execute multiple Git operations or scripts.

1.  **Open your `.git-toolkit.yml` file**.
2.  **Add a `commands` section** and define your custom command:
    ```yaml
    # .git-toolkit.yml
    commands:
      # ... other commands
      release:
        description: "Tags a new version and pushes tags to origin."
        steps:
          - tag: v{{ version }} # Example: uses a templating variable for version
          - push-tags: true

      update-all-submodules:
        description: "Updates all submodules recursively."
        script: |
          git submodule update --init --recursive
          echo "All submodules updated!"
    ```
3.  **Run your custom command**:
    ```bash
    ./git-toolkit release
    ./git-toolkit update-all-submodules
    ```

### 2.3. How to Create a Simple Hook

Hooks allow you to execute scripts or logic before or after specific Git operations.

1.  **Open your `.git-toolkit.yml` file**.
2.  **Add a `hooks` section** and define your hook for a specific event:
    ```yaml
    # .git-toolkit.yml
    hooks:
      pre_push:
        description: "Ensures no direct pushes to main branch."
        script: |
          current_branch=$(git rev-parse --abbrev-ref HEAD)
          if [ "$current_branch" = "main" ]; then
            echo "ERROR: Direct pushes to 'main' branch are not allowed. Please use a PR."
            exit 1
          fi
          echo "Pre-push check passed."
    ```
3.  This `pre_push` hook will now automatically run every time you attempt a `git push`. If you try to push directly to `main`, it will prevent the push.

---

## 3. 🤝 How to Contribute to Git Toolkit

We welcome contributions!

1.  **Read the Contribution Guidelines**: Start by reviewing the [CONTRIBUTING.md](../../.github/CONTRIBUTING.md) document for a detailed workflow.
2.  **Set up your development environment**: Follow the instructions in the [Developer Guide](Developer%20Guide.md).
3.  **Find a task**: Look for open issues labeled `good first issue` or `help wanted` on our [GitHub Issues page](https://github.com/phpwalter/Git-Toolkit/issues).
4.  **Follow our standards**: Adhere to the [Branch Naming Guidelines](../branch-naming-guidelines.md) and [Code of Conduct](../../.github/CODE_OF_CONDUCT.md).

---

## 4. 🐛 How to Report Issues

### 4.1. How to Report a Bug

If you find a bug or unexpected behavior:

1.  **Check existing issues**: Search our [GitHub Issues](https://github.com/phpwalter/Git-Toolkit/issues) to see if the bug has already been reported.
2.  **Open a new bug report**: If not, use the bug report template on GitHub:
    👉 [Open a Bug Report](https://github.com/phpwalter/Git-Toolkit/issues/new?assignees=&labels=bug&projects=&template=bug_report.md&title=%5BBug%5D+)
3.  **Provide details**: Include the Git Toolkit version, Python version, OS, steps to reproduce, and expected vs. actual behavior.

### 4.2. How to Request a Feature

If you have an idea for a new feature or enhancement:

1.  **Check existing requests**: Search our [GitHub Issues](https://github.com/phpwalter/Git-Toolkit/issues) for similar requests.
2.  **Open a new feature request**: If not, use the feature request template on GitHub:
    👉 [Submit a Feature Request](https://github.com/phpwalter/Git-Toolkit/issues/new?assignees=&labels=enhancement&projects=&template=feature_request.md&title=%5BFeature%5D+)
3.  **Explain your use case**: Clearly describe the problem you're trying to solve and how the new feature would help.

---

## 5. ❓ Where to Find More Information

*   **[FAQ](../../FAQ.md)**: For frequently asked questions.
*   **[Developer Guide](Developer%20Guide.md)**: For in-depth development setup and concepts.
*   **[Documentation Summary](SUMMARY.md)**: For a complete index of all project documentation.
*   **[Support Policy](../../SUPPORT.md)**: For general support inquiries.

---

_Last updated: 2025-07-17_<br>
_Next review: 2026-07-01_
