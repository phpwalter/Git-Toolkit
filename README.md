
[![PyPI version](https://img.shields.io/pypi/v/git-toolkit.svg)](https://pypi.org/project/git-toolkit/)
[![Build Status](https://github.com/phpwalter/git-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/phpwalter/git-toolkit/actions)
[![Coverage Status](https://img.shields.io/codecov/c/github/phpwalter/git-toolkit.svg)](https://codecov.io/gh/phpwalter/git-toolkit)
[![Downloads](https://img.shields.io/pypi/dm/git-toolkit.svg)](https://pypi.org/project/git-toolkit/)
[![License](https://img.shields.io/github/license/phpwalter/git-toolkit.svg)](./LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/git-toolkit.svg)](https://pypi.org/project/git-toolkit/)

# 🧰 Git-Toolkit

A lightweight, cross-platform Python CLI toolkit to **standardize** and **automate** common Git workflows for development teams.  
Built on **GitPython**, powered by **YAML** config, and extensible via hooks, plugins, and multi-language docs.

> 🔍 See the full project design in [PROPOSAL.md](./PROPOSAL.md)  
> 📚 Learn about the team process in [`WORKFLOW.md`](.github/WORKFLOW.md)

---

## 🚀 Quick Start

```bash
# Step 1: Add as Git submodule
git submodule add https://github.com/yourorg/git-toolkit.git tools/git-toolkit

# Step 2: Install locally
pip install ./tools/git-toolkit

# Step 3: Initialize config
gt init-config
# → creates .git-toolkit.yaml based on config_default.yaml

# Step 4: Run Git commands
gt clone https://github.com/org/repo.git
gt status
gt push
````

---

## 📋 Features

✅ Git-native commands: `clone`, `checkout`, `status`, `commit`, `push`, `submodule update`
✅ Cross-platform: Windows / macOS / Linux
✅ Configurable via `.git-toolkit.yaml` or global `~/.git-toolkit/config.yaml`
✅ Auth options:

* Git Credential Manager (default)
* Personal Access Token (PAT) with OS keyring
* (Coming soon) OAuth for GitHub/GitLab/Bitbucket
  ✅ Hooks system with lifecycle events:
* `pre_clone`, `post_clone`, `pre_push`, `post_push`, etc.
  ✅ Plugin support via Python entry points
  ✅ Docs localization (`docs/<lang>/`), CI/CD enforcement, and sync tooling

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

## 🌍 Localization Strategy

* Canonical docs live in `docs/en/`
* Translated docs live in `docs/es/`, `docs/fr/`, etc.
* Structure synced via `git_toolkit/tools/i18n/sync_docs_structure.py`
* Auto-injected headers, language bars, and nav parity enforced

🔁 Learn more in [DOCS\_SYNC.md](.github/DOCS_SYNC.md)

---

## 🤝 Contributing

1. Fork this repo
2. Create a feature branch: `git checkout -b feature/my-fix`
3. Write tests under `git_toolkit/tests/`
4. Implement and document
5. Open a Pull Request

📘 Contributor guide: [CONTRIBUTING.md](.github/CONTRIBUTING.md)
📑 Governance and behavior: [CODE\_OF\_CONDUCT.md](.github/CODE_OF_CONDUCT.md)

---

## 📅 Roadmap

| Version | Milestones                                        |
| ------- | ------------------------------------------------- |
| `v0.1`  | CLI + config + hooks + GCM auth                   |
| `v0.2`  | PAT support, full test coverage, i18n             |
| `v0.3`  | OAuth auth, plugin registry                       |
| `v1.0`  | Production-ready, PyPI badges, release automation |

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

