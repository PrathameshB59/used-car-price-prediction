from django.shortcuts import render

from .ml.predictor import predict_car_price
from .ml.model_b.gemini_predictor import predict_with_gemini
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def home(request):
    """
    Render the Used Car Price Prediction homepage.

    Two independent prediction systems are used:
    ...
    """
    """
    Render the Used Car Price Prediction homepage.

    Two independent prediction systems are used:

    Model A:
        Local trained Machine Learning model.

    Model B:
        Gemini + internet market research,
        with Tavily as the search fallback.

    Both predictions are returned to the frontend
    so they can be compared.
    """

    model_a = None
    model_b = None

    model_a_error = None
    model_b_error = None

    comparison = None

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
            # Common input dictionary
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
            # Model B input
            #
            # Model B uses slightly different
            # field names.
            # ---------------------------------

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

            # =================================
            # MODEL A
            # =================================

            try:

                model_a = predict_car_price(
                    car_data
                )

            except Exception as e:

                model_a_error = str(e)

            # =================================
            # MODEL B
            # =================================

            try:

                model_b = predict_with_gemini(
                    model_b_car_data
                )

            except Exception as e:

                model_b_error = str(e)

            # =================================
            # COMPARISON
            # =================================

            if (
                model_a is not None
                and model_b is not None
                and model_b.get("estimated_price") is not None
            ):

                model_b_price = float(
                    model_b["estimated_price"]
                )

                difference = abs(
                    float(model_a) - model_b_price
                )

                if model_a != 0:

                    difference_percent = (
                        difference
                        / float(model_a)
                    ) * 100

                else:

                    difference_percent = 0

                if model_a > model_b_price:

                    higher_model = "Model A"

                elif model_b_price > model_a:

                    higher_model = "Model B"

                else:

                    higher_model = "Both models agree"

                comparison = {

                    "difference": difference,

                    "difference_percent":
                        difference_percent,

                    "higher_model":
                        higher_model,

                }

        except (ValueError, TypeError) as e:

            model_a_error = (
                "Please enter valid car details. "
                f"{e}"
            )

    context = {

        "model_a": model_a,

        "model_b": model_b,

        "model_a_error": model_a_error,

        "model_b_error": model_b_error,

        "comparison": comparison,

    }

    return render(
        request,
        "predictor/index.html",
        context
    )
