---

# 2026-08-19 — ML Preprocessing and Model Decision Update

The Kaggle notebook has progressed beyond initial dataset inspection into preprocessing.

## Current ML Dataset Status

- Dataset: CarDekho Used Car Dataset
- Rows: 15,411
- Raw columns: 14
- Target: `selling_price`
- Missing values: 0
- Completely duplicated rows: 0

## Current Model Features

After removing `selling_price`, `Unnamed: 0`, and `car_name`, the feature matrix contains 11 columns.

Numerical:

- `vehicle_age`
- `km_driven`
- `mileage`
- `engine`
- `max_power`
- `seats`

Categorical:

- `brand`
- `model`
- `seller_type`
- `fuel_type`
- `transmission_type`

## Encoding

Categorical features are converted into numerical representations during preprocessing.

The current preprocessing implementation uses:

- `OneHotEncoder`
- `ColumnTransformer`

The numerical columns are passed through unchanged.

Unknown categorical values are configured to be ignored during transformation.

## Train/Test Split

The dataset has been split using:

- 80% training data
- 20% testing data
- `random_state=42`

Observed shapes:

```text
Training features: (12328, 11)
Testing features:  (3083, 11)
Training target:   (12328,)
Testing target:    (3083,)
```

## Preprocessing Results

The preprocessor is fitted only on the training data and then reused for the testing data.

Observed processed shapes:

```text
Processed training: (12328, 165)
Processed testing:  (3083, 165)
```

This confirms that one-hot encoding expanded the original 11 feature columns into 165 numerical columns.

Important distinction:

```text
Preprocessor = prepares/transforms data
ML model     = learns patterns from prepared data
```

The preprocessor is therefore not the prediction model.

## Current ML Model Decision

The project has decided to use:

```python
RandomForestRegressor
```

as the main regression model for the project.

The current pipeline is:

```text
Raw Dataset
→ Feature/Target Separation
→ Train/Test Split
→ Preprocessing
→ One-Hot Encoding
→ Processed Training Data
→ RandomForestRegressor
→ Training
→ Prediction
→ Evaluation
```

Model training itself has not yet been completed at this documentation update.
