"""
AutoValue AI — Pre-startup model readiness tests.

Purpose:
    Verify Model A deployment artifacts and determine whether at least
    one complete Model B provider path is configured.

Why:
    Model A is required.

    Model B has a fallback chain:
        1. Primary Gemini
        2. Backup Gemini
        3. Tavily + Backup Gemini

    Therefore, individual optional providers should not all be required.

Inputs:
    Saved Model A artifacts and environment variables.

Outputs:
    Pytest PASS/FAIL results.

Architecture:
    Model A
        ↓
    Required

    Model B
        ↓
    At least one complete usable path
"""


import os
from pathlib import Path

import joblib


# Resolve the project root without depending on the user's home directory.
# This keeps the test portable across Linux and Windows.
PROJECT_ROOT = Path(__file__).resolve().parents[2]


MODEL_PATH = (
    PROJECT_ROOT
    / "backend"
    / "predictor"
    / "ml"
    / "final_car_price_model.joblib"
)


PREPROCESSOR_PATH = (
    PROJECT_ROOT
    / "backend"
    / "predictor"
    / "ml"
    / "final_preprocessor.joblib"
)


def test_model_a_artifacts_exist():
    """
    Purpose:
        Confirm that Model A deployment artifacts exist.

    Inputs:
        Project filesystem.

    Output:
        PASS when both artifacts exist.

    Why:
        Model A cannot run without its saved model and preprocessing
        pipeline.
    """

    assert MODEL_PATH.is_file(), (
        f"Missing Model A artifact: {MODEL_PATH}"
    )

    assert PREPROCESSOR_PATH.is_file(), (
        f"Missing Model A preprocessor: {PREPROCESSOR_PATH}"
    )


def test_model_a_artifacts_can_load():
    """
    Purpose:
        Confirm that both Model A joblib artifacts can be loaded.

    Inputs:
        Saved model and preprocessor files.

    Output:
        PASS when both objects deserialize successfully.

    Why:
        A file can exist but still be corrupted or incompatible with
        the current Python/scikit-learn environment.
    """

    preprocessor = joblib.load(
        PREPROCESSOR_PATH
    )

    model = joblib.load(
        MODEL_PATH
    )

    assert preprocessor is not None
    assert model is not None


def test_model_b_configuration_is_available_or_optional():
    """
    Purpose:
        Check whether a Model B provider is configured without making
        external API access mandatory for deterministic local testing.

    Inputs:
        GEMINI_API_KEY, GEMINI_BACKUP_API_KEY, TAVILY_API_KEY.

    Output:
        PASS when a provider path exists.
        SKIP when no provider is configured.

    Why:
        Model B depends on external services. Normal automated tests must
        remain deterministic and should not fail simply because API keys are
        intentionally absent from the local test environment.
    """
    import os

    primary_gemini_available = bool(os.getenv("GEMINI_API_KEY"))
    backup_gemini_available = bool(os.getenv("GEMINI_BACKUP_API_KEY"))
    tavily_available = bool(os.getenv("TAVILY_API_KEY"))

    # A direct Gemini key is enough for one usable Model B path.
    primary_path_available = primary_gemini_available

    # A backup Gemini key is also independently usable according to the
    # current provider fallback design.
    backup_path_available = backup_gemini_available

    # Tavily is only a complete fallback when backup Gemini is available,
    # because the current implementation uses Tavily for search and then
    # backup Gemini for the final market-analysis response.
    tavily_fallback_available = (
        tavily_available and backup_gemini_available
    )

    usable_path_available = any(
        (
            primary_path_available,
            backup_path_available,
            tavily_fallback_available,
        )
    )

    if not usable_path_available:
        import pytest

        pytest.skip(
            "Model B provider keys are not configured; "
            "deterministic local tests do not require live external APIs."
        )