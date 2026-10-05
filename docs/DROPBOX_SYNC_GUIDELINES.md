# Dropbox Sync Optimization & Development Guidelines

This document outlines the required configuration for team members developing inside the synced `used-car-price-prediction` workspace when using Dropbox or similar cloud syncing services.

---

## 1. Context & Issue Summary

Syncing active development directories over cloud sync daemons causes critical performance bottlenecks and file-lock contention:
* **High File Count Bottleneck:** Folders such as `node_modules/`, `.venv/`, and `.pytest_cache/` generate tens of thousands of tiny files. Syncing these introduces indexing latency, network throttling (rates dropping to 10–40 KB/s), and CPU exhaustion.
* **File Lock & State Corruption:** Active reads and writes during test execution, compilation, or package installs conflict with Dropbox's background file indexer.

---

## 2. Changes Applied (Ignored Directories)

The following local artifacts have been excluded from cloud sync:

| Directory | Purpose | Why Excluded |
| :--- | :--- | :--- |
| `.venv/` | Python Virtual Environment | Contains machine-specific binary wheels and thousands of standard library modules. Reproducible via `requirements.txt`. |
| `node_modules/` | Node.js Dependencies | Holds deep dependency trees (often 15,000+ files). Reproducible via `package.json` / `package-lock.json`. |
| `.pytest_cache/` | Test Execution Cache | Ephemeral cache generated during test runs. Highly volatile. |

---

## 3. Setup Instructions for Team Members

If your local environment runs inside a managed Dropbox path, apply the exclusion rules manually using the Dropbox CLI:

### Linux CLI Setup

Run the following commands from your project root:

```bash
# If using an alternate or custom Dropbox instance
HOME="$HOME/.dropbox-alt" dropbox exclude add .venv
HOME="$HOME/.dropbox-alt" dropbox exclude add node_modules
HOME="$HOME/.dropbox-alt" dropbox exclude add .pytest_cache

# Standard Dropbox instance setup
dropbox exclude add .venv
dropbox exclude add node_modules
dropbox exclude add .pytest_cache
```

Verify your active exclusions:

```bash
dropbox exclude list
```

Expected output:
```text
Excluded: 
.pytest_cache
.venv
node_modules
```

---

## 4. Rebuilding Excluded Environments Locally

Excluding these directories does not delete your code; it only prevents non-essential local build artifacts from congesting team bandwidth. 

When cloning or setting up a clean copy:

### Python Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Node.js Dependencies
```bash
npm install
```

### Running Tests
```bash
pytest
```