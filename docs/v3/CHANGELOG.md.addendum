---

## 2026-08-19 — ML Preprocessing and Random Forest Milestone

### Added

- Built a preprocessing pipeline using `ColumnTransformer`.
- Added `OneHotEncoder` for categorical features.
- Configured unknown categories to be ignored during transformation.
- Kept numerical features as pass-through features.
- Split the dataset into training and testing sets.
- Used an 80/20 train-test split with `random_state=42`.
- Fitted preprocessing only on the training data.
- Transformed both training and testing features using the same fitted preprocessor.
- Verified processed feature shapes.

### Verified Results

```text
Training features: (12328, 11)
Testing features:  (3083, 11)

Processed training: (12328, 165)
Processed testing:  (3083, 165)
```

### Model Decision

- Confirmed `RandomForestRegressor` as the main ML algorithm for this project.
- Clarified that the preprocessor is not the ML prediction model.
- Clarified the distinction between preprocessing and model training.

### Current Status

Preprocessing and train/test preparation are complete.

Random Forest training, prediction, and evaluation are the next ML steps.
