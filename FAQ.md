![toolkit-logo-banner.png](../docs/assets/toolkit-logo-banner.png)
# <img src="../docs/assets/toolkit-icon.png" alt="Description" width="30"/> Frequently Asked Questions – Git Toolkit

This FAQ addresses common questions about the **Git Toolkit** project.

---

## 💡 General Questions

### ❓ What is Git Toolkit?

**Git Toolkit** is a lightweight, per-project CLI utility designed to automate and standardize Git workflows across development teams and repositories. It's added to each repository as a Git submodule, allowing projects to define their own Git commands, automation rules, and multi-repo workflows using a `.git-toolkit.yml` configuration file.

### ❓ How is Git Toolkit different from other Git tools?

Unlike global CLI tools or simple aliases, Git Toolkit is:
*   **Per-project**: Configured via `.git-toolkit.yml` stored in version control, ensuring consistency across a team.
*   **Submodule-based**: Integrated directly into your repository, making it easy to manage and version.
*   **Extensible**: Supports lifecycle hooks, plugins, and script steps for advanced automation.
*   **Python-first**: Built with Python and GitPython, offering a robust and scriptable foundation.

It fills gaps left by tools like `git-extras` (hard to extend), `pre-commit` (focused on linting/testing, not Git workflows), and `GitHub CLI` (GitHub-specific, no local project config).

### ❓ How do I install Git Toolkit in my project?

From your project directory, run:
```bash
git submodule add https://github.com/phpwalter/git-toolkit.git .git-toolkit
cp .git-toolkit/.git-toolkit.example.yml .git-toolkit.yml
pip install -r .git-toolkit/requirements.txt
```

### ❓ How do I run Git Toolkit commands?

You can run commands directly:
```bash
./.git-toolkit/git-toolkit <command>
```
For convenience, you can create a symlink:
```bash
ln -s .git-toolkit/git-toolkit git-toolkit
./git-toolkit status
```

### ❓ What is `.git-toolkit.yml`?

The `.git-toolkit.yml` file is the central configuration file for Git Toolkit within your project. It defines:
*   **Repositories**: Lists the Git repositories managed by the toolkit (e.g., monorepo components, submodules).
*   **Commands**: Custom Git commands and workflows with defined steps.
*   **Safety Rules**: Such as preventing force pushes or protecting specific branches.

### ❓ Does Git Toolkit support multi-repo workflows?

Yes, Git Toolkit is designed with multi-repo support in mind. You can define multiple repositories in your `.git-toolkit.yml` and orchestrate actions across them, making it ideal for monorepos, microservices, or projects using many submodules.

### ❓ What kind of extensibility does Git Toolkit offer?

Git Toolkit is highly extensible through:
*   **Hooks**: Run custom scripts or logic `pre_` or `post_` Git operations (e.g., `pre_push`, `post_commit`).
*   **Plugins**: Drop-in Python modules for advanced, reusable logic.
*   **Script Steps**: Define Bash, Python, or other scripts directly within your YAML-defined workflows.

### ❓ Is Git Toolkit cross-platform?

Yes, Git Toolkit is designed to work on Linux, macOS, and Windows. It's also CI/CD ready, allowing you to enforce Git workflows in automated pipelines.

### ❓ What are the system requirements for Git Toolkit?

*   Python 3.7+
*   [GitPython](https://gitpython.readthedocs.io/en/stable/) (installed via `requirements.txt`)

---

## 🔒 Security & Policies

### ❓ How do I report a security vulnerability?

Please report security vulnerabilities privately and responsibly via GitHub's [Private Vulnerability Reporting](https://github.com/phpwalter/Git-Toolkit/security/advisories) or by emailing the security team. Refer to our [Security Policy](./.github/SECURITY.md) for full details.

### ❓ Where can I find the Code of Conduct?

Our [Code of Conduct](./.github/CODE_OF_CONDUCT.md) outlines the standards of behavior expected from all contributors and participants in the Git Toolkit community.

### ❓ Are there branch naming guidelines for contributions?

Yes, we have [Branch Naming Guidelines](../docs/en/branch-naming-guidelines.md) that all contributors must follow to ensure consistency and support CI/CD automation.

---

## 📚 Further Information

### ❓ Who maintains Git Toolkit?

Git Toolkit is primarily maintained by [@phpwalter](https://github.com/phpwalter). For more details on governance and maintainers, refer to the [GOVERNANCE.md](./.github/GOVERNANCE.md) and [MAINTAINERS.md](./.github/MAINTAINERS.md) files.

---

## 🔗 Related Documents

*   [README.md](../README.md)
*   [PROPOSAL.md](../PROPOSAL.md)
*   [CONTRIBUTING.md](./.github/CONTRIBUTING.md)
*   [CODE_OF_CONDUCT.md](./.github/CODE_OF_CONDUCT.md)
*   [SECURITY.md](./.github/SECURITY.md)
*   [GOVERNANCE.md](./.github/GOVERNANCE.md)
*   [Branch Naming Guidelines](../docs/en/branch-naming-guidelines.md)

---

_Last updated: 2025-07-16_<br>
_Next review: 2026-07-01_
