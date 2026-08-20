from datetime import date

from django.shortcuts import render

from .ml.predictor import predict_car_price


def home(request):
    """
    Render the Used Car Price Prediction homepage and
    process car price prediction requests.
    """

    prediction = None
    error = None

    if request.method == "POST":
        try:
            # Get values from the submitted form
            brand = request.POST.get("brand")
            model = request.POST.get("model")
            year = int(request.POST.get("year"))
            km_driven = float(request.POST.get("km_driven"))
            seller_type = request.POST.get("seller_type")
            fuel_type = request.POST.get("fuel_type")
            transmission_type = request.POST.get("transmission_type")
            mileage = float(request.POST.get("mileage"))
            engine = float(request.POST.get("engine"))
            max_power = float(request.POST.get("max_power"))
            seats = float(request.POST.get("seats"))

            # Convert manufacturing year into vehicle age
            current_year = date.today().year
            vehicle_age = current_year - year

            # Create data in the exact format expected by the ML preprocessor
            car_data = {
                "brand": brand,
                "model": model,
                "vehicle_age": vehicle_age,
                "km_driven": km_driven,
                "seller_type": seller_type,
                "fuel_type": fuel_type,
                "transmission_type": transmission_type,
                "mileage": mileage,
                "engine": engine,
                "max_power": max_power,
                "seats": seats,
            }

            # Get prediction from the trained ML model
            prediction = predict_car_price(car_data)

        except (ValueError, TypeError) as e:
            error = f"Please enter valid car details. {e}"

    context = {
        "prediction": prediction,
        "error": error,
    }

    return render(request, "predictor/index.html", context)
