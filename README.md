<!-- Badge Block -->
![CI](https://img.shields.io/github/actions/workflow/status/phpwalter/Git-Toolkit/ci.yml?label=ci&logo=githubactions&logoColor=white)
![Release](https://img.shields.io/github/actions/workflow/status/phpwalter/Git-Toolkit/release.yml?label=release&logo=rocket&logoColor=white)
![Version](https://img.shields.io/github/v/release/phpwalter/Git-Toolkit?label=version&logo=semantic-release&logoColor=white)
![Coverage](https://img.shields.io/codecov/c/github/phpwalter/Git-Toolkit?logo=codecov&logoColor=white)
![Security](https://img.shields.io/badge/security-passing-brightgreen?logo=auth0&logoColor=white)
![License](https://img.shields.io/github/license/phpwalter/Git-Toolkit?logo=opensourceinitiative&logoColor=white)
![Python](https://img.shields.io/pypi/pyversions/git-toolkit?logo=python&logoColor=white)
![Last Commit](https://img.shields.io/github/last-commit/phpwalter/Git-Toolkit?label=%F0%9F%97%93%20Last%20Commit&color=007ec6)
![Maintenance](https://img.shields.io/badge/%F0%9F%9B%A0%EF%B8%8F%20Maintenance-active-brightgreen)


---
![toolkit-logo-banner.png](docs/assets/toolkit-logo-banner.png)


A lightweight, cross-platform Python CLI toolkit to **standardize** and **automate** common Git workflows for development teams.  
Built on **GitPython**, powered by **YAML** config, and extensible via hooks, plugins, and multi-language docs.

Automate your GitHub workflow from day one—hooks, CI/CD, versioning, releases, quality gates—all zero-touch.


> 🔍 See the full project design in [PROPOSAL.md](./PROPOSAL.md)  
> 📚 Learn about the team process in [`WORKFLOW.md`](.github/WORKFLOW.md)

---

## 📑 Table of Contents
- [Quick Start](#-quick-start)
- [Features](#-features)
- [Configuration](#⚙️-Configuration)
- [Hooks & Plugins](#-hooks--plugins)
- [Project Layout](#-project-layout)
- [Documentation](#-documentation)
- [Roadmap & Milestones](#-roadmap--milestones)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Quick Start

```bash
# 1. Install
pip install git-toolkit

# 2. Bootstrap your repo
git clone https://github.com/phpwalter/Git-Toolkit.git
cd your-repo
gt init-hooks

# 3. Work as normal
git add .
git commit -m "feat: your change"
git push
# CI, hooks, versioning & release all run automatically!
```

---

## 📋 Features

✅ Git-native commands: `clone`, `checkout`, `status`, `commit`, `push`, `submodule update`<br>
✅ Cross-platform: Windows / macOS / Linux<br>
✅ Configurable via `.git-toolkit.yaml` or global `~/.git-toolkit/config.yaml`<br>
✅ Auth options:<br>

* Git Credential Manager (default)<br>
* Personal Access Token (PAT) with OS keyring<br>
* (Coming soon) OAuth for GitHub/GitLab/Bitbucket<br>

✅ Hooks system with lifecycle events:<br>
* `pre_clone`, `post_clone`, `pre_push`, `post_push`, etc.<br>

✅ Plugin support via Python entry points<br>
✅ Docs localization (`docs/<lang>/`), CI/CD enforcement, and sync tooling<br>

---

## ⚙️ Configuration

Example `.git-toolkit.yaml`:

```yaml
default_remote: origin
branch_prefix: feature/
auth:
  method: credential_manager
hooks_dir: .git-toolkit/hooks
```

📄 See [config\_default.yaml](./config_default.yaml) for full schema.

---

## 🔌 Hooks & Plugins

Custom hook (e.g. `.git-toolkit/hooks/enforce_prefix.py`):

```python
from git_toolkit.hooks import hook

@hook("pre_push")
def enforce_feature_prefix(ctx):
    last_msg = ctx.repo.git.log("-1", "--pretty=%B")
    if not last_msg.startswith("FEATURE:"):
        raise RuntimeError("Commit message must start with 'FEATURE:'")
```

For plugins: expose via `entry_points` under `git_toolkit.plugins`.

---

## 🧱 Project Layout

```
.
├── README.md
├── PROPOSAL.md
├── config_default.yaml
├── git_toolkit/
│   ├── cli.py, config.py, hooks.py, ...
│   └── tests/
│       └── test_*.py
├── docs/
│   ├── en/, es/, fr/           ← i18n structure
│   └── ...
└── .github/
    ├── CONTRIBUTING.md
    ├── CODE_OF_CONDUCT.md
    ├── GOVERNANCE.md
    ├── SECURITY.md
    ├── SYNC_PROCESS.md
    ├── DOCS_SYNC.md
    ├── WORKFLOW.md             ← CI/CD, branching, review flow
    ├── ISSUE_TEMPLATE/
    └── workflows/
```

---

## 📖 Documentation

* **Proposal**: [PROPOSAL.md](https://github.com/phpwalter/Git-Toolkit/blob/main/PROPOSAL.md)
* **Phase 2 Architecture**: [docs/phase-2-architecture.md](https://github.com/phpwalter/Git-Toolkit/blob/main/docs/phase-2-architecture.md)

---

## 🌍 Localization Strategy

* Canonical docs live in `docs/en/`
* Translated docs live in `docs/es/`, `docs/fr/`, etc.
* Structure synced via `git_toolkit/tools/i18n/sync_docs_structure.py`
* Auto-injected headers, language bars, and nav parity enforced

🔁 Learn more in [DOC SYNC](.github/DOC_SYNC.md)

---

## 🤝 Contributing

1. Fork this repo
2. Create a feature branch: `git checkout -b feature/my-fix`
3. Write tests under `git_toolkit/scripts/tests/`
4. Implement and document
5. Open a Pull Request
6. All checks (CI, lint, tests, versioning) must pass
7. Merge once approved

📘 Contributor guide: [CONTRIBUTING.md](.github/CONTRIBUTING.md)
📑 Governance and behavior: [CODE\_OF\_CONDUCT.md](.github/CODE_OF_CONDUCT.md)

---

## 🚀 Roadmap & Milestones

| Milestone                                                                   | Due Date    | Deliverables                                       |
|-----------------------------------------------------------------------------|-------------|----------------------------------------------------|
| [v0.1.0 (“Hooks”)](https://github.com/phpwalter/Git-Toolkit/milestone/4)    | Aug 15 2025 | `gt init-hooks`, pre-commit & pre-push scripts     |
| [v0.2.0 (“CI”)](https://github.com/phpwalter/Git-Toolkit/milestone/5)       | Sep 15 2025 | GitHub Actions workflows (`ci.yml`, `release.yml`) |
| [v0.2.1 (“Releases”)](https://github.com/phpwalter/Git-Toolkit/milestone/6) | Oct 1 2025  | semantic-release setup, CHANGELOG automation       |
| [v0.3.0 (“Quality”)](https://github.com/phpwalter/Git-Toolkit/milestone/7)  | Nov 1 2025  | Coverage threshold, flake8/black, bandit scans     |
| [v1.0.0 (“Monthly”)](https://github.com/phpwalter/Git-Toolkit/milestone/8)  | Dec 1 2025  | Monthly release job, dashboard & metrics report    |

---

## 🛡️ Security & Compliance

* Vulnerability reporting → [SECURITY.md](.github/SECURITY.md)
* Community rules → [CODE\_OF\_CONDUCT.md](.github/CODE_OF_CONDUCT.md)
* Project governance → [GOVERNANCE.md](.github/GOVERNANCE.md)

---

## ⚖️ License

Licensed under the [MIT License](./LICENSE)

---

_LastUpdate: 2025-07-14_<br>
_Next Review: 2026-07-01_
