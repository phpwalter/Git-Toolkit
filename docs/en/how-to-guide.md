<!--
 file: how-to-guide.md
 path: L:/var/www/Git-Toolkit/docs/en/how-to-guide.md
 version: 1.0.0
 date: 2026-03-13
 author: Walter Torres
 copyright: Copyright 2026, Git-Toolkit.
 license: MIT
 maintainer: Git-Toolkit Team
 status: dev

 Provides practical, step-by-step instructions for common tasks when using, configuring, and contributing to the Git Toolkit project.
-->

![toolkit-logo-banner.png](../assets/toolkit-logo-banner.png)
# <img src="../assets/toolkit-icon.png" alt="Description" width="30"/> How-To Guide – Git Toolkit

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
    
    **On macOS/Linux:**
    ```bash
    ln -s .git-toolkit/git-toolkit git-toolkit
    ./git-toolkit status
    ```

    **On Windows:**

    Open Command Prompt or PowerShell **as an administrator**.
    ```powershell
    mklink git-toolkit .\.git-toolkit\git-toolkit
    ```
    Then you can run:
    ```
    .\git-toolkit.ps1 status
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
    *   `groups`: (Optional) A list of groups this repository belongs to (e.g., `frontend`, `backend`).

### 2.2. How to Use Repository Grouping

Grouping allows you to run commands on specific sets of repositories.

1.  **Define groups in `.git-toolkit.yml`**:
    ```yaml
    repositories:
      - name: web_app
        path: ./apps/web
        groups: ["frontend"]
      - name: api_service
        path: ./services/api
        groups: ["backend"]
      - name: shared_utils
        path: ./libs/utils
        groups: ["frontend", "backend"]
    ```
2.  **Filter commands by group**:
    Use the `--group` flag with any command to target only the repositories in that group.
    ```bash
    ./git-toolkit status --group frontend
    ./git-toolkit push --group backend
    ```

### 2.3. How to Create a Custom Command

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

### 2.4. How to View Repository Analytics

The `stats` command provides insights into your repositories' activity and health.

1.  **Run the stats command**:
    ```bash
    ./git-toolkit stats
    ```
    This will display a table with the active branch, total commit count, unique contributor count, and a health summary for each defined repository.

2.  **Export stats to JSON or Markdown**:
    ```bash
    ./git-toolkit stats --format json
    ./git-toolkit stats --format markdown
    ```
    *   **JSON**: Useful for programmatic analysis or integration with custom reporting tools.
    *   **Markdown**: Generates a detailed report including warnings for stale branches and large files.

### 2.5. How to Configure Health Metrics

You can customize the thresholds for repository health checks in your `.git-toolkit.yml`.

1.  **Open your `.git-toolkit.yml` file**.
2.  **Add a `health` section**:
    ```yaml
    # .git-toolkit.yml
    health:
      stale_branch_days: 30  # Warn if a branch hasn't been updated in 30 days
      large_file_kb: 1000    # Warn if a file exceeds 1000 KB (1 MB)
    ```
    If not specified, these default values will be used.

### 2.6. How to Run Custom Workflows

Workflows allow you to define sequences of commands and scripts that run across all your repositories. They support parallel execution and conditional steps.

1.  **Open your `.git-toolkit.yml` file**.
2.  **Add a `workflows` section**:
    ```yaml
    # .git-toolkit.yml
    workflows:
      sync-all:
        description: "Pull latest changes and update submodules"
        steps:
          - name: "pull"
            script: "git pull origin main"
            if: "branch == main"
          - name: "submodules"
            command: "submodule update"
    ```
3.  **Run the workflow**:
    ```bash
    ./git-toolkit run sync-all
    ```
4.  **Run in parallel**:
    To speed up execution for many repositories, use the `--parallel` flag. You can also specify the number of workers:
    ```bash
    ./git-toolkit run sync-all --parallel --workers 8
    ```

### 2.7. How to Manage the Metadata Cache

Git Toolkit caches repository metadata (like status and statistics) to improve performance, especially when dealing with many repositories.

1.  **View performance improvements**:
    Subsequent runs of `status` or `stats` commands will be significantly faster as they use cached data.
    - `status` cache TTL: 60 seconds
    - `stats` cache TTL: 300 seconds (5 minutes)

2.  **Clear the cache**:
    If you need to force a refresh of the metadata, use the `clear-cache` command:
    ```bash
    ./git-toolkit clear-cache
    ```

### 2.8. How to Configure Workflow Webhooks

Workflows can send notifications to external services (like Slack or Discord) upon completion.

1.  **Open your `.git-toolkit.yml` file**.
2.  **Add a `webhook_url` to your workflow**:
    ```yaml
    workflows:
      deploy:
        description: "Deploy to production"
        webhook_url: "https://hooks.slack.com/services/..."
        steps:
          - name: "build"
            script: "npm run build"
          - name: "push"
            command: "push"
    ```
3.  When the workflow finishes, Git Toolkit will send a POST request with the execution results to the specified URL.

### 2.9. How to Manage Authentication Tokens

Git Toolkit supports secure storage of Personal Access Tokens (PATs) for different Git hosts using the system keyring.

1.  **Store a token for a host**:
    ```bash
    ./git-toolkit auth set github.com --token your_personal_access_token
    ```
    This will securely store the token in your system's keyring (e.g., Windows Credential Manager, macOS Keychain).

2.  **Verify a stored token (masked)**:
    ```bash
    ./git-toolkit auth get github.com
    ```

3.  **Delete a stored token**:
    ```bash
    ./git-toolkit auth delete github.com
    ```

4.  **Use host-specific tokens in configuration**:
    You can also define tokens directly in `.git-toolkit.yml` (though using the `auth` command is more secure):
    ```yaml
    # .git-toolkit.yml
    auth:
      tokens:
        github.com: "your_token_here"
        gitlab.com: "another_token_here"
    ```

Git Toolkit will look for tokens in the following order:
1.  Host-specific token in `.git-toolkit.yml`.
2.  Host-specific token in the system keyring.
3.  `GIT_TOOLKIT_PAT` environment variable.

### 2.10. How to Use Observability Features

Git Toolkit provides structured logging and execution history to help you debug and audit your workflows.

1.  **Enable Verbose Logging**:
    Use the `--verbose` flag with any command to see detailed debug logs in the console.
    ```bash
    ./git-toolkit status --verbose
    ```

2.  **View Execution History**:
    The `history` command shows a list of recent Git Toolkit operations.
    ```bash
    ./git-toolkit history
    ```
    You can limit the number of entries shown using the `--limit` flag:
    ```bash
    ./git-toolkit history --limit 5
    ```

3.  **Inspect Log Files**:
    Git Toolkit automatically saves detailed logs to the `.git-toolkit/logs/` directory. Each day has its own log file (e.g., `2026-03-25.log`).

4.  **Audit Execution Data**:
    A machine-readable execution history is maintained in `.git-toolkit/history.json`. This file contains timestamps, commands, arguments (with tokens masked), and success/failure status for the last 100 operations.

---

## 3. 🤝 How to Contribute to Git Toolkit

We welcome contributions!

1.  **Read the Contribution Guidelines**: Start by reviewing the [CONTRIBUTING.md](../../.github/CONTRIBUTING.md) document for a detailed workflow.
2.  **Set up your development environment**: Follow the instructions in the [Developer Guide](developer_guide.md).
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
*   **[Developer Guide](developer_guide.md)**: For in-depth development setup and concepts.
*   **[Documentation Summary](SUMMARY.md)**: For a complete index of all project documentation.
*   **[Support Policy](../../.github/SUPPORT.md)**: For general support inquiries.

---

_Last updated: 2026-03-25_<br>
_Next review: 2026-07-01_
