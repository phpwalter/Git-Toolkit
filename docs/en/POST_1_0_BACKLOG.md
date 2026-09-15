# Post-1.0 Backlog Boundary

The following capabilities are intentionally excluded from the Git Toolkit 1.0 release gate. They may be developed after the CLI/policy core is stable.

## Workflow engine evolution

- DAG execution and dependency graphs.
- Cross-step output passing.
- Compensation/rollback steps.
- Long-running workflow persistence/resume.

## Authentication providers

- Provider-specific OAuth for GitHub, GitLab, Bitbucket, and others.
- Browser-based authorization UX.
- Provider account/session management.

## User interface

- Supported browser GUI/control plane.
- Desktop application.
- Visual workflow/configuration builder.

## Additional version-control systems

- Mercurial.
- Subversion.
- Other non-Git adapters.

## Advanced analytics

- Organization-level compliance/adherence reporting.
- Historical trend warehouse.
- Team productivity or individual evaluation features are not implied by current repository health metrics.

## Localization automation

- Translation synchronization tooling.
- Translation status automation.
- Contributor assignment/notification for localization work.

## Scope rule

Post-1.0 work must not delay a release once all documented 1.0 requirements are met. Any proposal to move one of these items into 1.0 requires an explicit scope change with new acceptance criteria and release impact analysis.
