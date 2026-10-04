"""
AutoValue AI - Prediction API
=============================

Purpose:
    Provide a JSON endpoint that connects the redesigned frontend
    to the existing Django prediction functions.

Architecture:
    Frontend JavaScript
        ↓
    POST /api/predict/
        ↓
    Model A + Model B
        ↓
    comparison
        ↓
    JSON response

Important:
    This file does not contain ML implementation.
    It reuses the existing Model A and Model B functions.
"""

import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .ml.predictor import predict_car_price
from .ml.model_b.gemini_predictor import predict_with_gemini


def _error_response(message, status=400):
    """
    Purpose:
        Create a consistent JSON error response.

    Inputs:
        message: Human-readable error description.
        status: HTTP status code.

    Output:
        JsonResponse containing the error message.
    """
    return JsonResponse(
        {
            "status": "error",
            "error": message,
        },
        status=status,
    )


def _calculate_comparison(model_a, model_b):
    """
    Purpose:
        Compare the two available price estimates.

    Inputs:
        model_a: Model A numeric prediction.
        model_b: Model B prediction dictionary.

    Output:
        Dictionary containing difference information.

    Why:
        Keeping comparison calculation on the backend means the
        frontend only displays already-validated results.
    """
    if model_a is None or not model_b:
        return None

    model_b_price = model_b.get("estimated_price")

    if model_b_price is None:
        return None

    difference = abs(float(model_a) - float(model_b_price))

    if float(model_a) == 0:
        difference_percent = 0.0
    else:
        difference_percent = (
            difference / abs(float(model_a))
        ) * 100

    if float(model_a) > float(model_b_price):
        higher_model = "Model A"
    elif float(model_b_price) > float(model_a):
        higher_model = "Model B"
    else:
        higher_model = "Equal"

    return {
        "difference": round(difference, 2),
        "difference_percent": round(difference_percent, 2),
        "higher_model": higher_model,
    }


@require_POST
def api_predict(request):
    """
    Purpose:
        Receive vehicle information from the frontend and run
        both existing valuation models.

    Inputs:
        JSON request body containing the vehicle fields.

    Output:
        JSON response containing Model A, Model B, comparison,
        and separate error information when a model fails.

    Security:
        Django's normal CSRF protection remains enabled.
        The frontend must send the CSRF token with the request.
    """

    # ----------------------------------------------------------
    # 1. Parse the JSON request
    # ----------------------------------------------------------

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return _error_response(
            "Request body must contain valid JSON."
        )

    if not isinstance(payload, dict):
        return _error_response(
            "Request body must be a JSON object."
        )

    # ----------------------------------------------------------
    # 2. Read and normalize frontend fields
    # ----------------------------------------------------------

    brand = str(payload.get("brand", "")).strip()
    model = str(payload.get("model", "")).strip()

    year = payload.get("year")
    age = payload.get("age")
    km_driven = payload.get("km_driven")

    transmission = str(
        payload.get("transmission", "")
    ).strip()

    owner = str(
        payload.get("owner", "")
    ).strip()

    fuel_type = str(
        payload.get("fuel_type", "")
    ).strip()

    seller_type = str(
        payload.get("seller_type", "")
    ).strip()

    # ----------------------------------------------------------
    # 3. Validate required values
    # ----------------------------------------------------------

    required_values = {
        "brand": brand,
        "model": model,
        "year": year,
        "age": age,
        "km_driven": km_driven,
        "transmission": transmission,
        "owner": owner,
        "fuel_type": fuel_type,
        "seller_type": seller_type,
    }

    missing_fields = [
        field
        for field, value in required_values.items()
        if value is None or value == ""
    ]

    if missing_fields:
        return _error_response(
            "Missing required fields.",
            status=400,
        )

    # ----------------------------------------------------------
    # 4. Convert numeric values
    # ----------------------------------------------------------

    try:
        year = int(year)
        age = int(age)
        km_driven = float(km_driven)
    except (TypeError, ValueError):
        return _error_response(
            "Year, age and kilometres driven must be numeric.",
            status=400,
        )

    # ----------------------------------------------------------
    # 5. Build Model A input
    #
    # IMPORTANT:
    # Seller Type is deliberately excluded.
    # Model A has exactly eight features.
    # ----------------------------------------------------------

    model_a_car_data = {
        "Brand": brand,
        "model": model,
        "Year": year,
        "Age": age,
        "kmDriven": km_driven,
        "Transmission": transmission,
        "Owner": owner,
        "FuelType": fuel_type,
    }

    # ----------------------------------------------------------
    # 6. Build Model B input
    #
    # Model B uses the frontend-friendly lowercase contract.
    # Seller Type is included here.
    # ----------------------------------------------------------

    model_b_car_data = {
        "brand": brand,
        "model": model,
        "year": year,
        "age": age,
        "km_driven": km_driven,
        "transmission": transmission,
        "owner": owner,
        "fuel_type": fuel_type,
        "seller_type": seller_type,
    }

    # ----------------------------------------------------------
    # 7. Run Model A independently
    # ----------------------------------------------------------

    model_a = None
    model_a_error = None

    try:
        model_a = float(
            predict_car_price(model_a_car_data)
        )
    except Exception as exc:
        # We keep Model B running even when Model A fails.
        model_a_error = str(exc)

    # ----------------------------------------------------------
    # 8. Run Model B independently
    # ----------------------------------------------------------

    model_b = None
    model_b_error = None

    try:
        model_b = predict_with_gemini(
            model_b_car_data
        )
    except Exception as exc:
        # We keep the API response useful even if external
        # Model B services fail.
        model_b_error = str(exc)

    # ----------------------------------------------------------
    # 9. Determine overall API status
    # ----------------------------------------------------------

    if model_a is not None and model_b is not None:
        status = "success"
    elif model_a is not None or model_b is not None:
        status = "partial"
    else:
        status = "error"

    # ----------------------------------------------------------
    # 10. Compare the two predictions when possible
    # ----------------------------------------------------------

    comparison = _calculate_comparison(
        model_a,
        model_b,
    )

    # ----------------------------------------------------------
    # 11. Build the JSON response
    # ----------------------------------------------------------

    response_data = {
        "status": status,

        "car": {
            "brand": brand,
            "model": model,
            "year": year,
            "age": age,
            "km_driven": km_driven,
            "transmission": transmission,
            "owner": owner,
            "fuel_type": fuel_type,
            "seller_type": seller_type,
        },

        "model_a": model_a,
        "model_a_error": model_a_error,

        "model_b": model_b,
        "model_b_error": model_b_error,

        "comparison": comparison,
    }

    # Return 200 for success/partial because the endpoint itself
    # successfully processed the request. The response status
    # tells the frontend whether one or both models failed.
    return JsonResponse(response_data, status=200)
