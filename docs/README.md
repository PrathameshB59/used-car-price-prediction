# Indian Used Car Price Prediction

## v0.4 — Results UI Release

A Django-based AIML project that predicts an estimated used-car price for the Indian market.

### Current Release

- **Version:** `v0.4`
- **Release:** Results UI polish and presentation-ready frontend cleanup
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
## Frontend Experience

The application provides three main user-facing areas:

```text
Predict
→ Enter vehicle details and receive ML Price Estimate and Market AI Estimate results.

Results
→ Review previous predictions stored locally in the browser.

How It Works
→ Understand the ML and market-AI price prediction pipelines.
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

### Presentation Branch

`presentation/cleanup` is based on the `v0.4` release and removes historical
backup copies and duplicated documentation. The release itself remains
recoverable through the `v0.4` tag and the
`backup/before-presentation-cleanup` branch.
