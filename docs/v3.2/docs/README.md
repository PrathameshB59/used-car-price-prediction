# Used Car Price Prediction Using Machine Learning

## Current Project Status

This project predicts used-car selling prices for the Indian market using machine learning and will be integrated into a Django web application.

### Current Dataset and Model Facts

- Dataset: CarDekho Used Car Dataset
- Total records: 15,411
- Target: `selling_price`
- Missing values found: 0
- Completely duplicated rows found: 0
- Training records: 12,328
- Testing records: 3,083
- Processed features after preprocessing/encoding: 165

### Current Features

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

## Current Model

```python
RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)
```

The model was trained with:

```python
model.fit(X_train_processed, y_train)
```

Predictions were generated for the unseen test set:

```python
y_pred = model.predict(X_test_processed)
```

The preprocessing pipeline was fit only on training data and then used to transform test data:

```text
X_train → fit_transform()
X_test  → transform()
```

This helps prevent data leakage.

## Current Evaluation Results

| Metric | Result |
|---|---:|
| MAE | 98,825.34 |
| RMSE | 214,256.12 |
| R² | 0.9390 |

The current R² result means the model explains approximately 93.9% of the variation in the test-set selling prices.

An Actual vs Predicted scatter plot was also created. Points closer to the diagonal reference line represent closer predictions.

## Current Workflow

```text
Dataset
→ Feature/Target Separation
→ Train/Test Split
→ Preprocessing
→ Categorical Encoding
→ Random Forest Training
→ Test Prediction
→ MAE / RMSE / R² Evaluation
→ Actual vs Predicted Visualization
```

## Next Step: Model Deployment

The current model is not yet integrated into Django.

Next:

```text
Save preprocessing pipeline
+
Save trained model
↓
Load both artifacts
↓
Verify prediction after reload
↓
Create Django prediction logic
↓
Validate user input
↓
Apply same preprocessing
↓
Generate predicted price
↓
Display result
```

The Django application must use the same preprocessing pipeline that was used during training.
