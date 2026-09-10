# Changelog

---

## 2026-09-05 — Model B Development

### Completed

- Model B Gemini integration added to the project.
- Tavily API configuration added as the web-search fallback for Model B.
- Gemini model selection made configurable through environment variables.
- Gemini API timeout configuration added.
- Django CSRF/form submission issue investigated and fixed.
- Normal Django POST prediction flow verified.
- Prediction form explicitly posts to `/`.
- Initial animated prediction flow implemented.
- Model A + Model B comparison flow integrated into the frontend.
- Local project backup created before the next UI redesign.

### Current Prediction Flow

```text
User enters car details
        ↓
Prediction form
        ↓
Loading / prediction animation
        ↓
Django backend
        ↓
Model A + Model B
        ↓
Comparison
```

## v0.1.0 — Model A Web MVP

### Completed

- Final V2 Random Forest model integrated into Django.
- Final preprocessing pipeline integrated into Django.
- Responsive prediction frontend completed.
- Automatic vehicle-age calculation added.
- `Other / Unknown` custom text support added for categorical inputs.
- Seller Type added to the web form for future market analysis.
- Obsolete `car_price_model.joblib` removed.
- Final model stored through Git LFS.
- Final preprocessor saved as a normal repository artifact.
- Release committed as `e435b61`.
- Git tag created: `v0.1.0`.

### Model A Input Contract

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

### Planned — v0.2.0

- Model B market-enhanced valuation.
- Current Indian used-car listing evidence.
- Official manufacturer/model verification where available.
- Selectable Gemini model configuration.
- Python-based market statistics.
- Side-by-side Model A and Model B results.
- Confidence/evidence presentation.

### Planned — v1.0.0

Final integrated project after Model A + Model B testing, documentation, and presentation preparation.
