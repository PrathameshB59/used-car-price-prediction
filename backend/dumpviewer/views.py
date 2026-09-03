from pathlib import Path
import json
import os
import re
import subprocess
import urllib.error
import urllib.request

from django.http import JsonResponse
from django.shortcuts import render


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DUMP_ROOT = PROJECT_ROOT / "dump"

ACTIVITY_LOG = DUMP_ROOT / "ACTIVITY_LOG.md"


# ============================================================
# FILE SYSTEM RULES
# ============================================================

# Runtime/development directories that should not appear
# in the browser.
IGNORED_NAMES = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
}


# Files that can safely be opened as text.
TEXT_EXTENSIONS = {
    ".py",
    ".html",
    ".css",
    ".js",
    ".md",
    ".txt",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".ini",
    ".cfg",
    ".csv",
    ".xml",
    ".sql",
    ".sh",
}


# Never expose these through the file viewer.
# This is important because the project currently contains
# Django configuration and local runtime files.
FORBIDDEN_FILE_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "db.sqlite3",
}


FORBIDDEN_FILE_PATTERNS = {
    "settings.py",
}


# ============================================================
# SECURITY HELPERS
# ============================================================

def is_safe_path(path):
    """
    Make sure a requested path stays inside the project.

    This prevents path traversal such as:

        ../../some-secret-file
    """

    try:
        path.resolve().relative_to(
            PROJECT_ROOT.resolve()
        )

        return True

    except ValueError:
        return False


def should_ignore(path):
    """
    Hide runtime/development directories.
    """

    return any(
        part in IGNORED_NAMES
        for part in path.parts
    )


def is_forbidden_file(path):
    """
    Prevent sensitive files from being displayed.
    """

    if path.name in FORBIDDEN_FILE_NAMES:
        return True

    if path.name in FORBIDDEN_FILE_PATTERNS:
        return True

    return False


# ============================================================
# PROJECT TREE
# ============================================================

def get_project_tree(root=PROJECT_ROOT):
    """
    Scan the project and return files/folders.

    The returned information is used by JavaScript
    to build the visual project explorer.
    """

    items = []

    if not root.exists():
        return items

    for path in sorted(
        root.rglob("*"),
        key=lambda item: str(item).lower(),
    ):

        if should_ignore(path):
            continue

        if not is_safe_path(path):
            continue

        if path.is_file() and is_forbidden_file(path):
            continue

        try:
            relative_path = path.relative_to(
                PROJECT_ROOT
            )

            size = (
                path.stat().st_size
                if path.is_file()
                else 0
            )

            modified = (
                path.stat().st_mtime
            )

        except OSError:
            continue

        items.append(
            {
                "name": path.name,
                "path": str(relative_path),
                "type": (
                    "directory"
                    if path.is_dir()
                    else "file"
                ),
                "size": size,
                "modified": modified,
            }
        )

    return items


def get_dump_tree():
    """
    Return historical development material
    stored under dump/.
    """

    if not DUMP_ROOT.exists():
        return []

    items = []

    for path in sorted(
        DUMP_ROOT.rglob("*"),
        key=lambda item: str(item).lower(),
    ):

        if should_ignore(path):
            continue

        if not is_safe_path(path):
            continue

        try:
            relative_path = path.relative_to(
                DUMP_ROOT
            )

            size = (
                path.stat().st_size
                if path.is_file()
                else 0
            )

            modified = (
                path.stat().st_mtime
            )

        except OSError:
            continue

        items.append(
            {
                "name": path.name,
                "path": str(relative_path),
                "type": (
                    "directory"
                    if path.is_dir()
                    else "file"
                ),
                "size": size,
                "modified": modified,
            }
        )

    return items


# ============================================================
# ACTIVITY LOG
# ============================================================

def read_activity_log():
    """
    Read the local dump activity log.
    """

    if not ACTIVITY_LOG.exists():
        return "No activity log found."

    try:
        return ACTIVITY_LOG.read_text(
            encoding="utf-8"
        )

    except OSError:
        return "Unable to read activity log."


# ============================================================
# GIT
# ============================================================

def run_git(command):
    """
    Execute a Git command locally.

    Git is the authoritative source for:
        branch
        commit
        tags
        remote
        working tree status
        ahead/behind
    """

    try:

        result = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode != 0:
            return ""

        return result.stdout.strip()

    except (
        OSError,
        subprocess.SubprocessError,
    ):
        return ""


def get_git_info():
    """
    Collect current local Git information.
    """

    branch = run_git(
        [
            "git",
            "branch",
            "--show-current",
        ]
    )

    commit = run_git(
        [
            "git",
            "rev-parse",
            "--short",
            "HEAD",
        ]
    )

    full_commit = run_git(
        [
            "git",
            "rev-parse",
            "HEAD",
        ]
    )

    latest_tag = run_git(
        [
            "git",
            "describe",
            "--tags",
            "--abbrev=0",
        ]
    )

    remote_url = run_git(
        [
            "git",
            "remote",
            "get-url",
            "origin",
        ]
    )

    status = run_git(
        [
            "git",
            "status",
            "--short",
        ]
    )

    upstream = run_git(
        [
            "git",
            "rev-parse",
            "--abbrev-ref",
            "--symbolic-full-name",
            "@{u}",
        ]
    )

    ahead_behind = run_git(
        [
            "git",
            "rev-list",
            "--left-right",
            "--count",
            "HEAD...@{u}",
        ]
    )

    ahead = 0
    behind = 0

    if ahead_behind:

        parts = ahead_behind.split()

        if len(parts) == 2:

            try:
                ahead = int(parts[0])
                behind = int(parts[1])

            except ValueError:
                ahead = 0
                behind = 0

    return {
        "branch": branch or "unknown",
        "commit": commit or "unknown",
        "full_commit": full_commit,
        "latest_tag": latest_tag or "none",
        "remote_url": remote_url or "none",
        "upstream": upstream or "none",
        "status": status,
        "clean": not bool(status),
        "ahead": ahead,
        "behind": behind,
    }


def get_git_lfs_info():
    """
    Return Git LFS information.
    """

    output = run_git(
        [
            "git",
            "lfs",
            "ls-files",
        ]
    )

    if not output:
        return {
            "available": False,
            "count": 0,
            "files": [],
        }

    files = []

    for line in output.splitlines():

        line = line.strip()

        if not line:
            continue

        parts = line.split(
            maxsplit=2
        )

        if len(parts) >= 3:

            files.append(
                {
                    "oid": parts[0],
                    "status": parts[1],
                    "path": parts[2],
                }
            )

    return {
        "available": True,
        "count": len(files),
        "files": files,
    }


# ============================================================
# RELEASE HISTORY
# ============================================================

def get_releases():
    """
    Read Git tags and associated commits.

    Git tags are the authoritative rollback mechanism.
    """

    output = run_git(
        [
            "git",
            "for-each-ref",
            "--sort=-creatordate",
            "--format=%(refname:short)|%(creatordate:iso8601)|%(subject)|%(objectname:short)",
            "refs/tags",
        ]
    )

    releases = []

    if not output:
        return releases

    for line in output.splitlines():

        parts = line.split(
            "|",
            maxsplit=3,
        )

        if len(parts) != 4:
            continue

        tag, date, subject, commit = parts

        releases.append(
            {
                "tag": tag,
                "date": date,
                "subject": subject,
                "commit": commit,
            }
        )

    return releases


# ============================================================
# PROJECT STATISTICS
# ============================================================

def get_project_stats():
    """
    Calculate useful project statistics.
    """

    items = get_project_tree()

    files = [
        item
        for item in items
        if item["type"] == "file"
    ]

    folders = [
        item
        for item in items
        if item["type"] == "directory"
    ]

    extension_counts = {}

    for item in files:

        suffix = Path(
            item["name"]
        ).suffix.lower()

        extension_counts[suffix] = (
            extension_counts.get(
                suffix,
                0,
            )
            + 1
        )

    total_size = sum(
        item["size"]
        for item in files
    )

    return {
        "files": len(files),
        "folders": len(folders),
        "python": extension_counts.get(
            ".py",
            0,
        ),
        "html": extension_counts.get(
            ".html",
            0,
        ),
        "css": extension_counts.get(
            ".css",
            0,
        ),
        "javascript": extension_counts.get(
            ".js",
            0,
        ),
        "markdown": extension_counts.get(
            ".md",
            0,
        ),
        "models": extension_counts.get(
            ".joblib",
            0,
        ),
        "notebooks": (
            extension_counts.get(
                ".ipynb",
                0,
            )
            + extension_counts.get(
                ".pdf",
                0,
            )
        ),
        "total_size": total_size,
        "extensions": extension_counts,
    }


# ============================================================
# DOCUMENTATION HEALTH
# ============================================================

def get_documentation_status():
    """
    Check the important root documentation files.
    """

    required_docs = [
        "docs/README.md",
        "docs/CHANGELOG.md",
        "docs/COMMAND.md",
        "docs/EXECUTION_PLAN.md",
        "docs/HOW_TO_USE.md",
        "docs/WHAT_I_LEARNED.md",
    ]

    result = []

    for relative_path in required_docs:

        path = PROJECT_ROOT / relative_path

        result.append(
            {
                "name": Path(
                    relative_path
                ).name,
                "path": relative_path,
                "exists": path.exists(),
                "size": (
                    path.stat().st_size
                    if path.exists()
                    else 0
                ),
            }
        )

    return result


# ============================================================
# PROJECT HEALTH
# ============================================================

def get_health():
    """
    Perform basic application health checks.

    This does not replace Django's full test suite.
    It provides a quick dashboard-level health summary.
    """

    model_path = (
        PROJECT_ROOT
        / "backend"
        / "predictor"
        / "ml"
        / "final_car_price_model.joblib"
    )

    preprocessor_path = (
        PROJECT_ROOT
        / "backend"
        / "predictor"
        / "ml"
        / "final_preprocessor.joblib"
    )

    predictor_path = (
        PROJECT_ROOT
        / "backend"
        / "predictor"
        / "ml"
        / "predictor.py"
    )

    manage_path = (
        PROJECT_ROOT
        / "backend"
        / "manage.py"
    )

    static_css = (
        PROJECT_ROOT
        / "frontend"
        / "static"
        / "predictor"
        / "css"
        / "style.css"
    )

    static_js = (
        PROJECT_ROOT
        / "frontend"
        / "static"
        / "predictor"
        / "js"
        / "script.js"
    )

    git_available = bool(
        run_git(
            [
                "git",
                "--version",
            ]
        )
    )

    checks = [
        {
            "name": "Django project",
            "key": "django",
            "ok": manage_path.exists(),
        },
        {
            "name": "ML model",
            "key": "model",
            "ok": model_path.exists(),
        },
        {
            "name": "Preprocessor",
            "key": "preprocessor",
            "ok": preprocessor_path.exists(),
        },
        {
            "name": "Prediction code",
            "key": "predictor",
            "ok": predictor_path.exists(),
        },
        {
            "name": "Frontend CSS",
            "key": "css",
            "ok": static_css.exists(),
        },
        {
            "name": "Frontend JavaScript",
            "key": "javascript",
            "ok": static_js.exists(),
        },
        {
            "name": "Git",
            "key": "git",
            "ok": git_available,
        },
    ]

    passed = sum(
        1
        for check in checks
        if check["ok"]
    )

    total = len(checks)

    percentage = (
        round(
            passed / total * 100
        )
        if total
        else 0
    )

    return {
        "checks": checks,
        "passed": passed,
        "total": total,
        "percentage": percentage,
    }


# ============================================================
# GITHUB
# ============================================================

def get_github_repository():
    """
    Extract owner/repository from the GitHub origin URL.

    Supports:

        git@github.com:owner/repo.git

    and:

        https://github.com/owner/repo.git
    """

    remote = run_git(
        [
            "git",
            "remote",
            "get-url",
            "origin",
        ]
    )

    if not remote:
        return None

    remote = remote.strip()

    if remote.startswith(
        "git@github.com:"
    ):

        path = remote.split(
            "git@github.com:",
            1,
        )[1]

    elif "github.com/" in remote:

        path = remote.split(
            "github.com/",
            1,
        )[1]

    else:
        return None

    path = path.rstrip("/")

    if path.endswith(".git"):
        path = path[:-4]

    parts = path.split("/")

    if len(parts) != 2:
        return None

    return {
        "owner": parts[0],
        "repo": parts[1],
    }


def get_github_info():
    """
    Query the GitHub REST API.

    If internet access is unavailable,
    the dashboard gracefully falls back to local Git.
    """

    repository = get_github_repository()

    if not repository:

        return {
            "online": False,
            "available": False,
            "message":
                "GitHub remote is not configured.",
        }

    owner = repository["owner"]
    repo = repository["repo"]

    api_url = (
        "https://api.github.com/repos/"
        f"{owner}/{repo}"
    )

    request = urllib.request.Request(
        api_url,
        headers={
            "User-Agent":
                "Used-Car-Price-Prediction-DumpViewer",
            "Accept":
                "application/vnd.github+json",
        },
    )

    token = os.environ.get(
        "GITHUB_TOKEN"
    )

    if token:

        request.add_header(
            "Authorization",
            f"Bearer {token}",
        )

    try:

        with urllib.request.urlopen(
            request,
            timeout=5,
        ) as response:

            data = json.loads(
                response.read().decode(
                    "utf-8"
                )
            )

        return {
            "online": True,
            "available": True,
            "owner": data.get(
                "owner",
                {},
            ).get(
                "login",
                owner,
            ),
            "repo": data.get(
                "name",
                repo,
            ),
            "full_name": data.get(
                "full_name",
                f"{owner}/{repo}",
            ),
            "description": data.get(
                "description"
            ),
            "private": data.get(
                "private",
                False,
            ),
            "default_branch": data.get(
                "default_branch"
            ),
            "stars": data.get(
                "stargazers_count",
                0,
            ),
            "forks": data.get(
                "forks_count",
                0,
            ),
            "open_issues": data.get(
                "open_issues_count",
                0,
            ),
            "html_url": data.get(
                "html_url"
            ),
            "updated_at": data.get(
                "updated_at"
            ),
            "message":
                "GitHub is online.",
        }

    except (
        urllib.error.URLError,
        urllib.error.HTTPError,
        TimeoutError,
        json.JSONDecodeError,
    ) as error:

        return {
            "online": False,
            "available": False,
            "owner": owner,
            "repo": repo,
            "full_name":
                f"{owner}/{repo}",
            "message":
                "GitHub unavailable. "
                "Using local Git data.",
            "error": str(error),
        }


# ============================================================
# DJANGO VIEWS
# ============================================================

def index(request):
    """
    Render the Project Inspector dashboard.
    """

    return render(
        request,
        "dumpviewer/index.html",
        {
            "activity_log":
                read_activity_log(),
        },
    )


def activity_api(request):
    """
    Return dump activity and archive files.
    """

    return JsonResponse(
        {
            "log":
                read_activity_log(),
            "items":
                get_dump_tree(),
        }
    )


def project_api(request):
    """
    Return current project structure.
    """

    return JsonResponse(
        {
            "items":
                get_project_tree(),
        }
    )


def stats_api(request):
    """
    Return project statistics.
    """

    return JsonResponse(
        get_project_stats()
    )


def git_api(request):
    """
    Return local Git information.
    """

    info = get_git_info()

    info["lfs"] = get_git_lfs_info()

    return JsonResponse(info)


def releases_api(request):
    """
    Return Git release/tag history.
    """

    return JsonResponse(
        {
            "releases":
                get_releases(),
        }
    )


def health_api(request):
    """
    Return project health and documentation status.
    """

    return JsonResponse(
        {
            "health":
                get_health(),
            "documentation":
                get_documentation_status(),
        }
    )


def github_api(request):
    """
    Return live GitHub repository information.
    """

    return JsonResponse(
        get_github_info()
    )


def file_api(request):
    """
    Safely return text-file contents.

    Files larger than 1 MB are not displayed.
    Sensitive configuration files are blocked.
    """

    relative_path = request.GET.get(
        "path",
        "",
    ).strip()

    if not relative_path:

        return JsonResponse(
            {
                "error":
                    "No file path supplied.",
            },
            status=400,
        )

    requested_path = (
        PROJECT_ROOT
        / relative_path
    ).resolve()

    if not is_safe_path(
        requested_path
    ):

        return JsonResponse(
            {
                "error":
                    "Invalid file path.",
            },
            status=403,
        )

    if (
        requested_path.is_file()
        and is_forbidden_file(
            requested_path
        )
    ):

        return JsonResponse(
            {
                "error":
                    "This file is protected "
                    "from the browser viewer.",
            },
            status=403,
        )

    if not requested_path.exists():

        return JsonResponse(
            {
                "error":
                    "File not found.",
            },
            status=404,
        )

    if not requested_path.is_file():

        return JsonResponse(
            {
                "error":
                    "Requested path is not a file.",
            },
            status=400,
        )

    if (
        requested_path.suffix.lower()
        not in TEXT_EXTENSIONS
    ):

        return JsonResponse(
            {
                "error":
                    "This file type is not "
                    "displayed by the viewer.",
            },
            status=415,
        )

    max_size = 1024 * 1024

    try:
        file_size = (
            requested_path.stat().st_size
        )

    except OSError:

        return JsonResponse(
            {
                "error":
                    "Unable to inspect file.",
            },
            status=500,
        )

    if file_size > max_size:

        return JsonResponse(
            {
                "error":
                    "File is larger than 1 MB.",
            },
            status=413,
        )

    try:

        content = requested_path.read_text(
            encoding="utf-8"
        )

    except UnicodeDecodeError:

        return JsonResponse(
            {
                "error":
                    "File is not valid UTF-8 text.",
            },
            status=415,
        )

    except OSError:

        return JsonResponse(
            {
                "error":
                    "Unable to read file.",
            },
            status=500,
        )

    return JsonResponse(
        {
            "path":
                relative_path,
            "content":
                content,
            "size":
                file_size,
        }
    )
