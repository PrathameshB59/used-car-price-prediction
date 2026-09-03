from pathlib import Path

import joblib
import pandas as pd


# Get the directory containing this file
BASE_DIR = Path(__file__).resolve().parent


# Paths to the final V2 ML artifacts
MODEL_PATH = BASE_DIR / "final_car_price_model.joblib"
PREPROCESSOR_PATH = BASE_DIR / "final_preprocessor.joblib"


# Load the final trained model
model = joblib.load(MODEL_PATH)


# Load the preprocessing pipeline used during training
preprocessor = joblib.load(PREPROCESSOR_PATH)


def predict_car_price(car_data):
    """
    Predict the selling price of a used car.

    Parameters:
        car_data (dict):
            Dictionary containing the 8 features expected
            by the final V2 ML model.

    Returns:
        float:
            Predicted selling price.
    """

    # Convert the dictionary into a one-row DataFrame.
    # The DataFrame structure must match the training features.
    input_df = pd.DataFrame([car_data])

    # Apply the same preprocessing used during model training.
    processed_data = preprocessor.transform(input_df)

    # Generate the price prediction.
    prediction = model.predict(processed_data)

    # Return the first prediction as a normal Python float.
    return float(prediction[0])
