# How to Use

## Current Status

The project is currently in development.

Phase 1, including the Python development environment, has been
completed.

Dataset research and comparison have been completed.

The actual dataset download and inspection are the next steps.

## Development Environment

Operating System:

Linux Mint 22.3 Cinnamon

Python:

3.12.3

Backend:

Django

Frontend:

HTML, CSS, JavaScript

Machine Learning:

Scikit-learn and XGBoost

Dataset:

Kaggle Indian used-car dataset

## Activate the Project

Navigate to the project:

```bash
cd ~/Desktop/'AIML projects/'used-car-price-prediction
{ _ble_edit_exec_gexec__save_lastarg "$@"; } 4>&1 5>&2 &>/dev/null

---

## 2026-08-19 — Notebook Learning Progress

The Kaggle notebook has progressed through the initial dataset-understanding stage.

The dataset currently has 15,411 rows and 14 raw columns. Missing-value inspection returned zero missing values for all columns, and duplicate-row inspection returned zero duplicates.

The current categorical features are:

- `brand` — 32 unique values
- `model` — 120 unique values
- `seller_type` — 3 unique values
- `fuel_type` — 5 unique values
- `transmission_type` — 2 unique values

The current numerical features are:

- `vehicle_age`
- `km_driven`
- `mileage`
- `engine`
- `max_power`
- `seats`

The target is `selling_price`, making this a regression problem.

The notebook is intentionally being developed as a learning workflow: each code block is being understood in terms of what it does, why it is needed, what the output means, and how it affects the final ML model.
