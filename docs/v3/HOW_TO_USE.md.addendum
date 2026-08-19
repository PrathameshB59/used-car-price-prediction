---

## 2026-08-19 — Current ML Notebook Status

The notebook has moved from dataset inspection into preprocessing and train/test preparation.

### Preprocessing

The current preprocessing uses:

- `ColumnTransformer`
- `OneHotEncoder`
- `remainder="passthrough"`

Categorical features:

```text
brand
model
seller_type
fuel_type
transmission_type
```

Numerical features:

```text
vehicle_age
km_driven
mileage
engine
max_power
seats
```

### Train/Test Split

The dataset is split into:

```text
80% training
20% testing
```

with:

```python
random_state=42
```

Observed:

```text
X_train: (12328, 11)
X_test:  (3083, 11)
y_train: (12328,)
y_test:  (3083,)
```

### Preprocessed Data

After one-hot encoding:

```text
X_train_processed: (12328, 165)
X_test_processed:  (3083, 165)
```

The increase from 11 to 165 columns is caused by categorical expansion through one-hot encoding.

### Important

The preprocessor is not the ML model.

It prepares the input data.

The selected ML model is:

```text
RandomForestRegressor
```

The next stage is model training.
