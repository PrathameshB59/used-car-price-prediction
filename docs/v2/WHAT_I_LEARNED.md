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


---

## 25. Dataset Inspection Results From the Kaggle Notebook

The actual dataset inspection has now been performed in the Kaggle notebook.

The dataset contains:

- 15,411 rows
- 14 columns in the raw dataset
- 13 meaningful vehicle/listing columns plus one index-like `Unnamed: 0` column

The inspected columns are:

- `Unnamed: 0`
- `car_name`
- `brand`
- `model`
- `vehicle_age`
- `km_driven`
- `seller_type`
- `fuel_type`
- `transmission_type`
- `mileage`
- `engine`
- `max_power`
- `seats`
- `selling_price`

### Missing values

We used:

```python
df.isnull().sum()
```

Every column returned `0`, so no missing values were found in this dataset.

### Duplicate rows

We used:

```python
df.duplicated().sum()
```

The result was `0`, so there are no completely duplicated rows.

---

## 26. Understanding `value_counts()`

`value_counts()` counts how many times each distinct value appears in a column.

Example:

```python
df["fuel_type"].value_counts()
```

The result showed:

- Petrol: 7,643
- Diesel: 7,419
- CNG: 301
- LPG: 44
- Electric: 4

This helps us understand both the categories and how frequently they occur.

---

## 27. Understanding `nunique()`

`nunique()` means the number of different/unique values in a column.

For this project we found:

- `brand` → 32 unique values
- `model` → 120 unique values
- `seller_type` → 3 unique values
- `fuel_type` → 5 unique values
- `transmission_type` → 2 unique values

This matters because the number of categories affects our encoding and preprocessing decisions.

For example, one-hot encoding a column with 2 categories creates only a small number of encoded columns, while a column with 120 categories can create many columns.

---

## 28. Understanding the Categorical-Feature Inspection Code

We used a list of categorical columns and a loop:

```python
categorical_columns = [
    "brand",
    "model",
    "seller_type",
    "fuel_type",
    "transmission_type"
]

for column in categorical_columns:
    print(f"\n===== {column} =====")
    print(df[column].value_counts())
```

The list stores the column names we want to inspect.

The `for` loop goes through one column name at a time.

`df[column]` selects that column.

`.value_counts()` counts the frequency of each category.

`print()` displays the result.

This is an example of using Python to avoid repeating the same code manually for every categorical column.

---

## 29. Understanding `select_dtypes()`

We used code similar to:

```python
X.select_dtypes(include=["int64", "float64"]).columns.tolist()
```

and:

```python
X.select_dtypes(include=["object"]).columns.tolist()
```

`select_dtypes()` selects columns based on their data type.

`include=["int64", "float64"]` asks for numerical columns.

`include=["object"]` asks for object/text columns in this dataset.

`.columns` gets the column names.

`.tolist()` converts the column-name result into a normal Python list.

The detected numerical features are:

- `vehicle_age`
- `km_driven`
- `mileage`
- `engine`
- `max_power`
- `seats`

The detected categorical features are:

- `brand`
- `model`
- `seller_type`
- `fuel_type`
- `transmission_type`

---

## 30. Understanding the Target Separation

We created:

```python
X = df.drop(
    columns=["selling_price", "Unnamed: 0", "car_name"]
)

y = df["selling_price"]
```

`X` contains the input features used by the model.

`y` contains the value we want the model to predict.

We removed:

- `selling_price` because it is the target, not an input
- `Unnamed: 0` because it is an index-like column rather than a useful vehicle feature
- `car_name` because the current preprocessing plan uses `brand` and `model` instead of the combined name field

The resulting shapes were:

```text
Features shape: (15411, 11)
Target shape: (15411,)
```

The `11` means X currently has 11 input columns.

The target has 15,411 values, one for each row.

---

## 31. Understanding the Target Distribution

The target column is:

```python
df["selling_price"]
```

We used:

```python
df["selling_price"].describe()
```

and a histogram to understand its distribution.

The price distribution is strongly right-skewed: many cars are concentrated at lower prices, while a smaller number of cars have very high prices.

The observed target statistics included approximately:

- median: ₹556,000
- 75th percentile: ₹825,000
- 90th percentile: ₹1,375,000
- 95th percentile: ₹2,050,000
- 99th percentile: ₹4,545,000
- maximum: ₹39,500,000

This is important because the target contains some very high-priced cars compared with the majority of the dataset.

---

## 32. Understanding `quantile()`

We used:

```python
df["selling_price"].quantile([0.25, 0.50, 0.75, 0.90, 0.95, 0.99])
```

A quantile tells us the value below which a particular proportion of observations falls.

For example:

`0.50` means 50% of observations are at or below the returned value. This is the median.

`0.99` means 99% of observations are at or below the returned value.

Quantiles help us understand the distribution without looking only at the minimum and maximum.

---

## 33. Understanding `sort_values()` and `head()`

We used code like:

```python
df.sort_values("selling_price", ascending=False)[
    ["car_name", "brand", "model", "selling_price"]
].head(10)
```

`sort_values()` sorts rows according to a column.

`ascending=False` means highest values first.

The list of column names selects only the columns we want to display.

`head(10)` displays the first 10 rows of the sorted result.

This allowed us to inspect the highest-priced cars in the dataset.

---

## 34. Understanding `df.describe()` Output Such as `5.561e+05`

Scientific notation may appear in Pandas output.

For example:

`5.561e+05`

means:

`5.561 × 10^5 = 556,100`

So scientific notation is simply another way of displaying large or small numbers.

---

## 35. Important Learning Rule Before Encoding

We do not automatically encode every categorical column in exactly the same way without inspecting the data first.

The project currently has categorical cardinalities of:

- brand → 32
- model → 120
- seller_type → 3
- fuel_type → 5
- transmission_type → 2

This inspection gives us the information needed to make the preprocessing decision deliberately.

The current plan is to continue with preprocessing and encoding only after understanding these feature characteristics.

---

## 36. Current Project Learning Position

I can now explain the workflow as:

Dataset
→ inspect shape and columns
→ inspect data types
→ check missing values
→ check duplicates
→ summarize numerical data
→ inspect categorical distributions
→ measure categorical cardinality
→ understand the target
→ separate X and y
→ decide preprocessing/encoding
→ split data
→ train models
→ evaluate models
→ save the final model and preprocessing pipeline
→ connect the model to Django

The important principle remains:

WHY
→ WHAT
→ HOW
→ OUTPUT
→ EFFECT ON THE MODEL
