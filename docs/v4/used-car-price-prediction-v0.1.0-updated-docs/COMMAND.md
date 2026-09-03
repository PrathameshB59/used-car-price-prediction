# Command Reference

## Start Project

```bash
cd ~/Desktop/'AIML projects'/used-car-price-prediction
source .venv/bin/activate
```

## Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## Django Check

```bash
cd backend
python manage.py check
```

## Database

```bash
python manage.py migrate
```

## Run Website

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Tests

From the project root:

```bash
pytest
```

## Git Release Verification

```bash
git status
git log --oneline -5
git tag
git show --stat v0.1.0
git lfs ls-files
```

Expected LFS entry:

```text
backend/predictor/ml/final_car_price_model.joblib
```

## Future Development

Create a feature branch before Model B work:

```bash
git checkout -b feature/model-b
```

After completing Model B, merge it into `main` and create the next release tag.
