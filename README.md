
[![PyPI version](https://img.shields.io/pypi/v/git-toolkit.svg)](https://pypi.org/project/git-toolkit/)
[![Build Status](https://github.com/phpwalter/git-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/phpwalter/git-toolkit/actions)
[![Coverage Status](https://img.shields.io/codecov/c/github/yourorg/git-toolkit.svg)](https://codecov.io/gh/phpwalter/git-toolkit)
[![Downloads](https://img.shields.io/pypi/dm/git-toolkit.svg)](https://pypi.org/project/git-toolkit/)
[![License](https://img.shields.io/github/license/phpwalter/git-toolkit.svg)](./LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/git-toolkit.svg)](https://pypi.org/project/git-toolkit/)

# Git-Toolkit

A lightweight, cross-platform Python CLI “sub-module” to **standardize** and **automate** common Git workflows on Windows, macOS, and Linux.  
Built on **GitPython**, driven by **YAML** config, with a structured hook/plugin system and built-in support for Git Credential Manager and optional OAuth.

**For the full design, timeline, and scope, see [PROPOSAL.md](./PROPOSAL.md).**

---

## 🚀 Quick Start

1. **Add as a Git submodule**  
   ```bash
   git submodule add https://github.com/yourorg/git-toolkit.git tools/git-toolkit
   ````

2. **Install locally**

   ```bash
   pip install --upgrade ./tools/git-toolkit
   ```
3. **Initialize default config**

   ```bash
   gt init-config
   # creates .git-toolkit.yaml based on config_default.yaml
   ```
4. **Run commands**

   ```bash
   gt clone https://github.com/yourorg/another-repo.git
   gt status
   gt push
   ```

---

## 📋 Features

* **Core Git commands**: `clone`, `checkout`, `status`, `commit`, `push`, `submodule update`
* **Cross-platform**: Windows, macOS, Linux
* **YAML-based configuration** (`.git-toolkit.yaml` or `~/.git-toolkit/config.yaml`)
* **Authentication**:

  * Git Credential Manager (default)
  * Personal Access Token via OS keyring
  * (Future) OAuth for GitHub/GitLab/Bitbucket
* **Hook/plugin system**: lifecycle events (`pre_clone`, `post_clone`, `pre_push`, `post_push`, …)
* **Submodule integration**: simple `git submodule add` + `pip install` workflow

---

## ⚙️ Configuration

Create or edit `.git-toolkit.yaml` in your repo root:

```yaml
default_remote: origin
branch_prefix: feature/
auth:
  method: credential_manager  # | pat
  pat:
    token: YOUR_TOKEN_HERE
hooks_dir: .git-toolkit/hooks    # optional custom hooks folder
```

See [`config_default.yaml`](config_default.yaml) for full schema and defaults.

---

## 🔌 Hooks & Plugins

Drop a custom hook in your repo (e.g. `.git-toolkit/hooks/enforce_prefix.py`):

```python
from git_toolkit.hooks import hook

@hook("pre_push")
def enforce_feature_prefix(ctx):
    last_msg = ctx.repo.git.log("-1", "--pretty=%B")
    if not last_msg.startswith("FEATURE:"):
        raise RuntimeError("Commit message must start with 'FEATURE:'")
```

Or publish a plugin package with an entry-point under `git_toolkit.plugins`.

---

## 📦 Project Layout

```
.
├── README.md
├── PROPOSAL.md
├── config_default.yaml
├── git_toolkit/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── auth.py
│   ├── git_actions.py
│   ├── hooks.py
│   └── tests/
│       ├── test_cli.py
│       ├── test_config.py
│       ├── test_auth.py
│       ├── test_git_actions.py
│       └── test_hooks.py
├── docs/
│   ├── en/
│   │   ├── contributing.md       ← Optional mirror of GitHub-facing files
│   │   ├── code-of-conduct.md
│   │   ├── governance.md
│   │   └── security.md
│   ├── es/
│   │   ├── README.md
│   │   ├── quickstart.md
│   │   ├── PROPOSAL.md
│   │   ├── cómo-contribuir.md     ← CONTRIBUTING translated
│   │   ├── código-de-conducta.md  ← CODE_OF_CONDUCT translated
│   │   ├── gobernanza.md          ← GOVERNANCE translated
│   │   └── seguridad.md           ← SECURITY translated
│   └── fr/
│       ├── README.md
│       ├── quickstart.md
│       ├── PROPOSAL.md
│       ├── contribuer.md          ← CONTRIBUTING translated
│       ├── code-de-conduite.md    ← CODE_OF_CONDUCT translated
│       ├── gouvernance.md         ← GOVERNANCE translated
│       └── sécurité.md            ← SECURITY translated
└── .github/
    ├── CONTRIBUTING.md            ← Primary GitHub-linked version
    ├── CODE_OF_CONDUCT.md
    ├── GOVERNANCE.md
    ├── SECURITY.md
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.yml
    │   ├── feature_request.yml
    │   └── config.yml
    ├── PULL_REQUEST_TEMPLATE.md
    └── workflows/
        └── ci.yml                 ← GitHub Actions for CI/lint/test
```

---

## 🌐 Localization

* **Canonical English docs** live at the repo root.
* **Translated docs** under `docs/<lang>/`, including localized `README.md`, `quickstart.md`, and `PROPOSAL.md`.

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch (`git checkout -b feature/xyz`)
3. Write tests under `git_toolkit/tests/`
4. Implement and document your changes
5. Submit a Pull Request against the appropriate milestone

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📅 Roadmap

* **v0.1 (MVP)**: core CLI, YAML config, GCM auth, basic hooks
* **v0.2**: PAT/keyring support, additional lifecycle events
* **v0.3**: OAuth flows, plugin packaging via entry-points
* **v1.0**: Production-ready release

---

## ⚖️ License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

_Last Updated: 2025-07-12_<br>
_Next Review: 2026-07-01_
