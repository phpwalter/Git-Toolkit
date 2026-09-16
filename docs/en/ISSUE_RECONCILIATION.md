# Issue Tracker Reconciliation

This document maps legacy roadmap issues to the stabilized 1.0 codebase. Close an issue only after verifying the merged `main` implementation satisfies its objective.

## Likely completed by stabilization work

| Issue | Legacy objective | Current implementation evidence |
|---|---|---|
| #59 | Multi-repository definition | `Config.repositories` models multiple repositories. |
| #60 | Iterate across repositories | CLI/workflow execution iterates selected repository targets. |
| #61 | Basic multi-repository orchestration | Group targeting and workflow execution exist. |
| #63 | CI/CD readiness | Cross-platform GitHub Actions CI exists. |
| #74 | Prevent force pushes on protected branches | Policy engine blocks unconditional force push and protected rewrites. |
| #77 | Bandit in CI | Bandit production-code gate is active. |
| #79 | Cross-platform compatibility | Linux/macOS/Windows matrix covers Python 3.11-3.13. |
| #84 | Branch naming validation | `safety.branch_name_pattern` policy exists. |
| #93 | Invalid config/Git-state handling | Config errors and Git-state errors are handled explicitly. |
| #96 | pathlib paths | Configuration/runtime path handling uses `pathlib.Path`. |
| #101 | Protected branches config | `safety.protect_branches` exists. |
| #104 | Dependency security scanning | `pip-audit` is a CI gate. |
| #117 | Configuration overrides | Global then project precedence plus `config explain`. |
| #123 | Initial plugin system | Entry-point and explicitly trusted local plugins implemented. |
| #137 | plugins.py | Plugin manager exists. |
| #138 | Plugin commands | Plugins may register CLI commands. |
| #139 | Plugin hook logic | Plugin hook dispatch is supported. |
| #140 | Local plugin discovery | Available behind explicit trust gate. |
| #143 | Versioned plugin API | `PLUGIN_API_VERSION` compatibility check exists. |
| #145 | Dry-run mode | Global dry-run routing exists for supported mutating operations. |
| #153 | SUPPORT.md | Support policy exists in `.github/SUPPORT.md`. |

## Rewrite rather than simply close

- #75/#76/#112: historical flake8/Black wording should be replaced by Ruff-based tooling policy.
- #88: Python 3.7+ is obsolete; supported floor is Python 3.11.
- #122: branch naming exists in product policy, but repository-host CI branch-name enforcement should be evaluated independently.
- #142/#126: plugin architecture exists, but broader plugin API maturity remains an extensibility roadmap item.

## Keep open for post-1.0 scope

- #124 and #154-157: translation/i18n automation.
- #127: advanced workflow customization beyond current linear workflows.
- #132: provider OAuth.
- #133: supported GUI.
- #135: non-Git VCS.
- #136: advanced analytics.

## Reconciliation procedure

For each issue:

1. verify the relevant behavior on merged `main`;
2. link the implementing PR/commit;
3. update stale acceptance criteria when the product direction changed;
4. close as completed only when the objective is actually met;
5. close as not planned when superseded by an intentional design decision;
6. keep remaining work open with current terminology and scope.
