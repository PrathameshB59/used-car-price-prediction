# Changelog

## [Unreleased]

### 2026-08-21 — Kaggle Model Training and Evaluation

Added:

- Restored the Kaggle notebook.
- Attached the CarDekho Used Car Dataset.
- Ran all notebook cells successfully.
- Completed train/test splitting.
- Completed preprocessing and categorical encoding.
- Produced 165 processed features.
- Created and trained a Random Forest Regressor.
- Generated predictions for all 3,083 test records.
- Compared actual and predicted prices.
- Calculated MAE, RMSE, and R².
- Created an Actual vs Predicted visualization.

Current model:

```text
RandomForestRegressor
n_estimators=100
random_state=42
n_jobs=-1
```

Current results:

```text
MAE:  98825.3405297853
RMSE: 214256.11721654845
R²:   0.93901860493298
```

Status:

The current Random Forest experiment completed successfully. Final model selection, model saving, and Django prediction integration are still pending.

### Previous Milestones

- Project environment created.
- Django foundation created.
- Local Git repository initialized.
- Dataset selected and inspected.
- Initial documentation created.
