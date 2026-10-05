"""
AutoValue AI — After-startup smoke tests.

Purpose:
    Verify that the Django application responds after startup.

Why:
    API tests prove the prediction endpoint. This smoke test proves the
    application itself is reachable.

Scope:
    We intentionally do not test every CSS/JS/static asset here.
    Browser-level asset and route checks belong to Playwright.
"""


import pytest
from django.test import Client


@pytest.fixture
def client():
    """
    Purpose:
        Provide a Django test client.

    Inputs:
        None.

    Output:
        Django Client instance.

    Why:
        The Django test client lets us verify the application without
        requiring a real browser.
    """
    return Client()


def test_homepage_responds(client):
    """
    Purpose:
        Verify that the main application page responds successfully.

    Inputs:
        Django test client.

    Output:
        HTTP 200 response containing the application shell.

    Why:
        This is the smallest useful test answering:
        "Is Django serving AutoValue AI?"
    """
    response = client.get("/")

    assert response.status_code == 200
    assert response.content


def test_homepage_contains_application_mount_point(client):
    """
    Purpose:
        Verify that the frontend application mount point exists.

    Inputs:
        Django test client.

    Output:
        PASS when the HTML contains the #app container.

    Why:
        The frontend router renders its page fragments into this element.
    """
    response = client.get("/")

    content = response.content.decode(
        "utf-8",
        errors="replace",
    )

    assert 'id="app"' in content