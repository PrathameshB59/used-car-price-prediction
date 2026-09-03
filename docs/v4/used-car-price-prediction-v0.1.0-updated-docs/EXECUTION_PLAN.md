# Execution Plan

## v0.1.0 — Model A Web MVP

### Completed

- [x] Project setup
- [x] Virtual environment
- [x] Dataset investigation
- [x] V2 data cleaning/audit
- [x] Final feature selection
- [x] Preprocessing pipeline
- [x] Random Forest training
- [x] Model evaluation
- [x] Model artifact saving
- [x] Preprocessor artifact saving
- [x] Reload/prediction verification
- [x] Django integration
- [x] Responsive frontend
- [x] Custom Other/Unknown inputs
- [x] Seller Type UI field
- [x] Git LFS configuration
- [x] v0.1.0 release

## v0.2.0 — Model B

### Goal

Build a second valuation path that combines the existing ML estimate with current-market evidence.

### Planned Architecture

```text
                    User Input
                       │
             ┌─────────┴─────────┐
             ↓                   ↓
        Model A ML          Model B Pipeline
             │                   │
             │            AI model selection
             │                   ↓
             │          Web/current listings
             │                   +
             │          Official manufacturer info
             │                   ↓
             │          Structured evidence
             │                   ↓
             │          Python statistics
             │                   ↓
             └──────────┬────────┘
                        ↓
                 Separate results
                        ↓
             Model A | Model B
```

Model B should not blindly let an AI model invent a price. Extracted market evidence should be validated and statistical calculations should be performed in Python.

### Planned AI Selection

Default:

```text
Gemini 2.5 Flash
```

Experimental:

```text
Gemini 3.6 Flash
```

Additional models can be added later through configuration.

## v1.0.0 — Final Project

- [ ] Model A + Model B fully integrated
- [ ] End-to-end testing
- [ ] Public documentation
- [ ] Final UI polish
- [ ] Viva explanation
- [ ] Final presentation/demo
