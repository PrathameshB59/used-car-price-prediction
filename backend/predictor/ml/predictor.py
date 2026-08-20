from pathlib import Path

import joblib
import pandas as pd


# Get the directory containing this file
BASE_DIR = Path(__file__).resolve().parent


# Define paths to the saved ML files
MODEL_PATH = BASE_DIR / "car_price_model.joblib"
PREPROCESSOR_PATH = BASE_DIR / "preprocessor.joblib"


# Load the trained model
model = joblib.load(MODEL_PATH)


# Load the preprocessor
preprocessor = joblib.load(PREPROCESSOR_PATH)


def predict_car_price(car_data):
    """
    Predict the selling price of a car.

    Parameters:
        car_data (dict): Dictionary containing car features.

    Returns:
        float: Predicted selling price.
    """

    # Convert the dictionary into a one-row DataFrame
    input_df = pd.DataFrame([car_data])

    # Apply the same preprocessing used during training
    processed_data = preprocessor.transform(input_df)

    # Make prediction
    prediction = model.predict(processed_data)

    # Return the first prediction as a float
    return float(prediction[0])
