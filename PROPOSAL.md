<!--
 file: PROPOSAL.md
 path: L:/var/www/Git-Toolkit/PROPOSAL.md
 version: 1.0.0
 date: 2026-03-13
 author: Walter Torres
 copyright: Copyright 2026, Git-Toolkit.
 license: MIT
 maintainer: Git-Toolkit Team
 status: dev

 Project proposal for the Git Toolkit, outlining its executive summary, problem statement, and objectives.
-->

<!-- PROPOSAL.md Badge Block -->
![Version](https://img.shields.io/github/v/release/phpwalter/Git-Toolkit?label=version&logo=semantic-release&logoColor=white)
![CI](https://img.shields.io/github/actions/workflow/status/phpwalter/Git-Toolkit/ci.yml?label=ci&logo=githubactions&logoColor=white)
![Release](https://img.shields.io/github/actions/workflow/status/phpwalter/Git-Toolkit/release.yml?label=release&logo=rocket&logoColor=white)
![License](https://img.shields.io/github/license/phpwalter/Git-Toolkit?logo=opensourceinitiative&logoColor=white)
![Last Commit](https://img.shields.io/github/last-commit/phpwalter/Git-Toolkit?label=%F0%9F%97%93%20Last%20Commit&color=007ec6)
![Maintenance](https://img.shields.io/badge/%F0%9F%9B%A0%EF%B8%8F%20Maintenance-active-brightgreen)

---

![toolkit-logo-banner.png](./docs/assets/toolkit-logo-banner.png)
# <img src="./docs/assets/toolkit-icon.png" alt="Description" width="30"/> Project Proposal: Git Toolkit

---

## 1. 📝 Executive Summary

**Git Toolkit** is a lightweight, per-project Git automation utility designed to standardize developer workflows, streamline Git operations, and simplify team onboarding across all major platforms (Windows, macOS, Linux).

Unlike global CLI tools, Git Toolkit is added to each repository as a **submodule**. Projects define their own Git workflows using a declarative YAML configuration (`.git-toolkit.yml`) and may extend behavior using plugins, hooks, and language-agnostic scripts.

The toolkit wraps `GitPython`, supports Git Credential Manager and Personal Access Tokens, and provides lifecycle hooks and CI/CD-friendly scripting—making it ideal for modern developer environments.

---

## 2. 👥 Stakeholders

Git Toolkit provides value to:

- **Developers**: Use clean, version-controlled Git workflows per project.
- **DevOps Teams**: Automate repetitive tasks, enforce Git policy, and integrate with CI/CD pipelines.
- **Release Managers**: Track versions, enforce commit hygiene, and simplify tagging + changelog generation.
- **Open Source Maintainers**: Document, share, and enforce project-specific Git behaviors with contributors.

---

## 3. 🔍 Market Gaps & Alternatives

| Tool           | Strengths                       | Limitations                                               |
|----------------|---------------------------------|-----------------------------------------------------------|
| **Gitless**    | Simplifies Git for end-users    | Not compatible with Git; no plugin system; not extensible |
| **git-extras** | Many helpful CLI aliases        | Hard to extend; shell-based; no Python API or hooks       |
| **pre-commit** | Great for hook-based automation | Focused on linting/testing, not Git workflows             |
| **GitHub CLI** | Deep GitHub integration         | GitHub-specific; no local project config; not extensible  |

### Git Toolkit fills these gaps:
✅ Python-first, submodule-based CLI  
✅ Per-project `.git-toolkit.yml` config  
✅ Lifecycle hooks (`pre_push`, `post_commit`, etc.)  
✅ Plugin-ready, scriptable, and CI/CD-compatible  
✅ Auth via GCM, PAT, and future OAuth support

---

## 4. ❗ Problem Statement & Objectives

### Problems:
- Teams reinvent Git workflows across repos
- Git credential setup varies across machines and OSes
- No consistent way to define, share, or validate Git behaviors

### Objectives:
1. **Scriptable CLI** for Git operations (`clone`, `status`, `push`, etc.)
2. **Declarative configuration** with per-project `.git-toolkit.yml`
3. **Secure authentication** with Git Credential Manager and optional PATs
4. **Hooks and plugins** for pre/post-action automation
5. **Cross-platform and CI/CD ready**

---

## 5. 🚧 Scope & Deliverables

### ✅ In Scope (MVP)
- Python CLI using `argparse` and `GitPython`
- CLI commands: `clone`, `status`, `push`, `checkout`, `submodule update`
- Per-project config file: `.git-toolkit.yml`
- Hook system: `pre_clone`, `post_push`, etc.
- Plugin loader using entry points or local scripts
- Auth support: Git Credential Manager (default), Personal Access Token (PAT)

### 🚫 Out of Scope (MVP)
- OAuth web flows (planned for future)
- GUI interface
- PyPI package distribution
- Support for non-Git VCS

---

## 6. 🏗 Project Architecture

### Submodule Usage (User Project View)
```
your-project/
├── .git/
├── .git-toolkit/            # Git Toolkit submodule
├── .git-toolkit.yml         # Project-specific config
└── src/
```

### Git Toolkit Source Layout (Contributor View)
```
.
├── README.md
├── PROPOSAL.md
├── config\_default.yaml
├── git\_toolkit/
│   ├── cli.py
│   ├── config.py
│   ├── hooks.py
│   ├── auth.py
│   ├── git\_actions.py
│   └── tests/
│       └── test\_\*.py
├── docs/
│   ├── en/, es/, fr/
└── .github/
├── CONTRIBUTING.MD, workflows/, etc.
````

---

## 7. ⚙️ Configuration & Hooks

### Sample `.git-toolkit.yml`
```yaml
repositories:
  - name: main
    path: .
  - name: ui
    path: ./packages/ui
    default_branch: main

commands:
  status:
    script: |
      git -C {{repo.path}} status

  release:
    steps:
      - tag: v{{ version }}
      - push-tags: true

safety:
  prevent_force_push: true
  protect_branches:
    - main
    - release/*
````

### Supported Hook Events

* `pre_clone`, `post_clone`
* `pre_checkout`, `post_checkout`
* `pre_commit`, `post_commit`
* `pre_push`, `post_push`

### Plugin Example

```python
from git_toolkit.hooks import hook

@hook("pre_push")
def require_tagged_commit(ctx):
    if "v" not in ctx.repo.git.describe("--tags"):
        raise RuntimeError("All pushes must include a Git tag.")
```

---

## 8. 🔒 Authentication Strategy

| Method                 | Description                     | Status     |
|------------------------|---------------------------------|------------|
| Git Credential Manager | Native OS-integrated auth       | ✅ MVP      |
| Personal Access Token  | Read from config or keyring     | ✅ MVP      |
| OAuth (GitHub/GitLab)  | Planned via `requests-oauthlib` | 🔜 Phase 2 |

---

## 9. 📦 Installation & Usage

```bash
# Add to project
git submodule add https://github.com/phpwalter/Git-Toolkit.git .git-toolkit

# Install dependencies
pip install -r .git-toolkit/requirements.txt

# Run a command
.git-toolkit/git-toolkit status
```

You can also alias the command:

```bash
ln -s .git-toolkit/git-toolkit git-toolkit
./git-toolkit release
```

---

## 10. 🚀 Roadmap & Milestones

| Milestone         | ETA         | Goals                                        |
|-------------------|-------------|----------------------------------------------|
| v0.1.0 "Hooks"    | Aug 15 2025 | Hook system, CLI commands, config loading    |
| v0.2.0 "CI"       | Sep 15 2025 | GitHub Actions (`ci.yml`, `release.yml`)     |
| v0.2.1 "Releases" | Oct 1 2025  | semantic-release, changelog, version tagging |
| v0.3.0 "Quality"  | Nov 1 2025  | 80%+ test coverage, linting, security scans  |
| v1.0.0 "Monthly"  | Dec 1 2025  | Monthly release job, contribution dashboard  |

---

## 11. 🎯 Success Criteria

| Category        | Metric                            | Target                   |
|-----------------|-----------------------------------|--------------------------|
| CI Health       | Main branch build pass rate       | ≥ 99%                    |
| Test Coverage   | Module-level coverage             | ≥ 80% in all modules     |
| Adoption        | Submodules added to projects      | ≥ 5 internal repos by Q4 |
| Developer Setup | Time to usable CLI in new project | ≤ 5 minutes              |
| Lint/Style      | Zero flake8/black issues on main  | ✅ enforced               |

---

## 12. 🧭 Strategic Mapping

| Goal                               | Milestone       |
|------------------------------------|-----------------|
| Standardized Git workflows         | v0.1.0 + v0.2.0 |
| Extensible, declarative config     | v0.1.0          |
| Safe CI/CD with Git best practices | v0.2.0 + v0.2.1 |
| High quality, secure releases      | v0.3.0          |
| Visibility and governance          | v1.0.0          |

---

## 13. ⚠️ Risks & Mitigations

| Risk                        | Mitigation Strategy                        |
|-----------------------------|--------------------------------------------|
| Missing auth tools (GCM)    | Fallback to PAT + error guidance           |
| Platform path issues        | Use `pathlib` and cross-platform testing   |
| Plugin instability          | Version plugin API and enforce warnings    |
| Overuse of “magic” defaults | Clear config override rules + dry-run mode |

---

_Last updated: 2025-07-16_<br>
_Next review: 2026-07-01_
