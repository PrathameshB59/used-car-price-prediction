# Execution Plan

## Project

**Used Car Price Prediction Using Machine Learning**

## Target Market

**Indian Used-Car Market**

## Objective

Build a machine learning based web application that predicts the
estimated selling price of a used car using vehicle and listing
information.

The final application will run locally as a website using Django,
HTML, CSS, and JavaScript.

---

# Development Phases

## Phase 1 — Project Setup

- [x] Decide project topic
- [x] Select Indian used-car market
- [x] Create project directory
- [x] Create project subdirectories
- [x] Create documentation structure
- [x] Create Python virtual environment
- [x] Create requirements.txt
- [x] Create .gitignore
- [x] Install Python dependencies
- [x] Verify core Python/ML packages

## Phase 2 — Dataset Selection

- [x] Research Indian used-car datasets on Kaggle
- [x] Compare candidate datasets
- [x] Identify preferred dataset
- [ ] Download selected dataset
- [ ] Inspect actual dataset file
- [ ] Verify rows and columns
- [ ] Verify target variable
- [ ] Document dataset source and license
- [ ] Decide final feature policy

## Phase 3 — Data Understanding

- [ ] Load dataset using Pandas
- [ ] Inspect dataset shape
- [ ] Inspect column names
- [ ] Inspect data types
- [ ] Check missing values
- [ ] Check duplicate records
- [ ] Check unique values
- [ ] Identify numerical features
- [ ] Identify categorical features
- [ ] Identify boolean/date features
- [ ] Analyze target variable

## Phase 4 — Data Cleaning

- [ ] Handle missing values
- [ ] Handle duplicate records
- [ ] Convert incorrect data types
- [ ] Clean numerical values
- [ ] Clean categorical values
- [ ] Process dates where appropriate
- [ ] Investigate outliers
- [ ] Document cleaning decisions

## Phase 5 — Exploratory Data Analysis

- [ ] Analyze selling-price distribution
- [ ] Analyze price vs vehicle age
- [ ] Analyze price vs kilometers driven
- [ ] Analyze price by fuel type
- [ ] Analyze price by transmission
- [ ] Analyze price by ownership
- [ ] Analyze price by brand
- [ ] Analyze price by body type
- [ ] Analyze price by city/state where appropriate
- [ ] Analyze numerical correlations
- [ ] Document EDA findings

## Phase 6 — Feature Engineering

- [ ] Create vehicle age feature
- [ ] Process categorical features
- [ ] Process numerical features
- [ ] Evaluate high-cardinality features
- [ ] Remove unsuitable/leakage-prone features
- [ ] Build preprocessing pipeline
- [ ] Prepare final ML feature set

## Phase 7 — Machine Learning

- [ ] Split data into training and testing sets
- [ ] Train Linear Regression
- [ ] Train Decision Tree Regressor
- [ ] Train Random Forest Regressor
- [ ] Train Gradient Boosting Regressor
- [ ] Train XGBoost Regressor
- [ ] Record training results

## Phase 8 — Model Evaluation

- [ ] Calculate MAE
- [ ] Calculate RMSE
- [ ] Calculate R²
- [ ] Compare all models
- [ ] Analyze prediction errors
- [ ] Select final model
- [ ] Document model-selection reasoning

## Phase 9 — Model Saving

- [ ] Save trained model
- [ ] Save preprocessing pipeline
- [ ] Test loading model
- [ ] Test prediction from saved model
- [ ] Store model artifacts in models/

## Phase 10 — Django Backend

- [ ] Create Django application
- [ ] Create prediction endpoint
- [ ] Validate API input
- [ ] Load saved model
- [ ] Apply preprocessing
- [ ] Generate prediction
- [ ] Return JSON response
- [ ] Add error handling

## Phase 11 — Frontend

- [ ] Create HTML interface
- [ ] Create CSS design
- [ ] Create JavaScript logic
- [ ] Create car information form
- [ ] Add client-side validation
- [ ] Connect frontend to Django API
- [ ] Display predicted price
- [ ] Add loading/error states
- [ ] Make interface responsive

## Phase 12 — Integration

- [ ] Connect frontend and backend
- [ ] Test complete prediction flow
- [ ] Test valid inputs
- [ ] Test invalid inputs
- [ ] Test missing inputs
- [ ] Test multiple vehicle examples
- [ ] Verify prediction consistency

## Phase 13 — Testing

- [ ] Test preprocessing
- [ ] Test model loading
- [ ] Test prediction function
- [ ] Test Django API
- [ ] Test frontend integration
- [ ] Run pytest
- [ ] Perform end-to-end testing

## Phase 14 — Documentation

- [ ] Update README
- [ ] Update CHANGELOG
- [ ] Update COMMAND
- [ ] Update HOW_TO_USE
- [ ] Update EXECUTION_PLAN
- [ ] Add architecture explanation
- [ ] Add dataset explanation
- [ ] Add ML results
- [ ] Add screenshots
- [ ] Add troubleshooting section

## Phase 15 — Final Project

- [ ] Final code cleanup
- [ ] Final testing
- [ ] Verify localhost application
- [ ] Prepare project demonstration
- [ ] Prepare AIML viva explanation
- [ ] Prepare presentation
- [ ] Prepare final project report

---

## Learning Update: Encoding

Encoding is the process of converting categorical features into numerical representations that machine-learning algorithms can use.

Our dataset contains numerical features such as:

- vehicle_age
- km_driven
- mileage
- engine
- max_power
- seats

It also contains categorical features such as:

- brand
- model
- seller_type
- fuel_type
- transmission_type

Numerical values can generally be used directly by machine-learning algorithms, while categorical values such as "Petrol", "Diesel", "Manual", or "Maruti" need to be represented numerically.

### One-Hot Encoding

One-hot encoding creates a separate binary column for each category.

Example:

fuel_type:

Petrol
Diesel
CNG

can become:

fuel_Petrol | fuel_Diesel | fuel_CNG
------------ | ----------- | ----------
1            | 0           | 0
0            | 1           | 0
0            | 0           | 1

This avoids incorrectly creating an artificial numerical order between categories.

### Project Decision

We will inspect the number of unique values in each categorical feature before deciding the exact preprocessing strategy.

The target column is:

selling_price

The target is not encoded because it is the continuous numerical value that the model is learning to predict.

Encoding is part of preprocessing, not model training.

Conceptually:

Raw data
→ preprocessing
→ encoding
→ numerical feature matrix
→ model training
→ trained model
→ prediction

The same preprocessing used during training must also be applied to new user input during prediction.


---

# 2026-08-19 — Execution Progress Update

The following data-understanding work has now been completed in the Kaggle notebook. The original checklist above is intentionally preserved; this section records the actual progress without rewriting the plan.

## Data Understanding Completed

- Loaded the CarDekho used-car dataset.
- Verified dataset shape: 15,411 rows and 14 columns.
- Inspected column data types.
- Checked missing values: zero missing values in all columns.
- Checked duplicate rows: zero duplicate rows.
- Calculated numerical summary statistics.
- Identified numerical features.
- Identified categorical features.
- Inspected categorical value distributions.
- Calculated categorical cardinality with `nunique()`.
- Investigated the target variable `selling_price`.
- Visualized the target-price distribution.
- Inspected high-priced vehicles.
- Calculated target percentiles.
- Separated features `X` and target `y`.

## Current Feature Set Before Encoding

After removing `selling_price`, `Unnamed: 0`, and `car_name` from the model inputs, the current feature matrix contains 11 columns.

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

## Current Preprocessing Decision Point

The next learning step is categorical encoding.

The categorical cardinalities are:

```text
brand → 32
model → 120
seller_type → 3
fuel_type → 5
transmission_type → 2
```

This information will be used to choose an appropriate preprocessing strategy instead of assuming that every categorical column should automatically be handled identically.

## Important Workflow Rule

The preprocessing fitted during training must be reused for new user input during prediction. This is why the final system should save and load the preprocessing pipeline together with the trained model.
