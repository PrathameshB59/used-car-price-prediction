"""
AutoValue AI pytest configuration.

Purpose:
    Prepare Python and Django before Django-dependent tests run.

Inputs:
    The repository layout and Django settings module.

Outputs:
    Django is initialized for pytest, and the backend directory is
    available for imports such as ``config`` and ``predictor``.

Why:
    pytest starts from the repository root, while Django normally
    initializes itself through ``manage.py``. The Django test Client
    needs the application registry to be ready before middleware and
    models are imported. Django's test client also uses the host
    ``testserver``, so that host must be allowed during pytest runs.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


# Resolve paths from this file so the test setup works on Linux and Windows.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

# Make Django packages importable when pytest runs from the repository root.
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Tell Django which settings module belongs to this project.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


def pytest_configure() -> None:
    """
    Purpose:
        Initialize Django and configure the test-only host.

    Inputs:
        No arguments.

    Outputs:
        Django settings and installed applications are initialized, and
        Django's default test client host is accepted.

    Why:
        The Django Test Client sends requests using ``testserver``.
        The development settings correctly restrict allowed hosts, but
        pytest needs this separate test-only host so middleware does not
        reject every test request with HTTP 400.
    """
    import django
    from django.conf import settings

    # Add Django's standard test-client host without weakening production
    # host validation in the normal development server.
    if "testserver" not in settings.ALLOWED_HOSTS:
        settings.ALLOWED_HOSTS.append("testserver")

    # Initialize Django's application registry before tests import
    # middleware-dependent components.
    django.setup()