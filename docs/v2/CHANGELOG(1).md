# Changelog

All important project changes are recorded here.

## [Unreleased]

### Added

- Initial project structure.
- Documentation structure under `docs/`.
- `README.md`.
- `CHANGELOG.md`.
- `COMMAND.md`.
- `HOW_TO_USE.md`.
- `EXECUTION_PLAN.md`.
- Python virtual environment.
- Initial Python dependency configuration.
- `.gitignore`.
- Backend and frontend directory structure.
- Tests directory.

### Environment

- Operating system: Linux Mint 22.3 Cinnamon.
- Python version: 3.12.3.
- Virtual environment: `.venv`.
- pip successfully configured inside the project virtual environment.
- Core ML, data analysis, Django, Jupyter, and testing packages installed.
- Core package import verification completed successfully.

### Project Decisions

- Project topic: Used Car Price Prediction.
- Target market: Indian used-car market.
- Application type: Localhost web application.
- Backend: Django.
- Frontend: HTML, CSS, JavaScript.
- ML task: Regression.
- Dataset source: Kaggle.
- Preferred dataset category: Indian used-car dataset.

### Changed

- Moved the project to its permanent location:
  `~/Desktop/AIML projects/used-car-price-prediction`.
- Recreated the Python virtual environment after the project move.
- Updated project documentation after completing environment setup.

### Fixed

- Fixed the broken virtual environment caused by moving the project
  directory after the original `.venv` was created.

### Dataset Selection

- Researched Indian used-car datasets.
- Compared candidate datasets based on size, features, target variable,
  usefulness for ML, and suitability for a localhost prediction system.
- Identified a preferred Indian used-car dataset candidate.
- Final dataset inspection is still pending.

### Removed

- Nothing yet.

---

## 2026-08-18 — Django Migration

### Changed

- Replaced Flask with Django as the web framework.
- Django 6.1 installed inside the project virtual environment.
- Django project created using the project name `config`.
- Django project located under `backend/`.
- Django application `predictor` created.
- ML-specific code directory created at `backend/predictor/ml/`.
- Frontend structure prepared for Django templates and static files.
- Planned localhost development address changed from port 5000 to port 8000.

### Fixed

- Removed accidentally created nested `backend/backend/` directory.
- Corrected the Django ML directory location.
- Corrected frontend migration to use Django template/static-file structure.

### Development Status

- Django environment: completed.
- Django project structure: created.
- Django predictor application: created.
- Django configuration: not yet completed.
- First localhost Django page: not yet implemented.
- Git repository: not yet initialized.

---

## 2026-08-19 — Git Repository Milestone

### Added

- Initialized local Git repository.
- Renamed initial branch from `master` to `main`.
- Configured Git user identity.
- Added project `.gitignore`.
- Verified virtual environment is excluded.
- Verified SQLite database is excluded.
- Verified Python cache files are excluded.
- Staged the initial project source, documentation, frontend,
  backend, tests, and project configuration files.

### Git Status

The first project commit is ready to be created.

### Repository Policy

The project will use local Git version control throughout development.

GitHub remote setup will be performed separately if required.

---

## 2026-08-19 — ML Dataset Understanding Milestone

### Added

- Loaded the CarDekho Used Car Dataset in the Kaggle training notebook.
- Documented the dataset dimensions: 15,411 rows and 14 columns.
- Inspected all column data types.
- Checked missing values.
- Checked duplicate records.
- Calculated numerical summary statistics.
- Inspected categorical feature distributions.
- Calculated categorical feature cardinality.
- Inspected the `selling_price` target distribution.
- Calculated selling-price percentiles.
- Inspected high-priced vehicles.
- Separated model features `X` from target `y`.
- Documented the distinction between preprocessing/encoding and model training.

### Dataset Findings

- Missing values: 0 across all inspected columns.
- Completely duplicated rows: 0.
- `brand`: 32 unique values.
- `model`: 120 unique values.
- `seller_type`: 3 unique values.
- `fuel_type`: 5 unique values.
- `transmission_type`: 2 unique values.

### Learning Updates

- Clarified that `int64` means a 64-bit integer representation.
- Clarified that `np` is the conventional alias for NumPy.
- Learned that `value_counts()` counts category frequency.
- Learned that `nunique()` counts distinct values.
- Learned how `select_dtypes()` separates numerical and categorical columns.
- Learned how `quantile()` is used to inspect percentiles.
- Learned how `sort_values()` and `head()` can be combined to inspect extreme observations.
- Clarified that encoding is preprocessing and does not itself mean the model has learned.

### Preprocessing Status

Categorical cardinality has been inspected before encoding. The exact encoding/preprocessing strategy is the next ML decision point.

### Documentation Policy

Existing documentation sections are intentionally preserved. Progress is appended as dated updates so the history of the learning process remains visible.
