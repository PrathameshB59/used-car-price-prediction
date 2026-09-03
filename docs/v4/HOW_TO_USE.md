# How to Use

## v0.1.0 — Model A

### 1. Start Django

```bash
cd ~/Desktop/'AIML projects'/used-car-price-prediction
source .venv/bin/activate
cd backend
python manage.py runserver
```

### 2. Open the Website

Go to:

```text
http://127.0.0.1:8000/
```

### 3. Enter Car Details

Model A uses:

- Brand
- Model
- Manufacturing Year
- Vehicle Age
- Kilometers Driven
- Transmission
- Owner
- Fuel Type

Vehicle Age is automatically calculated from the manufacturing year.

### 4. Seller Type

Seller Type is displayed in the form, but Model A does not use it in prediction. It is reserved for the future market-enhanced Model B workflow.

### 5. Other / Unknown

Selecting `Other / Unknown` on supported categorical fields displays a text input. Enter the actual value there.

### Important ML Rule

Do not manually recreate preprocessing in Django.

The correct deployment flow is:

```text
User input
→ final_preprocessor.joblib
→ final_car_price_model.joblib
→ prediction
```

This preserves the feature transformation used during training.

### Example

```text
Brand: Maruti Suzuki
Model: Swift
Year: 2019
Age: 5
Kilometers: 50225
Transmission: Manual
Owner: First Owner
Fuel Type: Petrol
Seller Type: Dealer
```

The resulting number is an ML estimate, not a guaranteed selling price.
