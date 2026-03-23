![toolkit-logo-banner.png](../../docs/assets/toolkit-logo-banner.png)
# <img src="../../docs/assets/toolkit-icon.png" alt="Description" width="30"/> Maintainers – Git Toolkit

This document defines the **maintainer model, authority boundaries, and governance expectations** for the Git Toolkit open-source project.

Git Toolkit is currently a **single-maintainer project**. This document exists to set clear expectations for contributors, reviewers, and future maintainers.

---

## 👤 Current Maintainer

**Primary Maintainer & Project Owner**

-   **Name:** Walter Torres
-   **GitHub:** [@phpwalter](https://github.com/phpwalter)
-   **Role:** Architect, Maintainer, Release Authority
-   **Responsibilities:**
    -   Architectural integrity and core design decisions
    -   Milestone approval and roadmap planning
    -   Pull request review and merge
    -   Release tagging and publication
    -   Security triage and disclosure handling
    -   Community management and conflict resolution

All final decisions regarding Git Toolkit rest with the Primary Maintainer.

---

## 🔑 Maintainer Authority

The Primary Maintainer has final authority over:

-   Core architecture and design of the Git Toolkit CLI
-   Interpretation and enforcement of Git automation rules
-   Configuration schema and extensibility mechanisms (hooks, plugins)
-   CLI command surface and flags
-   Release tagging and versioning
-   Acceptance or rejection of contributions
-   Project governance and policy updates

This authority exists to preserve **consistency, security, and long-term maintainability** of the Git Toolkit.

---

## 🛠 Maintainer Responsibilities

Maintainers are expected to:

-   Review pull requests in a timely and constructive manner
-   Ensure contributions align with:
    -   [GOVERNANCE.md](./GOVERNANCE.md)
    -   [ROADMAP.md](../../ROADMAP.md)
    -   [MILESTONES.md](../../MILESTONES.md)
    -   [CONTRIBUTING.md](./CONTRIBUTING.md)
-   Enforce test coverage and code quality standards
-   Maintain a clear and accurate [CHANGELOG.md](../../CHANGELOG.md) (or similar release notes)
-   Respond to security disclosures per [SECURITY.md](./SECURITY.md)
-   Communicate clearly and respectfully with contributors and the community

---

## 🤝 Contributor Interaction Model

Contributors are welcome to:

-   Submit bug fixes
-   Improve documentation
-   Propose enhancements aligned with existing milestones or the roadmap
-   Suggest future roadmap items

Contributors **must not**:

-   Merge their own pull requests
-   Introduce breaking changes without prior discussion and maintainer approval
-   Modify core architectural invariants without maintainer approval
-   Publish releases or tags

---

## 🔁 Pull Request Review Process

1.  Contributor opens a PR.
2.  PR must reference:
    -   Relevant issue or feature request.
    -   Related milestone (if applicable).
3.  Tests must pass, and code quality standards must be met.
4.  Maintainer reviews for:
    -   Architectural alignment and design principles.
    -   Code quality, test coverage, and documentation.
    -   Adherence to project policies.
5.  Maintainer approves and merges.

The maintainer may request changes or close PRs that do not align with project goals or standards.

---

## 🔐 Security Handling

All security issues must follow the process defined in [SECURITY.md](./SECURITY.md).

Security fixes may bypass normal release cadence and be issued as patch releases at the maintainer’s discretion.

---

## 🧭 Adding Additional Maintainers (Future)

Git Toolkit may add additional maintainers in the future if:

-   The project reaches sustained external adoption.
-   A contributor demonstrates long-term, high-quality involvement and commitment to the project's vision.
-   There is clear alignment with the project’s architectural philosophy and governance model.

New maintainers will be added **by invitation only** and documented in this file.

---

## 🔚 Maintainer Transition or Project Status

If the Primary Maintainer steps down:

-   This file will be updated to reflect new ownership **or**
-   The project will be marked as **archived** with clear notice in [README.md](../../README.md)

---

## 📘 Related Documents

-   [GOVERNANCE.md](./GOVERNANCE.md) – Project governance model
-   [CONTRIBUTING.md](./CONTRIBUTING.md) – Contribution rules and guidelines
-   [ROADMAP.md](../../ROADMAP.md) – Project execution plan and future direction
-   [MILESTONES.md](../../MILESTONES.md) – Key project objectives and timelines
-   [RELEASE.md](../../RELEASE.md) – Release process and versioning strategy
-   [SECURITY.md](./SECURITY.md) – Vulnerability disclosure policy
-   [CHARTER.md](../../CHARTER.md) – Project mission, scope, and long-term goals

---

**Maintainer Note:**
Git Toolkit prioritizes consistency, automation, and security. Every decision is made with long-term stability and team productivity in mind.
