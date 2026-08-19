# What I Learned From the Used Car Price Prediction Project

This document records the concepts I personally learned while building the project.

The purpose is to understand the AIML workflow instead of only copying code.

---

## 1. Project Goal

The goal of this project is to predict the selling price of a used car in the Indian market using machine learning.

The final system will connect:

User input
→ Django application
→ preprocessing
→ trained machine-learning model
→ predicted used-car price

---

## 2. Machine Learning Problem

The target variable is:

selling_price

Because selling_price is a continuous numerical value, this is a:

Regression problem.

Regression means predicting a numerical quantity.

Examples:

- house price prediction
- temperature prediction
- used-car price prediction

Classification would instead predict categories such as:

- spam / not spam
- fraud / not fraud
- yes / no

---

## 3. Dataset

The project uses a CarDekho used-car dataset.

The dataset contains:

15,411 rows
14 columns

---

## 4. What Is a DataFrame?

Pandas DataFrame is a two-dimensional table containing rows and columns.

It allows us to:

- inspect data
- clean data
- analyze data
- transform data
- prepare data for machine learning

The dataset was loaded using:

pd.read_csv()

---

## 5. What Does Shape Mean?

df.shape returns:

(number_of_rows, number_of_columns)

For this dataset:

(15411, 14)

This means:

15,411 rows
14 columns

---

## 6. Dataset Columns

The dataset contains:

- car_name
- brand
- model
- vehicle_age
- km_driven
- seller_type
- fuel_type
- transmission_type
- mileage
- engine
- max_power
- seats
- selling_price

There is also an unnamed index-like column in the raw CSV.

---

## 7. Data Types

df.dtypes shows the type of data stored in each column.

Examples:

int64
float64
object

int means integer.

64 indicates the integer representation uses 64 bits.

float means a floating-point number, which can represent decimal values.

object is commonly used by Pandas for text/string data.

---

## 8. NumPy and np

NumPy is a Python library used for numerical computing.

It is commonly imported as:

import numpy as np

np is simply an alias for NumPy.

For example:

np.int64(0)

means the value 0 is represented as a NumPy 64-bit integer.

In our duplicate check, the important meaning was simply:

0 duplicate rows.

---

## 9. Missing Values

We checked missing values using:

df.isnull().sum()

The result showed:

0 missing values in every column.

This means the current dataset does not contain missing values that need to be handled at this stage.

---

## 10. Duplicate Records

We checked duplicate rows using:

df.duplicated().sum()

The result was:

0

Therefore, the dataset currently contains no completely duplicated rows.

---

## 11. Numerical Statistics

We used:

df.describe()

This provides summary statistics for numerical columns.

Important statistics include:

### count

Number of non-missing values.

### mean

Average value.

### std

Standard deviation.

It describes how spread out values are around the average.

### min

Smallest value.

### 25%

First quartile.

25% of observations are at or below this value.

### 50%

Median.

50% of observations are at or below this value.

### 75%

Third quartile.

75% of observations are at or below this value.

### max

Largest value.

---

## 12. Exploratory Data Analysis

The process of investigating the dataset before machine-learning training is called:

Exploratory Data Analysis (EDA).

EDA helps us understand:

- what data is available
- data types
- missing values
- duplicates
- distributions
- unusual values
- relationships between features
- possible outliers

The purpose is not simply to produce graphs.

The purpose is to understand the data before making modelling decisions.

---

## 13. Numerical Features

Our numerical features include:

- vehicle_age
- km_driven
- mileage
- engine
- max_power
- seats

These are already represented numerically.

---

## 14. Categorical Features

Our categorical features include:

- brand
- model
- seller_type
- fuel_type
- transmission_type

These contain categories rather than naturally meaningful numerical values.

Examples:

fuel_type:

Petrol
Diesel
CNG

transmission_type:

Manual
Automatic

---

## 15. What Is Encoding?

Encoding means converting categorical information into a numerical representation that a machine-learning algorithm can use.

A model cannot directly perform mathematical operations on text such as:

Petrol
Diesel
Manual

Therefore, categorical features need preprocessing.

---

## 16. One-Hot Encoding

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

This avoids creating an artificial numerical ranking between categories.

For example, assigning:

Petrol = 1
Diesel = 2
CNG = 3

could incorrectly suggest that CNG is mathematically greater than Diesel and Diesel is greater than Petrol.

One-hot encoding avoids that problem.

---

## 17. Encoding Is Preprocessing

Encoding does not mean the model has learned.

Encoding prepares the data.

The conceptual process is:

Raw data
→ preprocessing
→ encoding
→ numerical feature matrix
→ model training

Training is where the machine-learning algorithm learns patterns from examples.

---

## 18. How the Model Learns

During training, we provide:

X_train

which contains input features.

We also provide:

y_train

which contains the correct target values.

Conceptually:

car information
→ actual selling price

The model learns relationships between the input features and the target.

Later, a new car can be passed to the trained model to obtain a predicted price.

---

## 19. Regression

Our problem is regression because:

selling_price

is a continuous numerical value.

The model should output something such as:

₹350,000
₹620,000
₹980,000

rather than a category.

---

## 20. Planned Machine-Learning Algorithms

The project will not blindly assume that one algorithm is best.

We plan to understand and compare regression algorithms.

Potential models include:

1. Linear Regression
2. Decision Tree Regressor
3. Random Forest Regressor
4. Potentially a boosting model later if appropriate

Random Forest is currently our main candidate, but the final choice should be based on evaluation results rather than assumption.

---

## 21. Random Forest

Random Forest is a tree-based ensemble algorithm.

It builds many decision trees and combines their predictions.

A simplified idea is:

Training data
→ many decision trees
→ individual predictions
→ combined prediction

Random Forest is suitable to investigate for this project because the dataset contains a mixture of numerical and categorical information after preprocessing.

---

## 22. Important Difference: Encoding vs Learning

Encoding:

"Convert the data into a usable numerical representation."

Training:

"Learn patterns from the prepared data."

Prediction:

"Use the learned patterns to estimate the target for new data."

These are different stages of the machine-learning pipeline.

---

## 23. Current Learning Position

At this point I understand:

- what the project is trying to predict
- what regression means
- what a DataFrame is
- what dataset shape means
- how to inspect columns
- what data types mean
- what int64 means
- what NumPy and np mean
- how to check missing values
- how to check duplicate records
- how to read numerical statistics
- what EDA means
- what numerical features are
- what categorical features are
- why encoding is necessary
- what one-hot encoding means
- the difference between preprocessing and training
- how training data and target values are related
- why Random Forest is a candidate algorithm

---

## 24. Learning Philosophy

The project is being built as a learning project.

I should understand:

WHY we are doing something
→ WHAT the concept means
→ HOW the code implements it
→ WHAT the output tells us
→ HOW it affects the final model

I should not treat machine-learning code as something to copy and paste without understanding.

