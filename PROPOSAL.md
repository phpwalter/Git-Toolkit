[![PyPI version](https://img.shields.io/pypi/v/git-toolkit.svg)](https://pypi.org/project/git-toolkit/)
[![Build Status](https://github.com/phpwalter/git-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/yourorg/git-toolkit/actions)
[![Coverage Status](https://img.shields.io/codecov/c/github/yourorg/git-toolkit.svg)](https://codecov.io/gh/yourorg/git-toolkit)
[![Downloads](https://img.shields.io/pypi/dm/git-toolkit.svg)](https://pypi.org/project/git-toolkit/)
[![License](https://img.shields.io/github/license/phpwalter/git-toolkit.svg)](./LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/git-toolkit.svg)](https://pypi.org/project/git-toolkit/)



# Project Proposal: Git-Toolkit

## 1. Executive Summary  
We propose **Git-Toolkit**, a lightweight, cross-platform Python CLI “sub-module” for standardizing and automating common Git workflows across Windows, macOS, and Linux. By packaging GitPython wrappers, YAML-based config, and a structured hook/plugin system—with first-class support for Git Credential Manager and OAuth—Git-Toolkit will:  
- **Eliminate** ad-hoc, platform-specific scripts  
- **Simplify** authentication and credential management  
- **Empower** both new and experienced developers with an extensible, plugin-driven CLI  

## 2. Existing Solutions & Gaps  
| Project        | Strengths                                              | Gaps                                                              |
|----------------|--------------------------------------------------------|-------------------------------------------------------------------|
| **Gitless**    | Python “porcelain” with simplified commands            | Standalone VCS; no plugin API; no YAML config; not submodule-friendly |
| **git-extras** | Rich set of helper commands (`git summary`, etc.)      | Shell scripts; no unified Python backend; no hooks API           |
| **pre-commit** | Manages Git hooks via YAML; extensible linters/tests   | Focused on hooks/quality checks; not general Git actions         |
| **GitHub CLI** | First-class GitHub integration and workflows           | GitHub-specific; closed plugin model; not submodule-centric       |

**Gap to fill**:  
1. **Python-first** wrappers around core Git operations.  
2. **argparse-driven** minimal CLI.  
3. **YAML config** for defaults, auth, branch conventions.  
4. **Structured hook/plugin API** discoverable both in-repo and via entry-points.  
5. **GCM + optional OAuth** for major Git hosts.  
6. **Submodule integration** plus `pip install` from path.

## 3. Problem Statement & Objectives  
**Pain Points**  
- Inconsistent, scattered scripts per project  
- Manual credential/configuration work on each platform  
- No unified extension mechanism for custom pre/post steps  

**Objectives**  
1. **Core CLI**: `gt clone`, `gt checkout`, `gt status`, `gt push`, `gt submodule update`.  
2. **YAML config**: `.git-toolkit.yaml` or `~/.git-toolkit/config.yaml`.  
3. **Auth**: GCM (default) + PAT; OAuth extensibility.  
4. **Hooks/Plugins**: Python API for lifecycle events.

## 4. Scope & Deliverables  
**In-Scope (MVP)**  
- Python 3.8+ CLI using **argparse**  
- **GitPython** wrappers for clone/check-out/status/push/submodule  
- YAML config schema (remote, branch, auth method)  
- Hook points: `pre_clone`, `post_clone`, `pre_push`, `post_push`  
- Git Credential Manager integration via `credential.helper = manager-core`  

**Out-of-Scope (Phase 1)**  
- Full OAuth web-flow (defer to PAT + keyring)  
- GUI or non-Git VCS support  
- Publishing to PyPI (install via path/pip)  
- Advanced process watchers

## 5. Technical Architecture & Project Layout  
```

.
├── README.md                # English front-door
├── PROPOSAL.md              # English canonical proposal
├── config\_default.yaml     # YAML schema & defaults
├── git\_toolkit/            # source code + tests
│   ├── **init**.py
│   ├── cli.py               # argparse entry point
│   ├── config.py            # load & validate YAML
│   ├── auth.py              # GCM + PAT + keyring helpers
│   ├── git\_actions.py      # GitPython command wrappers
│   ├── hooks.py             # hook registry & executor
│   └── tests/               # unit tests co-located with code
│       ├── test\_cli.py
│       ├── test\_config.py
│       ├── test\_auth.py
│       ├── test\_git\_actions.py
│       └── test\_hooks.py
└── docs/                    # localized docs
├── es/                      # Spanish translations
│   ├── README.md
│   ├── quickstart.md
│   └── PROPOSAL.md          # Spanish translation
├── fr/                      # French translations
│   ├── README.md
│   ├── quickstart.md
│   └── PROPOSAL.md          # French translation
└── …                        # other languages

````

- **CLI (`cli.py`)** loads config, initializes auth, dispatches commands.  
- **Config (`config.py`)** merges defaults, local override, validates schema.  
- **Auth (`auth.py`)** configures GCM, reads PAT or keyring.  
- **Git Actions (`git_actions.py`)** wrap GitPython for core operations.  
- **Hooks (`hooks.py`)** support `@hook(event)` registration and dynamic discovery (in-repo or via entry-points).  
- **Tests** live inside the package to stay close to the code they verify.  
- **Docs** for each locale under `docs/<lang>/`, with canonical English files at the root.

## 6. YAML Configuration & Plugin Model  
### YAML Schema (`.git-toolkit.yaml`)
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

## 7. Authentication Strategy

1. **Phase 1: Git Credential Manager**

   * `repo.git.config("credential.helper", "manager-core")`
   * Leverage OS-native credential UI.
2. **Phase 1: PAT via Keyring**

   * Store token in OS keyring; read into HTTP headers if needed.
3. **Phase 2: OAuth Flows**

   * GitHub/GitLab OAuth via `requests-oauthlib`; tokens in keyring.

## 8. Integration & Installation

**Downstream Setup**

```bash
# 1. Add submodule
git submodule add https://github.com/you/git-toolkit.git tools/git-toolkit

# 2. Install
pip install --upgrade ./tools/git-toolkit

# 3. Init config
gt init-config   # copies config_default.yaml → .git-toolkit.yaml

# 4. Use
gt clone https://github.com/org/repo.git
```

A bootstrap script (`tools/git-toolkit/bootstrap.py`) will automate these steps.

## 9. Timeline & Milestones

| Phase              | Duration | Deliverables                                            |
| ------------------ | -------- | ------------------------------------------------------- |
| **Planning**       | 3 days   | Final YAML schema, hook list, auth approach             |
| **MVP Dev**        | 1 week   | Core CLI + config + GitPython actions + GCM integration |
| **Hooks System**   | 3 days   | Hook registry + sample plugins                          |
| **Testing & Docs** | 4 days   | pytest tests, README, quickstart guide                  |
| **Release v0.1**   | 2 days   | Tagged repo; bootstrap script; install instructions     |

## 10. Risks & Mitigations

* **Platform quirks**: use `pathlib` to abstract OS differences.
* **Missing GCM**: detect at runtime, fallback to PAT mode with clear guidance.
* **Plugin API churn**: version hook interfaces; deprecate with warnings.

## 11. Success Criteria

* ✅ Core commands functional on Windows/macOS/Linux in sample repos
* ✅ Seamless auth via GCM or PAT without manual prompts
* ✅ Two community-authored plugins demonstrating hook usage
* ✅ ≥ 80% test coverage; clear documentation; zero paid dependencies

---

*End of Proposal*

_Last Update: 2025-07-12_<br>
_Next Review: 2026-07-01_
