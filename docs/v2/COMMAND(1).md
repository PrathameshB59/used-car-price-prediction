# Command Reference

This document contains commands used to develop and run the project.

## Project Directory

```bash
cd ~/Desktop/'AIML projects/'used-car-price-prediction
{ _ble_edit_exec_gexec__save_lastarg "$@"; } 4>&1 5>&2 &>/dev/null

---

## 2026-08-19 — Dataset Inspection Commands

The following notebook commands were used while learning the dataset.

### Check Data Types

```python
df.dtypes
```

Shows the data type stored in each column.

### Check Missing Values

```python
df.isnull().sum()
```

Counts missing values in every column.

### Check Duplicate Rows

```python
df.duplicated().sum()
```

Counts completely duplicated rows.

### Numerical Summary

```python
df.describe()
```

Produces count, mean, standard deviation, quartiles, minimum, and maximum for numerical columns.

### Count Categories

```python
df["fuel_type"].value_counts()
```

Counts how frequently each fuel category appears.

### Count Unique Categories

```python
df["brand"].nunique()
df["model"].nunique()
df["fuel_type"].nunique()
```

Returns the number of distinct values in each selected column.

### Inspect All Categorical Distributions

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

The loop avoids writing the same inspection command five times.

### Separate Features and Target

```python
X = df.drop(
    columns=["selling_price", "Unnamed: 0", "car_name"]
)

y = df["selling_price"]
```

`X` contains model inputs and `y` contains the target values.

### Inspect Numerical Columns by Data Type

```python
X.select_dtypes(include=["int64", "float64"]).columns.tolist()
```

Selects numerical columns and returns their names as a Python list.

### Inspect Categorical Columns by Data Type

```python
X.select_dtypes(include=["object"]).columns.tolist()
```

Selects object/text columns and returns their names as a Python list.

### Target Percentiles

```python
df["selling_price"].quantile(
    [0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
)
```

Calculates selected percentiles of the selling-price distribution.

### Inspect Highest-Priced Cars

```python
df.sort_values("selling_price", ascending=False)[
    ["car_name", "brand", "model", "selling_price"]
].head(10)
```

Sorts by price from highest to lowest and displays the first 10 rows.
