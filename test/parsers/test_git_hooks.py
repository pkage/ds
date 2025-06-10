"""Test the git hooks integration."""

# std
from pathlib import Path

# lib
import pytest

# pkg
from ds.git import find_git_directory


def test_finds_git_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # setup: create nested directory structure with .git
    root = tmp_path / "project"
    nested = root / "src" / "module"
    git_dir = root / ".git"
    git_dir.mkdir(parents=True)
    nested.mkdir(parents=True)

    # change current working dir to nested module
    monkeypatch.chdir(nested)

    # do the test
    found = find_git_directory()

    assert found == git_dir


def test_returns_none_if_no_git(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # setup: create directory with no .git
    work_dir = tmp_path / "work"
    work_dir.mkdir()

    monkeypatch.chdir(work_dir)

    # perform the test
    found = find_git_directory()

    assert found is None


def test_git_file_instead_of_dir(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # setup: simulate a .git *file* (e.g., for a git worktree)
    root: Path = tmp_path / "project"
    nested: Path = root / "subdir"
    nested.mkdir(parents=True)

    git_file: Path = root / ".git"
    git_file.write_text("gitdir: ../.git/worktrees/project")

    monkeypatch.chdir(nested)

    # test
    found = find_git_directory()

    assert found is None
