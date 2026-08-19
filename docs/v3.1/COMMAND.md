---

## 2026-08-19 — Preprocessing and Train/Test Commands

### Create the preprocessing pipeline

```python
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_columns
        )
    ],
    remainder="passthrough"
)
```

`ColumnTransformer` lets different groups of columns receive different preprocessing.

`OneHotEncoder(handle_unknown="ignore")` converts categorical values into binary columns and avoids an error when a new category appears during testing or prediction.

`remainder="passthrough"` keeps the numerical columns unchanged.

### Split the dataset

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)
```

`test_size=0.20` reserves 20% for testing.

`random_state=42` makes the split reproducible.

### Fit and transform training data

```python
X_train_processed = preprocessor.fit_transform(X_train)
```

`fit_transform()` performs two operations:

1. `fit()` learns preprocessing information from the training data.
2. `transform()` converts the training data using that learned information.

### Transform testing data

```python
X_test_processed = preprocessor.transform(X_test)
```

The testing data uses the already-fitted preprocessor.

We do not fit the preprocessor again on the test data.

This prevents test-set information from leaking into training.

### Observed processed shapes

```text
Processed training shape: (12328, 165)
Processed testing shape:  (3083, 165)
```

### Main ML model

The selected model is:

```python
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(
    random_state=42
)
```

The next step is to train this model using the processed training data.
