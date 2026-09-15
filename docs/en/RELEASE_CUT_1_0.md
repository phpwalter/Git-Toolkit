# Git Toolkit 1.0 Release Cut Procedure

This procedure is executed only after all 1.0 readiness branches have been merged and `main` is green.

## 1. Verify source state

- Confirm `main` is the checked-out branch.
- Confirm CI is green for the exact `main` commit.
- Confirm there are no uncommitted changes.
- Confirm all required 1.0 documentation and acceptance tests are merged.

## 2. Set the release version

Change the authoritative runtime version from the development value to:

```python
__version__ = "1.0.0"
```

Do not create multiple independent version strings.

## 3. Finalize changelog

Move the 1.0 release content from `Unreleased` under:

```text
## 1.0.0 - YYYY-MM-DD
```

Leave a new empty `Unreleased` section above it.

## 4. Open release-cut pull request

The release-cut PR should contain only release metadata/documentation changes required for 1.0.0. CI must pass without exceptions.

## 5. Merge and verify

After merge:

- verify the exact merge commit is green;
- verify package metadata reports `1.0.0`;
- verify clean-install acceptance succeeds.

## 6. Tag

Create annotated tag `v1.0.0` on the verified green `main` commit and push the tag.

## 7. Automated release

The tag-driven release workflow must:

1. validate tag/package version identity;
2. rerun quality/security/test gates;
3. build wheel and source distribution;
4. validate package metadata;
5. perform a clean wheel install and CLI smoke test;
6. create the GitHub Release;
7. publish the same artifacts to PyPI through trusted publishing.

## 8. Post-release verification

- Confirm GitHub Release assets are present.
- Confirm PyPI reports version 1.0.0.
- Install from PyPI into a clean environment and execute `git-toolkit --version`.
- Confirm `main` remains clean and green.

Any mismatch between tag, package, changelog, GitHub Release, PyPI, or source commit is a release incident and must be corrected before further releases.
