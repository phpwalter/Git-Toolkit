from pathlib import Path

import pytest

from tools.verify_version_consistency import package_version, runtime_version, tag_version, verify


def test_reads_matching_versions(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\nname = "git-toolkit"\nversion = "1.2.3"\n', encoding="utf-8")
    version_file = tmp_path / "version.py"
    version_file.write_text('__version__ = "1.2.3"\n', encoding="utf-8")

    assert package_version(pyproject) == "1.2.3"
    assert runtime_version(version_file) == "1.2.3"
    assert verify(pyproject, version_file, "v1.2.3") == "1.2.3"


def test_rejects_version_mismatch(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\nname = "git-toolkit"\nversion = "1.2.3"\n', encoding="utf-8")
    version_file = tmp_path / "version.py"
    version_file.write_text('__version__ = "1.2.4"\n', encoding="utf-8")

    with pytest.raises(ValueError, match="Version mismatch"):
        verify(pyproject, version_file)


def test_rejects_tag_mismatch_and_invalid_tag(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\nname = "git-toolkit"\nversion = "1.2.3"\n', encoding="utf-8")
    version_file = tmp_path / "version.py"
    version_file.write_text('__version__ = "1.2.3"\n', encoding="utf-8")

    with pytest.raises(ValueError, match="Tag/version mismatch"):
        verify(pyproject, version_file, "v1.2.4")
    with pytest.raises(ValueError, match="vMAJOR.MINOR.PATCH"):
        tag_version("release-1.2.3")
