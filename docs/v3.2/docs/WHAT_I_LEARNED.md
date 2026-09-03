# What I Learned

## Regression

The target `selling_price` is continuous, so this is a regression problem.

## Train/Test Split

The model learns from training data and is evaluated on separate unseen test data.

## Fit vs Transform

```text
X_train → fit_transform()
X_test → transform()
```

The test data should not be used to fit preprocessing because that can cause data leakage.

## Categorical Encoding

Features such as brand, model, fuel type, seller type, and transmission type need numerical representations. The current preprocessing workflow produced 165 processed features.

## Random Forest

The current model uses 100 decision trees:

```text
RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)
```

## Model Evaluation

Current results:

- MAE: 98,825.34
- RMSE: 214,256.12
- R²: 0.9390

## Visualization

The Actual vs Predicted plot uses a diagonal line representing:

```text
Predicted Price = Actual Price
```

Points closer to that line are closer predictions.

## Django Integration

Deployment should preserve the training workflow:

```text
User input
→ same saved preprocessing
→ saved trained model
→ predicted price
```

The next learning step is saving, loading, and integrating these artifacts into Django.
