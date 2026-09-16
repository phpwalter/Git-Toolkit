# Maintainers

## Current maintainer

- `@phpwalter` — project owner and primary maintainer.

## Maintainer responsibilities

Maintainers are responsible for preserving the project's deterministic and security-sensitive contracts. Responsibilities include:

- reviewing pull requests and release changes;
- maintaining supported Python and operating-system matrices;
- keeping CI, coverage, security, dependency, and packaging gates effective;
- triaging issues and security reports;
- reconciling documentation with shipped behavior;
- controlling release versioning, tags, GitHub Releases, and PyPI publication;
- protecting credential, shell-execution, plugin, branch, remote-host, and force-push boundaries;
- ensuring post-1.0 work is not presented as supported 1.0 functionality before it is ready.

## Change approval

Changes to security boundaries, release automation, credential handling, policy enforcement, or compatibility commitments require explicit maintainer review. Mandatory release gates must not be bypassed by documentation-only exceptions or ad hoc overrides.

## Release authority

A production release must originate from a verified commit on `main`, pass required CI and release checks, and use matching source, package, tag, changelog, and release metadata.
