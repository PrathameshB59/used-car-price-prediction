# Execution Plan

## Phase 1 — Project Setup

- [x] Project structure
- [x] Virtual environment
- [x] Dependencies
- [x] Core package verification
- [x] Git repository

## Phase 2 — Dataset

- [x] Research datasets
- [x] Select CarDekho Used Car Dataset
- [x] Load and inspect dataset
- [x] Verify target variable

## Phase 3 — Data Understanding

- [x] Inspect shape and columns
- [x] Check data types
- [x] Check missing values
- [x] Check duplicates
- [x] Identify numerical features
- [x] Identify categorical features

## Phase 4 — Preprocessing

- [x] Separate features and target
- [x] Split training and testing data
- [x] Build preprocessing workflow
- [x] Encode categorical features
- [x] Fit preprocessing on training data
- [x] Transform test data
- [x] Create 165 processed features

## Phase 5 — Machine Learning

- [x] Create Random Forest model
- [x] Train model
- [x] Predict unseen test data
- [ ] Train additional models if required
- [ ] Final model selection

## Phase 6 — Evaluation

- [x] Calculate MAE
- [x] Calculate RMSE
- [x] Calculate R²
- [x] Compare actual and predicted values
- [x] Visualize predictions

Current results:

- MAE: **98,825.34**
- RMSE: **214,256.12**
- R²: **0.9390**

## Phase 7 — Model Saving

- [ ] Save trained model
- [ ] Save preprocessing pipeline
- [ ] Reload artifacts
- [ ] Verify prediction consistency

## Phase 8 — Django Integration

- [x] Django foundation
- [x] Predictor application
- [ ] Load saved model
- [ ] Load saved preprocessing pipeline
- [ ] Validate user input
- [ ] Generate prediction
- [ ] Return/display predicted price

## Phase 9 — Frontend and Testing

- [ ] Create final prediction form
- [ ] Connect form to Django
- [ ] Test valid/invalid inputs
- [ ] Test end-to-end prediction
- [ ] Run pytest

## Immediate Next Step

**Save the preprocessing pipeline and trained Random Forest model, reload them, and verify that predictions work after loading.**
