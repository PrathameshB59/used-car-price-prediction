from django.shortcuts import render

from .ml.predictor import predict_car_price


def get_field_value(post_data, field_name):
    """
    Get a normal form value.

    If the user selected 'Other / Unknown',
    use the custom value entered in the text box.
    """

    value = post_data.get(field_name)

    if value == "Other / Unknown":

        other_value = post_data.get(
            f"{field_name}_other"
        )

        if other_value:
            return other_value.strip()

    return value


def home(request):
    """
    Render the Used Car Price Prediction homepage
    and process prediction requests.
    """

    prediction = None
    error = None

    if request.method == "POST":

        try:

            # ---------------------------------
            # Get categorical values
            # ---------------------------------

            brand = get_field_value(
                request.POST,
                "brand"
            )

            model = get_field_value(
                request.POST,
                "model"
            )

            transmission = get_field_value(
                request.POST,
                "transmission"
            )

            owner = get_field_value(
                request.POST,
                "owner"
            )

            fuel_type = get_field_value(
                request.POST,
                "fuel_type"
            )

            seller_type = get_field_value(
                request.POST,
                "seller_type"
            )

            # ---------------------------------
            # Get numerical values
            # ---------------------------------

            year = int(
                request.POST.get("year")
            )

            age = int(
                request.POST.get("age")
            )

            km_driven = float(
                request.POST.get("km_driven")
            )


            # ---------------------------------
            # Create ML input dictionary
            # ---------------------------------

            car_data = {

                "Brand": brand,

                "model": model,

                "Year": year,

                "Age": age,

                "kmDriven": km_driven,

                "Transmission": transmission,

                "Owner": owner,

                "FuelType": fuel_type,

            }


            # ---------------------------------
            # Predict
            # ---------------------------------

            prediction = predict_car_price(
                car_data
            )


        except (ValueError, TypeError) as e:

            error = (
                "Please enter valid car details. "
                f"{e}"
            )


    context = {

        "prediction": prediction,

        "error": error,

    }


    return render(
        request,
        "predictor/index.html",
        context
    )
