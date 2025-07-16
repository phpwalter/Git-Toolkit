
<!-- PROPOSAL.md Badge Block -->
![Version](https://img.shields.io/github/v/release/phpwalter/Git-Toolkit?label=version&logo=semantic-release&logoColor=white)
![CI](https://img.shields.io/github/actions/workflow/status/phpwalter/Git-Toolkit/ci.yml?label=ci&logo=githubactions&logoColor=white)
![Release](https://img.shields.io/github/actions/workflow/status/phpwalter/Git-Toolkit/release.yml?label=release&logo=rocket&logoColor=white)
![License](https://img.shields.io/github/license/phpwalter/Git-Toolkit?logo=opensourceinitiative&logoColor=white)
![Last Commit](https://img.shields.io/github/last-commit/phpwalter/Git-Toolkit?label=%F0%9F%97%93%20Last%20Commit&color=007ec6)
![Maintenance](https://img.shields.io/badge/%F0%9F%9B%A0%EF%B8%8F%20Maintenance-active-brightgreen)

![toolkit-logo-banner.png](docs/assets/toolkit-logo-banner.png)

# Project Proposal: Git-Toolkit

## 1. 📝Executive Summary  
We propose **Git-Toolkit**, a lightweight, cross-platform Python CLI “sub-module” for standardizing and automating common Git workflows across Windows, macOS, and Linux. By packaging GitPython wrappers, YAML-based config, and a structured hook/plugin system—with first-class support for Git Credential Manager and OAuth—Git-Toolkit will:  
- **Eliminate** ad-hoc, platform-specific scripts  
- **Simplify** authentication and credential management  
- **Empower** new and experienced developers with an extensible, plugin-driven CLI  

---

## 2. 👥 Stakeholders  
This project delivers value to:  
- **Development Teams**  
  Quickly onboard standardized Git workflows with minimal setup.  
- **DevOps Engineers**  
  Consume a zero-touch CI/CD and release pipeline that “just works.”  
- **Release Managers**  
  Gain full traceability of version bumps, changelogs, and deployment cadence.  
- **Open-Source Contributors**  
  Understand project goals, contribution flow, and quality expectations from Day 1.  

---

## 3. 🔍 Existing Solutions & Gaps  
| Project        | Strengths                                            | Gaps                                                                  |
|----------------|------------------------------------------------------|-----------------------------------------------------------------------|
| **Gitless**    | Python “porcelain” with simplified commands          | Standalone VCS; no plugin API; no YAML config; not submodule-friendly |
| **git-extras** | Rich set of helper commands (`git summary`, etc.)    | Shell scripts; no unified Python backend; no hooks API                |
| **pre-commit** | Manages Git hooks via YAML; extensible linters/tests | Focused on hooks/quality; not general Git actions                     |
| **GitHub CLI** | First-class GitHub integration and workflows         | GitHub-specific; closed plugin model; not submodule-centric           |

**Gap to fill:**  
1. Python-first wrappers around core Git operations  
2. Minimal `argparse`-driven CLI  
3. YAML config for defaults, auth, branch conventions  
4. Structured hook/plugin API discoverable in-repo and via entry-points  
5. GCM + optional OAuth for major Git hosts  
6. Submodule integration + `pip install` from path  

---

## 4. ❗Problem Statement & Objectives  
**Pain Points**  
- Inconsistent, scattered scripts per project  
- Manual credential/configuration work on each platform  
- No unified extension mechanism for custom pre/post steps  

**Objectives**  
1. **Core CLI**: `gt clone`, `gt checkout`, `gt status`, `gt push`, `gt submodule update`.  
2. **YAML config**: `.git-toolkit.yaml` or `~/.git-toolkit/config.yaml`.  
3. **Auth**: GCM (default) + PAT; OAuth extensibility.  
4. **Hooks/Plugins**: Python API for lifecycle events.  

---

## 5. 🚧 Scope & Deliverables  

**In-Scope (MVP)**  
- Python 3.8+ CLI using **argparse**  
- **GitPython** wrappers for clone/checkout/status/push/submodule  
- YAML config schema (remote, branch, auth method)  
- Hook points: `pre_clone`, `post_clone`, `pre_push`, `post_push`  
- Git Credential Manager integration via `credential.helper=manager-core`  

**Out-of-Scope (Phase 1)**  
- Full OAuth web-flow (defer to PAT + keyring)  
- GUI or non-Git VCS support  
- Publishing to PyPI (install via path/pip)  
- Advanced process watchers  

---

## 6. 🏗️Technical Architecture & Project Layout  
```
.
├── README.md
├── PROPOSAL.md
├── config\_default.yaml
├── git\_toolkit/
│   ├── **init**.py
│   ├── cli.py
│   ├── config.py
│   ├── auth.py
│   ├── git\_actions.py
│   ├── hooks.py
│   └── tests/
│       ├── test\_cli.py
│       ├── test\_config.py
│       ├── test\_auth.py
│       ├── test\_git\_actions.py
│       └── test\_hooks.py
└── docs/
├── assets/
└── en/, es/, fr/, …

````

---

## 7. 📜 YAML Configuration & Plugin Model  

### Schema (`.git-toolkit.yaml`)
```yaml
default_remote: origin
branch_prefix: feature/
auth:
  method: credential_manager  # | pat
  pat:
    token: YOUR_TOKEN_HERE
hooks_dir: .git-toolkit/hooks    # optional custom hooks folder
````

### Lifecycle Events

* `pre_clone`, `post_clone`
* `pre_checkout`, `post_checkout`
* `pre_commit`, `post_commit`
* `pre_push`, `post_push`

**Plugin Example**

```python
from git_toolkit.hooks import hook

@hook("pre_push")
def enforce_commit_prefix(ctx):
    msg = ctx.repo.git.log("-1", "--pretty=%B")
    if not msg.startswith("FEATURE:"):
        raise RuntimeError("Commit message must start with 'FEATURE:'")
```

---

## 8. 🔒 Authentication Strategy

1. **Phase 1: Git Credential Manager**
2. **Phase 1: PAT via Keyring**
3. **Phase 2: OAuth Flows** (GitHub/GitLab via `requests-oauthlib`)

---

## 9. ⚙️ Integration & Installation

```bash
git submodule add https://github.com/phpwalter/Git-Toolkit.git tools/git-toolkit
pip install --upgrade ./tools/git-toolkit
gt init-hooks      # bootstrap scripts and hooks
gt clone <repo>    # use core CLI
```

---

## 10. 🚀 Roadmap & Milestones

| Milestone                                                                   | Due Date    | Deliverables                                       |
|-----------------------------------------------------------------------------|-------------|----------------------------------------------------|
| [v0.1.0 (“Hooks”)](https://github.com/phpwalter/Git-Toolkit/milestone/4)    | Aug 15 2025 | `gt init-hooks`, pre-commit & pre-push scripts     |
| [v0.2.0 (“CI”)](https://github.com/phpwalter/Git-Toolkit/milestone/5)       | Sep 15 2025 | GitHub Actions workflows (`ci.yml`, `release.yml`) |
| [v0.2.1 (“Releases”)](https://github.com/phpwalter/Git-Toolkit/milestone/6) | Oct 1 2025  | semantic-release setup, CHANGELOG automation       |
| [v0.3.0 (“Quality”)](https://github.com/phpwalter/Git-Toolkit/milestone/7)  | Nov 1 2025  | Coverage ≥ 80%, flake8/black, bandit scans         |
| [v1.0.0 (“Monthly”)](https://github.com/phpwalter/Git-Toolkit/milestone/8)  | Dec 1 2025  | Monthly release job, dashboard & metrics report    |

---

## 11. 🎯 Success Criteria & Metrics

| Category            | Metric                                | Target                        |
| ------------------- | ------------------------------------- | ----------------------------- |
| **Pipeline Health** | CI pass rate on `main` (7-day window) | ≥ 99%                         |
| **Release Cadence** | Merge→release lead time (median, p95) | Median ≤ 2 days; p95 ≤ 5 days |
| **Code Quality**    | Test coverage (%) overall & by module | No module < 80%               |
|                     | Lint errors per commit                | Zero on `main`                |
| **Security**        | High-severity alerts per month        | ≤ 1                           |
| **Adoption**        | Downstream updates via Dependabot     | ≥ 90%                         |

---

## 12. 🗺️ Mapping Goals to Deliverables

| High-Level Goal                             | Milestone & Deliverable                           |
|---------------------------------------------|---------------------------------------------------|
| Rapid Git infra onboarding                  | v0.1.0 – `gt init-hooks` + local hooks            |
| Zero-touch CI/CD                            | v0.2.0 – GitHub Actions (`ci.yml`, `release.yml`) |
| Automated semantic versioning & releases    | v0.2.1 – semantic-release & changelog             |
| Quality gates & security scans              | v0.3.0 – coverage ≥ 80%, flake8/black, bandit     |
| Monthly release cadence & metrics reporting | v1.0.0 – monthly releases + dashboards            |

---

## 13. ⚠️ Risks & Mitigations

* **Platform quirks:** use `pathlib` to abstract OS differences.
* **Missing GCM:** detect at runtime, fallback to PAT with clear guidance.
* **Plugin API churn:** version hook interfaces; deprecate with warnings.

---

*End of Proposal*

_Last Update: 2025-07-16_<br>
_Next Review: 2026-07-01_
