# Indian Used Car Price Prediction

## v0.1.0 — Model A Web MVP

A Django-based AIML project that predicts an estimated used-car price for the Indian market.

### Release

- **Version:** `v0.1.0`
- **Release:** Model A Web MVP
- **Backend:** Django
- **Frontend:** HTML, CSS, JavaScript
- **ML:** Random Forest Regression
- **Model:** `RandomForestRegressor(n_estimators=100, random_state=42)`
- **Model artifacts:** saved model + saved preprocessing pipeline
- **Large model storage:** Git LFS

### Model A Features

The deployed V2 model expects exactly:

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

Seller Type is collected by the UI for future Model B market-enhanced valuation. It is intentionally not passed to Model A.

### Application Flow

```text
User input
   ↓
Django view
   ↓
Saved preprocessing pipeline
   ↓
Random Forest model
   ↓
Predicted price
   ↓
Web UI
```

### Run Locally

```bash
cd ~/Desktop/'AIML projects'/used-car-price-prediction
source .venv/bin/activate
python -m pip install -r requirements.txt
cd backend
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

### Release Commit

```text
e435b61 Complete Model A web integration
```

### Next Version

`v0.2.0` is planned for Model B: market-enhanced valuation using current Indian market evidence, with Model A and Model B shown separately.
