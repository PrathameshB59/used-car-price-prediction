"""
AutoValue AI — After-startup API tests.

Purpose:
    Verify the running Django prediction API using Django's test client.

Why:
    These tests verify the HTTP/API contract without opening a browser.

External services:
    Model B is mocked. Gemini and Tavily are never called during these
    deterministic tests.

Test coverage:
    1. Successful prediction.
    2. Missing required input.
    3. Model B failure while Model A remains available.
"""


import json

import pytest
from django.test import Client


API_URL = "/api/predict/"


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
        The test client lets us test HTTP behavior without starting a
        real browser or development server.
    """
    return Client()


@pytest.fixture
def valid_payload():
    """
    Purpose:
        Provide one valid prediction request.

    Inputs:
        None.

    Output:
        Dictionary matching the frontend API contract.

    Why:
        Keeping valid test data in one fixture makes the tests readable
        and avoids repeating the request payload.
    """
    return {
        "brand": "Maruti Suzuki",
        "model": "Swift",
        "year": 2014,
        "age": 10,
        "km_driven": 60000,
        "transmission": "Manual",
        "owner": "First Owner",
        "fuel_type": "Petrol",
        "seller_type": "Individual",
    }


def post_prediction(client, payload):
    """
    Purpose:
        Send a JSON prediction request to the API.

    Inputs:
        client:
            Django test client.
        payload:
            Prediction request dictionary.

    Output:
        Django HTTP response.

    Why:
        Keeping request construction in one helper makes individual tests
        focus on the behavior they are proving.
    """
    return client.post(
        API_URL,
        data=json.dumps(payload),
        content_type="application/json",
    )


def test_prediction_api_success(
    client,
    valid_payload,
    monkeypatch,
):
    """
    Purpose:
        Verify a successful prediction request.

    Inputs:
        Valid vehicle payload and mocked Model A/Model B results.

    Output:
        HTTP 200 with success response structure.

    Why:
        We verify the API contract rather than exact model prices.
        Exact prices belong to ML/model-specific tests.
    """
    from predictor import api_views

    monkeypatch.setattr(
        api_views,
        "predict_car_price",
        lambda car_data: 323659.0,
    )

    monkeypatch.setattr(
        api_views,
        "predict_with_gemini",
        lambda car_data: {
            "estimated_price": 335000,
            "confidence": "Medium",
            "reasoning": "Mock market evidence.",
            "search_method": "test_mock",
            "sources": [],
        },
    )

    response = post_prediction(
        client,
        valid_payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["model_a"] is not None
    assert data["model_b"] is not None
    assert data["comparison"] is not None

    assert isinstance(
        data["model_a"],
        (int, float),
    )

    assert isinstance(
        data["model_b"],
        dict,
    )

    assert "estimated_price" in data["model_b"]


def test_prediction_api_rejects_missing_required_field(
    client,
    valid_payload,
):
    """
    Purpose:
        Verify that a request missing a required field is rejected.

    Inputs:
        Otherwise valid payload with brand removed.

    Output:
        HTTP 400 and an error response.

    Why:
        API validation prevents incomplete data from reaching Model A
        and Model B.
    """
    payload = valid_payload.copy()
    payload.pop("brand")

    response = post_prediction(
        client,
        payload,
    )

    assert response.status_code == 400

    data = response.json()

    assert "error" in data


def test_prediction_api_handles_model_b_failure(
    client,
    valid_payload,
    monkeypatch,
):
    """
    Purpose:
        Verify partial-failure behavior.

    Inputs:
        Valid request, successful Model A, failing Model B.

    Output:
        HTTP 200 with partial status and Model A still available.

    Why:
        Model B depends on external services. Its failure must not destroy
        a valid Model A valuation.
    """
    from predictor import api_views

    monkeypatch.setattr(
        api_views,
        "predict_car_price",
        lambda car_data: 323659.0,
    )

    def failing_model_b(car_data):
        raise RuntimeError(
            "Mock Model B provider failure"
        )

    monkeypatch.setattr(
        api_views,
        "predict_with_gemini",
        failing_model_b,
    )

    response = post_prediction(
        client,
        valid_payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "partial"

    # Model A must remain usable when Model B fails.
    assert data["model_a"] == 323659.0

    assert data["model_b"] is None
    assert data["model_b_error"] is not None