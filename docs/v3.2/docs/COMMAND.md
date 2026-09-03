# Command Reference

## Project Directory

```bash
cd ~/Desktop/'AIML projects'/used-car-price-prediction
```

## Activate Virtual Environment

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## Django Checks

```bash
cd backend
python manage.py check
```

## Django Migrations

```bash
cd backend
python manage.py migrate
```

## Run Django

```bash
cd backend
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Run Tests

```bash
pytest
```

## Git

```bash
git status
git add .
git commit -m "Describe the change"
```

## Current ML Workflow

```text
Load dataset
→ inspect data
→ define features and target
→ split train/test data
→ fit preprocessing on training data
→ transform test data
→ create Random Forest
→ fit()
→ predict()
→ evaluate
```

The next commands added to this project should support saving and loading the preprocessing pipeline and trained model.
