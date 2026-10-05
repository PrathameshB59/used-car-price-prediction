#!/usr/bin/env bash
#
# AutoValue AI — Playwright launcher
#
# Purpose:
#   Run Playwright while keeping Node dependencies outside Dropbox.
#
# Why:
#   Dropbox's synced project path does not reliably expose the external
#   Node dependency tree through normal Node module resolution. NODE_PATH
#   provides that dependency location without copying node_modules into
#   the project.
#
# Inputs:
#   Playwright arguments, for example:
#       test tests/e2e
#
# Output:
#   Playwright output and the same exit status returned by Playwright.
#

set -euo pipefail

# Keep the large dependency tree outside Dropbox.
PLAYWRIGHT_ROOT="${HOME}/.local/share/autovalue-ai-node/node_modules"

# Tell Node where the external packages are installed.
export NODE_PATH="${PLAYWRIGHT_ROOT}"

# Fail with a useful message if the external installation disappeared.
if [[ ! -x "${PLAYWRIGHT_ROOT}/.bin/playwright" ]]; then
    echo "ERROR: Playwright installation not found:"
    echo "  ${PLAYWRIGHT_ROOT}"
    exit 1
fi

# Run Playwright and forward every argument supplied to this launcher.
exec "${PLAYWRIGHT_ROOT}/.bin/playwright" "$@"