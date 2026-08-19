# Used Car Price Prediction Using Machine Learning

## Project Overview

This project is a machine learning based web application that predicts
the estimated selling price of used cars in the Indian market.

The project uses a Kaggle dataset, Python-based machine learning
algorithms, and a Django backend. The user interface will be built using
HTML, CSS, and JavaScript.

The application will run locally on `localhost`.

## Problem Statement

Used-car prices depend on several factors such as vehicle age,
kilometers driven, brand, model, fuel type, transmission, ownership,
engine specifications, location, and other vehicle characteristics.

The objective of this project is to build a regression model capable of
estimating the selling price of a used car from relevant input features.

## Objective

Build a complete machine learning pipeline:

Kaggle Dataset
→ Data Understanding
→ Data Cleaning
→ Exploratory Data Analysis
→ Feature Engineering
→ Model Training
→ Model Evaluation
→ Model Selection
→ Model Saving
→ Django Backend
→ HTML/CSS/JavaScript Frontend
→ Price Prediction

## Target Market

Indian used-car market.

## Machine Learning Task

Regression.

## Technology Stack

### Programming

- Python 3.12.3

### Data Processing

- Pandas
- NumPy

### Data Visualization

- Matplotlib
- Seaborn

### Machine Learning

- Scikit-learn
- XGBoost
- Joblib

### Backend

- Django
- Django

### Frontend

- HTML
- CSS
- JavaScript

### Development

- Jupyter Notebook
- Pytest
- Linux Mint Cinnamon
- Bash

## Application Architecture

Browser
↓
HTML/CSS/JavaScript
↓
Django Backend
↓
Input Validation
↓
Preprocessing Pipeline
↓
Trained ML Model
↓
Predicted Used-Car Price
↓
JSON Response
↓
Web Interface

## Project Structure

```text
used-car-price-prediction/
│
├── docs/
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── COMMAND.md
│   ├── HOW_TO_USE.md
│   └── EXECUTION_PLAN.md
│
├── dataset/
├── notebooks/
├── models/
├── backend/
├── frontend/
├── tests/
├── requirements.txt
├── .gitignore
└── .venv/
{ _ble_edit_exec_gexec__save_lastarg "$@"; } 4>&1 5>&2 &>/dev/null

---

## Django Web Architecture

The project uses Django as the web application framework.

```text
Browser
   ↓
HTML / CSS / JavaScript
   ↓
Django
   ↓
Predictor Application
   ↓
Input Validation
   ↓
ML Preprocessing
   ↓
Trained ML Model
   ↓
Predicted Used-Car Price
   ↓
Django Response
   ↓
Web Browser
{ _ble_edit_exec_gexec__save_lastarg "$@"; } 4>&1 5>&2 &>/dev/null

---

## Current Development Status

### Django Web Foundation — Completed

The Django web application is now successfully running on localhost.

Completed:

- Django 6.1 installed and verified.
- Django project `config` created.
- Django application `predictor` created.
- Django URL routing configured.
- Django homepage view configured.
- Django templates configured.
- Django static files configured.
- HTML frontend connected to Django.
- CSS frontend connected to Django.
- JavaScript frontend connected to Django.
- SQLite database initialized.
- Django migrations applied.
- Django system checks pass.
- Localhost website verified successfully.

Current website:

```text
http://127.0.0.1:8000/
{ _ble_edit_exec_gexec__save_lastarg "$@"; } 4>&1 5>&2 &>/dev/null

---

## Version Control

The project uses Git for local version control.

The repository uses the `main` branch.

The following are intentionally excluded from version control:

- Python virtual environment
- SQLite database
- Python cache files
- Local datasets
- Trained model binaries
- Environment/secrets files
- IDE-generated files

The first Git commit is being created after the Django frontend
foundation was successfully verified.

---

## Dataset Acquisition Status

The selected Kaggle dataset has been downloaded and extracted locally.

### Dataset

**Name:** CarDekho Used Car Dataset

**Source:** Kaggle

**Local CSV:**

```text
dataset/cardekho_dataset.csv
{ _ble_edit_exec_gexec__save_lastarg "$@"; } 4>&1 5>&2 &>/dev/null

---

## 2026-08-19 — Machine Learning Notebook Progress

The selected CarDekho Used Car Dataset has now been loaded and inspected in the Kaggle training notebook.

### Verified Dataset Facts

- 15,411 rows
- 14 raw columns
- `selling_price` is the target variable
- No missing values were found using `df.isnull().sum()`
- No completely duplicated rows were found using `df.duplicated().sum()`

### Feature Understanding

Numerical features currently identified:

- `vehicle_age`
- `km_driven`
- `mileage`
- `engine`
- `max_power`
- `seats`

Categorical features currently identified:

- `brand`
- `model`
- `seller_type`
- `fuel_type`
- `transmission_type`

Categorical cardinalities inspected:

- brand → 32
- model → 120
- seller_type → 3
- fuel_type → 5
- transmission_type → 2

### Target Understanding

The target is a continuous numerical value, so the problem is regression.

The selling-price distribution is strongly right-skewed, with a small number of very high-priced vehicles.

### Preprocessing Learning Status

Encoding has been studied as a preprocessing step rather than a learning algorithm. One-hot encoding is the current concept being investigated, but the final preprocessing strategy will be chosen after considering the categorical cardinalities and the model evaluation results.

### Current ML Pipeline Position

```text
Dataset
→ Data Understanding
→ EDA
→ Feature/Target Separation
→ Categorical Feature Inspection
→ Preprocessing Decision
→ Encoding
→ Train/Test Split
→ Model Training
→ Evaluation
→ Model Selection
→ Model Saving
→ Django Integration
```
