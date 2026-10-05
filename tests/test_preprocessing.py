"""
AutoValue AI — Model A preprocessing integration tests.

Purpose:
    Verify that the saved preprocessing pipeline and Random Forest
    model can be loaded together and produce a valid prediction.

Why:
    Model A is deployed through saved joblib artifacts. This test
    protects that deployment contract without retraining the model.

Inputs:
    One fixed representative vehicle record using the exact eight
    Model A features.

Outputs:
    Pytest PASS/FAIL results.

Architecture:
    Test input
        ↓
    final_preprocessor.joblib
        ↓
    final_car_price_model.joblib
        ↓
    valid price
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd


# Resolve paths from this test file instead of hard-coding a user's
# home directory. This keeps the test portable across Linux and Windows.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

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


def sample_car_data() -> dict:
    """
    Purpose:
        Return one representative vehicle using the Model A contract.

    Inputs:
        None.

    Output:
        Dictionary containing exactly the eight Model A features.

    Why:
        Keeping the test input in one helper makes the test easy to
        understand and avoids repeating the same data.
    """
    return {
        "Brand": "Maruti Suzuki",
        "model": "Swift",
        "Year": 2014,
        "Age": 10,
        "kmDriven": 60000,
        "Transmission": "Manual",
        "Owner": "First Owner",
        "FuelType": "Petrol",
    }


def test_model_artifacts_exist():
    """
    Purpose:
        Confirm that both deployment artifacts exist.

    Inputs:
        None.

    Output:
        PASS when both files exist; otherwise pytest FAIL.

    Why:
        A missing artifact means Django cannot perform Model A
        prediction even if the Python code itself is correct.
    """
    assert MODEL_PATH.is_file(), f"Missing model: {MODEL_PATH}"
    assert PREPROCESSOR_PATH.is_file(), (
        f"Missing preprocessor: {PREPROCESSOR_PATH}"
    )


def test_model_and_preprocessor_load():
    """
    Purpose:
        Verify that both joblib artifacts can be deserialized.

    Inputs:
        Saved model and preprocessor paths.

    Output:
        PASS when both objects load successfully.

    Why:
        A file can exist but still be corrupted or incompatible with
        the installed Python/scikit-learn environment.
    """
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    model = joblib.load(MODEL_PATH)

    assert preprocessor is not None
    assert model is not None


def test_model_a_produces_valid_prediction():
    """
    Purpose:
        Run one complete Model A prediction through the saved artifacts.

    Inputs:
        Representative car data.

    Output:
        A finite positive numeric price.

    Why:
        This verifies the actual deployment path instead of only
        checking that the files exist.
    """
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    model = joblib.load(MODEL_PATH)

    car_data = sample_car_data()

    # Convert the dictionary to a one-row DataFrame because the saved
    # preprocessing pipeline expects tabular feature names.
    input_df = pd.DataFrame([car_data])

    transformed_data = preprocessor.transform(input_df)
    prediction = model.predict(transformed_data)[0]

    assert isinstance(prediction, (int, float, np.integer, np.floating))
    assert np.isfinite(prediction)
    assert prediction > 0