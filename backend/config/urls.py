from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "",
        include("predictor.urls"),
    ),

    path(
        "dump/",
        include("dumpviewer.urls"),
    ),
]
