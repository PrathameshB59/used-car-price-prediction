from django.shortcuts import render


def home(request):
    """
    Render the Used Car Price Prediction homepage.
    """
    return render(request, "predictor/index.html")
