"""Experimental git hooks integration."""

# std
from pathlib import Path
from typing import Dict, List

VALID_GIT_HOOKS = [
    "applypatch-msg",
    "commit-msg",
    "fsmonitor-watchman",
    "post-update",
    "pre-applypatch",
    "pre-commit",
    "pre-merge-commit",
    "pre-push",
    "pre-rebase",
    "pre-receive",
    "prepare-commit-msg",
    "push-to-checkout",
    "update",
]
"""List of all valid git hook names."""

Hooks = Dict[str, List[str]]
"""Hooks are a valid git hook identifier and a list of tasks to execute"""


def find_git_directory() -> Path | None:
    """
    Recurse up directories until we find a .git folder, otherwise bail.
    """

    cwd = Path(".").absolute()

    # little hack: iterate through this directory and all its parents
    for path in [cwd, *cwd.parents]:
        gitpath = path / Path(".git")
        if gitpath.exists() and gitpath.is_dir():
            # found a match
            return gitpath

    return None
