from django.urls import path

from . import views
from .api_views import api_predict


urlpatterns = [
    path("", views.home, name="home"),
    path(
        "api/predict/",
        api_predict,
        name="api_predict",
    ),
]
