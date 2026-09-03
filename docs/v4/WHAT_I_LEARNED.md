# What I Learned — v0.1.0

This project is being developed as an AIML learning project. The goal is to understand why each component exists, not only how to run it.

## Regression

Used-car price is continuous, so price prediction is a regression problem.

## Random Forest

Random Forest combines many decision trees. The current model uses 100 estimators and `random_state=42`.

```python
RandomForestRegressor(
    n_estimators=100,
    random_state=42
)
```

## Preprocessing

Raw categorical and numerical values must be transformed into the representation expected by the trained model.

The saved preprocessing pipeline is reused during prediction.

```text
training data
→ fit preprocessing
→ transform data
→ train model
```

For deployment:

```text
user input
→ transform using saved preprocessing
→ model prediction
```

## Data Leakage

Training preprocessing must not learn from the test set.

Conceptually:

```text
X_train → fit_transform()
X_test  → transform()
```

The same principle is preserved by saving the fitted preprocessing pipeline.

## Django Integration

Django receives form values, converts numeric fields, builds the model input dictionary, sends it through the saved preprocessing pipeline, and displays the prediction.

## Feature Contract

The final Model A model expects exactly:

```text
Brand
model
Year
Age
kmDriven
Transmission
Owner
FuelType
```

Seller Type is currently UI-only for Model A.

## Git LFS

The final Random Forest artifact is large, so Git LFS is used instead of storing the large binary directly as a normal Git object.

## Versioning

```text
v0.1.0 → Model A Web MVP
v0.2.0 → Model B market-enhanced valuation
v1.0.0 → final stable project
```

## Main Learning Pattern

For every project change, understand:

```text
WHY?
WHAT concept?
HOW does the code implement it?
WHAT does the output mean?
WHAT changes in the architecture?
```
