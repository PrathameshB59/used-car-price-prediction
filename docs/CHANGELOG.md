# Changelog

## 2026-09-17 — v0.4 Results UI Release & Presentation Cleanup

### Release

- Released `v0.4` from commit `c522391`.
- Polished the Results history layout in light mode: the fixed topbar no
  longer overlaps content, saved-prediction headers have usable spacing, and
  Clear history uses the project button style rather than browser defaults.

### Presentation Branch

- Created `presentation/cleanup` from the `v0.4` release.
- Preserved the release state with `backup/before-presentation-cleanup`.
- Removed tracked historical UI snapshots, duplicate documentation versions,
  and obsolete backup/recovery copies from the presentation branch.
- Consolidated duplicate Results-history CSS into the original selectors and
  removed obsolete Clear history selectors.

## 2026-09-16 — Frontend Theme & UI Milestone

### Completed

- Light/dark theme toggle added to the main predictor interface.
- Theme preference is persisted in browser `localStorage`.
- Light mode uses a blue-gray application background with lighter cards and semantic accent colors.
- Separate Results dashboard remains the dedicated page for saved predictions.
- Separate How It Works page remains the dedicated explanation page.
- Topbar-only navigation retained across the predictor frontend.
- How It Works presents Model A and Model B as connected visual pipelines.
- Frontend presentation changes remain separate from Django prediction logic.
- Before/after Git checkpoints created for the UI milestone.
- UI milestone committed as `bc7b9de`.

### Theme Flow

```text
User selects Light / Dark
        ↓
JavaScript updates theme class
        ↓
CSS applies the selected visual system
        ↓
localStorage stores the preference
        ↓
Next page load restores the preference
```

## 2026-09-15 — Frontend Dashboard & UX Refinement

### Completed

- Separate Results dashboard page added.
- Prediction history stored locally in the browser using `localStorage`.
- Results page navigation refined with `Back to form` at the top and `Predict another car` as the bottom action.
- Prediction flow now distinguishes successful, partial, and failed valuation states on the frontend.
- ML Price Estimate and Market AI Estimate naming standardized across the frontend.
- How It Works page separated into its own frontend page.
- Topbar navigation simplified to a single application navigation bar.
- Frontend prediction flow kept separate from backend prediction logic.

### Current Frontend Flow

```text
Prediction Form
      ↓
Loading State
      ↓
Prediction Result
      ↓
ML Price Estimate + Market AI Estimate
      ↓
Local Prediction History
      ↓
Results Dashboard
```

----

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
