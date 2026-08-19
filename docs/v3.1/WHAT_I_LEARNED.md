---

## 37. What I Learned About the Preprocessor

The preprocessor is not the machine-learning model.

Its job is to prepare raw features so that the ML algorithm can work with them.

Conceptually:

```text
Raw X
→ Preprocessor
→ Numerical X
→ ML Model
```

The preprocessor contains rules learned from the training data, such as which categorical values exist.

---

## 38. What I Learned About `ColumnTransformer`

We used:

```python
ColumnTransformer(...)
```

because different feature types can require different treatment.

For this project:

```text
Categorical columns → OneHotEncoder
Numerical columns   → passthrough
```

So one preprocessing object can manage both groups.

---

## 39. What I Learned About `OneHotEncoder`

We use:

```python
OneHotEncoder(handle_unknown="ignore")
```

The encoder creates binary columns for categories.

`handle_unknown="ignore"` is important because a category might appear during testing or future prediction that was not present when the encoder was fitted.

Instead of crashing, the encoder handles that unseen category safely.

---

## 40. What I Learned About `fit()`

`fit()` means:

```text
Learn the preprocessing information.
```

For the encoder, this includes learning which categories exist.

Example:

```python
fuel_encoder.fit(...)
```

does not produce the final transformed data.

It learns the rules needed for transformation.

---

## 41. What I Learned About `transform()`

`transform()` means:

```text
Use the already learned preprocessing rules to convert data.
```

For example:

```python
preprocessor.transform(X_test)
```

uses the preprocessing information learned from the training data.

---

## 42. What I Learned About `fit_transform()`

`fit_transform()` combines:

```text
fit()
+
transform()
```

So:

```python
X_train_processed = preprocessor.fit_transform(X_train)
```

means:

```text
1. Learn preprocessing information from X_train.
2. Transform X_train using that information.
```

We use this on training data.

---

## 43. Why We Do Not Fit on Test Data

We use:

```python
X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)
```

not:

```python
preprocessor.fit_transform(X_test)
```

The test set should behave like unseen data.

If preprocessing learns from the test set, information from the test set can leak into the training process.

This is called data leakage.

---

## 44. What I Learned From the 11 → 165 Shape Change

Before encoding:

```text
X_train = (12328, 11)
X_test  = (3083, 11)
```

After preprocessing:

```text
X_train_processed = (12328, 165)
X_test_processed  = (3083, 165)
```

The number of rows stays the same because we did not create or remove records.

The number of columns increases because categorical features were expanded into multiple one-hot columns.

So:

```text
11 original model features
→ 165 numerical features after encoding
```

---

## 45. What I Learned About Train/Test Split

We used:

```python
train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)
```

This separates the data into two groups.

Training data:

```text
80%
```

Testing data:

```text
20%
```

The model learns from the training data.

The test data is kept aside for evaluating how well the trained model performs on unseen examples.

---

## 46. What I Learned About `random_state`

`random_state=42` makes the random split reproducible.

Without a fixed random state, running the same notebook again could produce a different split.

With the same random state, the split can be reproduced.

The number `42` itself has no special mathematical meaning here. It is simply a chosen fixed seed.

---

## 47. Our Selected ML Algorithm

We have decided to use:

```python
RandomForestRegressor
```

for this project.

This is the actual machine-learning model.

It is different from:

```python
preprocessor
```

The roles are:

```text
preprocessor
→ prepares data

RandomForestRegressor
→ learns patterns

model.predict()
→ produces predicted prices
```

---

## 48. Current Learning Position

The project has now reached the point where the data has been prepared for model training.

Current state:

```text
Dataset
→ inspection
→ feature/target separation
→ train/test split
→ categorical encoding
→ processed numerical features
→ RandomForestRegressor selected
```

The next learning step is:

```text
Train RandomForestRegressor
```

Then:

```text
Predict
→ Evaluate
→ Understand errors
→ Save model
→ Connect to Django
```

The learning rule remains:

WHY
→ WHAT
→ HOW
→ OUTPUT
→ EFFECT ON THE MODEL
