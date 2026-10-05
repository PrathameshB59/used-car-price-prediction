"""
AutoValue AI Test Runner

WHY:
    This runner provides one simple command for the whole project test flow.
    It also keeps the Playwright dependency outside Dropbox by delegating
    browser testing to tests/run_playwright.sh.

WHAT:
    The runner executes:
        1. Django system checks
        2. Pre-startup pytest checks
        3. Preprocessing pytest checks
        4. Starts Django
        5. After-startup pytest checks
        6. Playwright E2E tests

HOW:
    Python controls the complete sequence so the workflow stays understandable
    and remains easier to adapt for Windows as well as Linux.

OUTPUT:
    Each stage reports PASS or FAIL and a Markdown summary is written to
    tests/logs/LATEST.md.

ARCHITECTURE:
    Python test runner
        -> pytest / Django checks
        -> Django server
        -> tests/run_playwright.sh
        -> Playwright browser tests
        -> Markdown test report
"""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


# Resolve the repository from this file instead of assuming a fixed OS path.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

BACKEND_DIR = PROJECT_ROOT / "backend"
MANAGE_PY = BACKEND_DIR / "manage.py"

TESTS_DIR = PROJECT_ROOT / "tests"
PRE_STARTUP_DIR = TESTS_DIR / "pre_startup"
AFTER_STARTUP_DIR = TESTS_DIR / "after_startup"
E2E_DIR = TESTS_DIR / "e2e"
LOG_DIR = TESTS_DIR / "logs"
LOG_FILE = LOG_DIR / "LATEST.md"

# The reusable launcher is the single entry point for browser tests.
PLAYWRIGHT_LAUNCHER = TESTS_DIR / "run_playwright.sh"

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000
SERVER_URL = f"http://{SERVER_HOST}:{SERVER_PORT}/"


def print_header(title: str) -> None:
    """
    Print a readable section heading for one test stage.

    Inputs:
        title: Text shown above the stage.

    Outputs:
        Prints the heading to the terminal.
    """
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def run_command(
    command: list[str],
    *,
    cwd: Path = PROJECT_ROOT,
    env: dict[str, str] | None = None,
) -> tuple[int, str]:
    """
    Run a command and return its exit code and combined output.

    Inputs:
        command: Executable followed by command-line arguments.
        cwd: Directory where the command should run.
        env: Optional environment variables for the command.

    Outputs:
        Tuple containing:
            return_code: Process exit code.
            output: Combined stdout and stderr.
    """
    print(f"[RUN] {' '.join(command)}")

    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    print(completed.stdout)

    return completed.returncode, completed.stdout


def find_python() -> str:
    """
    Return the Python executable running this test system.

    Inputs:
        None.

    Outputs:
        Python executable path.
    """
    return sys.executable


def wait_for_server(timeout_seconds: float = 15.0) -> bool:
    """
    Wait until Django accepts an HTTP connection.

    Inputs:
        timeout_seconds: Maximum amount of time to wait.

    Outputs:
        True when the application returns HTTP 200.
        False when the timeout is reached first.
    """
    deadline = time.monotonic() + timeout_seconds

    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(
                SERVER_URL,
                timeout=1,
            ) as response:
                return response.status == 200
        except Exception:
            # Django needs a short moment to finish startup.
            time.sleep(0.25)

    return False


def is_port_open() -> bool:
    """
    Check whether the expected Django port is already occupied.

    Inputs:
        None.

    Outputs:
        True when something accepts a TCP connection on port 8000.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex(
            (SERVER_HOST, SERVER_PORT)
        ) == 0


def write_report(results: list[tuple[str, bool]]) -> None:
    """
    Write a human-readable Markdown test summary.

    Inputs:
        results: Test-stage names paired with PASS/FAIL values.

    Outputs:
        Updates tests/logs/LATEST.md.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    overall = passed == total

    lines = [
        "# AutoValue AI Test Report",
        "",
        "## Run Information",
        "",
        f"- Python: `{sys.version.split()[0]}`",
        f"- OS: `{os.name}`",
        "- Test mode: deterministic/local",
        "",
        "## Results",
        "",
        "| Stage | Status |",
        "|---|---|",
    ]

    for name, ok in results:
        lines.append(
            f"| {name} | {'PASS' if ok else 'FAIL'} |"
        )

    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"Passed: **{passed}/{total}**",
            "",
            f"Result: **{'PASS' if overall else 'FAIL'}**",
            "",
        ]
    )

    LOG_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> int:
    """
    Run the complete AutoValue AI validation sequence.

    Inputs:
        None. The runner uses the project structure relative to this file.

    Outputs:
        Returns 0 when every stage passes.
        Returns 1 when any required stage fails.
    """
    python = find_python()
    results: list[tuple[str, bool]] = []
    django_process: subprocess.Popen[str] | None = None

    print_header("AutoValue AI Test System")
    print("[INFO] Standard deterministic/local test mode.")

    # This environment is shared with all Python-based test commands.
    python_environment = {
        **os.environ,
        "PYTHONPATH": str(BACKEND_DIR),
        "DJANGO_SETTINGS_MODULE": "config.settings",
    }

    # ------------------------------------------------------------------
    # Stage 1: pre-startup checks
    # ------------------------------------------------------------------
    print_header("1/3  PRE-STARTUP CHECKS")

    return_code, _ = run_command(
        [
            python,
            str(MANAGE_PY),
            "check",
        ],
        cwd=PROJECT_ROOT,
        env=python_environment,
    )

    django_check_ok = return_code == 0
    results.append(
        ("Django system check", django_check_ok)
    )

    print(
        "[PASS] Django system check"
        if django_check_ok
        else "[FAIL] Django system check"
    )

    return_code, _ = run_command(
        [
            python,
            "-m",
            "pytest",
            "-q",
            str(PRE_STARTUP_DIR),
        ],
        cwd=PROJECT_ROOT,
        env=python_environment,
    )

    pre_startup_ok = return_code == 0
    results.append(
        ("Pre-startup pytest", pre_startup_ok)
    )

    print(
        "[PASS] Pre-startup pytest"
        if pre_startup_ok
        else "[FAIL] Pre-startup pytest"
    )

    return_code, _ = run_command(
        [
            python,
            "-m",
            "pytest",
            "-q",
            str(TESTS_DIR / "test_preprocessing.py"),
        ],
        cwd=PROJECT_ROOT,
        env=python_environment,
    )

    preprocessing_ok = return_code == 0
    results.append(
        ("Preprocessing pytest", preprocessing_ok)
    )

    print(
        "[PASS] Preprocessing pytest"
        if preprocessing_ok
        else "[FAIL] Preprocessing pytest"
    )

    # ------------------------------------------------------------------
    # Stage 2: start Django and run backend tests
    # ------------------------------------------------------------------
    print_header("2/3  STARTING DJANGO")

    if is_port_open():
        print(
            "[FAIL] Port 8000 is already in use.\n"
            "       Stop the existing Django server before running "
            "this test runner."
        )

        results.append(
            ("Django server startup", False)
        )

        write_report(results)
        return 1

    print("[RUN] Starting Django server")

    django_process = subprocess.Popen(
        [
            python,
            str(MANAGE_PY),
            "runserver",
            f"{SERVER_HOST}:{SERVER_PORT}",
            "--noreload",
        ],
        cwd=PROJECT_ROOT,
        env=python_environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    server_ok = wait_for_server()
    results.append(
        ("Django server startup", server_ok)
    )

    print(
        f"[PASS] Django responding at {SERVER_URL}"
        if server_ok
        else "[FAIL] Django did not respond"
    )

    if server_ok:
        print_header("AFTER-STARTUP CHECKS")

        return_code, _ = run_command(
            [
                python,
                "-m",
                "pytest",
                "-q",
                str(AFTER_STARTUP_DIR),
            ],
            cwd=PROJECT_ROOT,
            env=python_environment,
        )

        after_startup_ok = return_code == 0
        results.append(
            ("After-startup pytest", after_startup_ok)
        )

        print(
            "[PASS] After-startup pytest"
            if after_startup_ok
            else "[FAIL] After-startup pytest"
        )

        # --------------------------------------------------------------
        # Stage 3: Playwright
        # --------------------------------------------------------------
        print_header("3/3  PLAYWRIGHT E2E")

        if not PLAYWRIGHT_LAUNCHER.exists():
            print(
                "[FAIL] Playwright launcher not found:\n"
                f"       {PLAYWRIGHT_LAUNCHER}"
            )
            playwright_ok = False
        else:
            # The launcher owns the Dropbox workaround.
            # This keeps NODE_PATH and the external Node installation
            # in exactly one place instead of duplicating that logic here.
            return_code, _ = run_command(
                [
                    str(PLAYWRIGHT_LAUNCHER),
                    "test",
                    str(E2E_DIR),
                ],
                cwd=PROJECT_ROOT,
                env=os.environ.copy(),
            )

            playwright_ok = return_code == 0

        results.append(
            ("Playwright E2E", playwright_ok)
        )

        print(
            "[PASS] Playwright E2E"
            if playwright_ok
            else "[FAIL] Playwright E2E"
        )

    # ------------------------------------------------------------------
    # Always stop Django before leaving the runner.
    # ------------------------------------------------------------------
    print("[RUN] Stopping Django server")

    if django_process is not None:
        django_process.terminate()

        try:
            django_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # The graceful shutdown did not finish quickly, so force-stop
            # the child process to avoid leaving a server running.
            django_process.kill()
            django_process.wait()

    print("[PASS] Django server stopped")

    # ------------------------------------------------------------------
    # Final report
    # ------------------------------------------------------------------
    write_report(results)

    print_header("RESULT")

    overall_ok = all(ok for _, ok in results)

    print(
        "RESULT: PASS"
        if overall_ok
        else "RESULT: FAIL"
    )

    print(f"Report: {LOG_FILE}")

    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())