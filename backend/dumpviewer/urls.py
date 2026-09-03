from django.urls import path

from . import views


urlpatterns = [
    # Main dashboard
    path(
        "",
        views.index,
        name="dumpviewer",
    ),

    # Archive / dump information
    path(
        "api/activity/",
        views.activity_api,
        name="dumpviewer-api",
    ),

    # Current project files
    path(
        "api/project/",
        views.project_api,
        name="dumpviewer-project-api",
    ),

    # Project statistics
    path(
        "api/stats/",
        views.stats_api,
        name="dumpviewer-stats-api",
    ),

    # Local Git information
    path(
        "api/git/",
        views.git_api,
        name="dumpviewer-git-api",
    ),

    # Git release/tag history
    path(
        "api/releases/",
        views.releases_api,
        name="dumpviewer-releases-api",
    ),

    # Project health checks
    path(
        "api/health/",
        views.health_api,
        name="dumpviewer-health-api",
    ),

    # Live GitHub repository
    path(
        "api/github/",
        views.github_api,
        name="dumpviewer-github-api",
    ),

    # Read text files
    path(
        "api/file/",
        views.file_api,
        name="dumpviewer-file-api",
    ),
]
