"""
AutoValue AI — Pre-startup project health tests.

Purpose:
    Verify the Django project and required frontend structure before
    starting the development server.

Why:
    These checks catch broken project structure early.

Inputs:
    Project files and Django configuration.

Outputs:
    Pytest PASS/FAIL results.
"""


from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_required_project_paths_exist():
    """
    Purpose:
        Verify important application directories/files exist.

    Inputs:
        Project filesystem.

    Output:
        PASS when required paths are present.

    Why:
        Missing application structure should be detected before startup.
    """
    required_paths = [
        PROJECT_ROOT / "backend" / "manage.py",
        PROJECT_ROOT / "backend" / "predictor",
        PROJECT_ROOT / "frontend" / "static" / "predictor",
        PROJECT_ROOT / "frontend" / "templates" / "predictor",
        PROJECT_ROOT / "requirements.txt",
    ]

    missing = [
        str(path)
        for path in required_paths
        if not path.exists()
    ]

    assert not missing, (
        "Required project paths are missing:\n"
        + "\n".join(missing)
    )


def test_django_configuration():
    """
    Purpose:
        Load Django and execute its system checks.

    Inputs:
        Project Django settings.

    Output:
        PASS when Django reports no system-check errors.

    Why:
        This catches configuration, URL, middleware, and app problems
        before the development server is started.
    """
    import os

    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "config.settings",
    )

    import django
    from django.core.management import call_command

    django.setup()

    # Django's own check framework is more reliable than manually
    # inspecting settings.py because it validates the actual application.
    call_command("check", verbosity=0)