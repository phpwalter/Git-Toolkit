# Main Branch Stability Policy

`main` is the authoritative integration and stable-release branch for Git Toolkit.

## Merge requirements

A change may merge to `main` only when:

- the pull request targets `main` from a feature branch;
- the complete CI matrix is green;
- production lint, type, security, dependency, test, coverage, build, and smoke checks pass;
- required documentation is updated with behavior changes;
- no unresolved release-blocking review comments remain.

## Direct pushes

Normal development should not be performed by direct push to `main`. Emergency maintenance must still satisfy the same CI and review evidence before release.

## Release source

Only a `main` commit with a green CI result may receive a production version tag. The release workflow verifies that the tag version matches package metadata.

## Stability expectation

`main` should remain installable and usable. Experimental work belongs on feature branches and must not depend on unmerged sibling branches.

## Recommended GitHub ruleset

Configure repository rules to:

1. require pull requests before merge;
2. require the CI workflow/status checks;
3. require branches to be up to date before merge;
4. block force pushes and deletions on `main`;
5. restrict bypass privileges to emergency maintainers;
6. require conversation resolution before merge.

Repository-host rules complement, but do not replace, Git Toolkit's own protected-branch policy.
