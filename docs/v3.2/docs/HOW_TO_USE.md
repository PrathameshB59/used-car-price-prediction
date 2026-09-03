# How to Use

## Current Status

The machine-learning notebook has completed the current Random Forest training and evaluation workflow.

Current results:

- Dataset records: 15,411
- Training records: 12,328
- Testing records: 3,083
- Processed features: 165
- MAE: 98,825.34
- RMSE: 214,256.12
- R²: 0.9390

## Run the Project

```bash
cd ~/Desktop/'AIML projects'/used-car-price-prediction
source .venv/bin/activate
cd backend
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Current ML Progress

Completed:

1. Dataset loading.
2. Data inspection.
3. Missing-value checking.
4. Duplicate checking.
5. Numerical/categorical feature selection.
6. Train/test splitting.
7. Preprocessing.
8. Categorical encoding.
9. Random Forest training.
10. Test prediction.
11. Actual/predicted comparison.
12. MAE, RMSE, and R² evaluation.
13. Actual vs Predicted visualization.

## Important Deployment Rule

Use the exact preprocessing pipeline from training:

```text
User input
→ saved preprocessing pipeline
→ saved trained model
→ predicted price
```

Do not manually create a different feature structure inside Django.
