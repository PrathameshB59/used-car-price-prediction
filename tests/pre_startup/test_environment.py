"""
AutoValue AI environment tests.

Purpose:
    Verify that the project runs inside an activated Python virtual
    environment while allowing that environment to live outside the
    Dropbox project directory.

Inputs:
    VIRTUAL_ENV, sys.prefix, and required package imports.

Outputs:
    Tests pass when the intended virtual environment is active and
    required dependencies can be imported.

Why:
    On Linux, the Python executable inside a virtual environment may
    ultimately resolve to the system Python binary. Therefore,
    checking Path(sys.executable).resolve() is not a reliable way to
    identify the active virtual environment.
"""

from __future__ import annotations

import os
import site
import sys
from pathlib import Path


# This points to the source-code repository, not the Python environment.
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_virtual_environment_is_active() -> None:
    """
    Purpose:
        Confirm that a Python virtual environment is active.

    Inputs:
        VIRTUAL_ENV environment variable.

    Outputs:
        Passes when VIRTUAL_ENV exists and points to a directory.

    Why:
        The shell should explicitly activate the project's Python
        environment before running the test system.
    """
    virtual_env = os.environ.get("VIRTUAL_ENV")

    assert virtual_env, (
        "No virtual environment is active. "
        "Activate ~/.virtualenvs/autovalue-ai before running tests."
    )

    virtual_env_path = Path(virtual_env).expanduser()

    assert virtual_env_path.is_dir(), (
        f"VIRTUAL_ENV points to a missing directory: {virtual_env_path}"
    )


def test_virtual_environment_is_outside_project() -> None:
    """
    Purpose:
        Confirm that the Python environment is stored outside Dropbox.

    Inputs:
        VIRTUAL_ENV and PROJECT_ROOT.

    Outputs:
        Passes when the active environment is not inside the project tree.

    Why:
        Dropbox should sync source/documentation files, while the large
        machine-specific Python environment stays local.
    """
    virtual_env = Path(os.environ["VIRTUAL_ENV"]).expanduser().resolve()
    project_root = PROJECT_ROOT.resolve()

    assert project_root not in virtual_env.parents, (
        f"Virtual environment {virtual_env} is inside the project "
        f"{project_root}. Keep it outside Dropbox."
    )


def test_python_prefix_matches_active_environment() -> None:
    """
    Purpose:
        Verify that Python itself is using the activated environment.

    Inputs:
        sys.prefix and VIRTUAL_ENV.

    Outputs:
        Passes when sys.prefix points to the same environment recorded
        by VIRTUAL_ENV.

    Why:
        sys.prefix is the reliable Python-level environment identifier.
        Unlike sys.executable, it is not confused by the executable's
        symbolic-link target.
    """
    virtual_env = Path(os.environ["VIRTUAL_ENV"]).expanduser().resolve()
    python_prefix = Path(sys.prefix).resolve()

    assert python_prefix == virtual_env, (
        f"Python prefix is {python_prefix}, but the active environment "
        f"is {virtual_env}."
    )


def test_site_packages_belong_to_active_environment() -> None:
    """
    Purpose:
        Confirm that Python is loading packages from the active environment.

    Inputs:
        Python's site-package directories and sys.prefix.

    Outputs:
        Passes when reported site-package directories are inside the
        active virtual environment.

    Why:
        This catches cases where a shell says an environment is active
        but Python is actually importing packages from somewhere else.
    """
    python_prefix = Path(sys.prefix).resolve()
    package_paths = [Path(path).resolve() for path in site.getsitepackages()]

    assert package_paths, "Python did not report any site-packages directory."

    for package_path in package_paths:
        assert python_prefix in package_path.parents, (
            f"Package directory {package_path} is outside the active "
            f"environment {python_prefix}."
        )


def test_required_packages_are_available() -> None:
    """
    Purpose:
        Verify that the main project dependencies are installed.

    Inputs:
        Installed Python packages.

    Outputs:
        Passes when Django, scikit-learn, NumPy, Pandas, joblib, and pytest
        can be imported.

    Why:
        Dependency failures should be caught before Django, ML, and E2E
        tests execute.
    """
    import django
    import joblib
    import numpy
    import pandas
    import pytest
    import sklearn

    assert django.get_version()
    assert joblib.__version__
    assert numpy.__version__
    assert pandas.__version__
    assert pytest.__version__
    assert sklearn.__version__